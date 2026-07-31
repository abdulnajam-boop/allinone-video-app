from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(slots=True)
class MemoryDocument:
    """A text document stored in ArautoVideo's semantic memory."""

    document_id: int
    text: str
    metadata: dict[str, str]


class TurboVecMemoryStore:
    """Local semantic-memory store backed by TurboVec.

    TurboVec stores vectors and stable numeric IDs. ArautoVideo stores the
    corresponding text and metadata in a small JSON sidecar file.

    The embedding model is injected so this provider remains independent of a
    particular embedding service. The object must expose ``encode(texts)`` and
    return an array-like value with one vector per input text.
    """

    def __init__(
        self,
        *,
        embedding_model: object,
        dimension: int,
        index_path: str | Path = "data/memory/arautovideo.tvim",
        metadata_path: str | Path = "data/memory/documents.json",
        bit_width: int = 4,
    ) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be greater than zero")
        if bit_width not in {2, 4}:
            raise ValueError("bit_width must be either 2 or 4")

        try:
            from turbovec import IdMapIndex
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "TurboVec memory dependencies are not installed. Run: "
                "pip install -r requirements-memory.txt"
            ) from exc

        self.embedding_model = embedding_model
        self.dimension = dimension
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)

        if self.index_path.exists():
            self.index = IdMapIndex.load(str(self.index_path))
        else:
            self.index = IdMapIndex(dim=dimension, bit_width=bit_width)

        self.documents = self._load_documents()

    def add(self, documents: Iterable[MemoryDocument]) -> None:
        items = list(documents)
        if not items:
            return

        ids = np.asarray([item.document_id for item in items], dtype=np.uint64)
        if len(set(ids.tolist())) != len(ids):
            raise ValueError("document IDs must be unique within one add operation")

        vectors = self._embed([item.text for item in items])
        self.index.add_with_ids(vectors, ids)

        for item in items:
            self.documents[str(item.document_id)] = asdict(item)

        self.save()

    def search(self, query: str, *, limit: int = 5) -> list[dict[str, object]]:
        if limit <= 0:
            raise ValueError("limit must be greater than zero")
        if not self.documents:
            return []

        query_vector = self._embed([query])
        scores, ids = self.index.search(query_vector, k=limit)

        score_values = np.asarray(scores).reshape(-1).tolist()
        id_values = np.asarray(ids).reshape(-1).tolist()

        results: list[dict[str, object]] = []
        for score, document_id in zip(score_values, id_values, strict=False):
            stored = self.documents.get(str(int(document_id)))
            if stored is None:
                continue
            results.append({"score": float(score), **stored})
        return results

    def remove(self, document_id: int) -> bool:
        key = str(document_id)
        if key not in self.documents:
            return False

        self.index.remove(document_id)
        del self.documents[key]
        self.save()
        return True

    def save(self) -> None:
        self.index.write(str(self.index_path))
        self.metadata_path.write_text(
            json.dumps(self.documents, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _embed(self, texts: list[str]) -> np.ndarray:
        encode = getattr(self.embedding_model, "encode", None)
        if not callable(encode):
            raise TypeError("embedding_model must expose a callable encode(texts) method")

        vectors = np.asarray(encode(texts), dtype=np.float32)
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)
        if vectors.ndim != 2 or vectors.shape[1] != self.dimension:
            raise ValueError(
                f"embedding model returned shape {vectors.shape}; "
                f"expected (n, {self.dimension})"
            )
        return np.ascontiguousarray(vectors, dtype=np.float32)

    def _load_documents(self) -> dict[str, dict[str, object]]:
        if not self.metadata_path.exists():
            return {}
        try:
            data = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Unable to load memory metadata: {exc}") from exc
        if not isinstance(data, dict):
            raise RuntimeError("Memory metadata must contain a JSON object")
        return data
