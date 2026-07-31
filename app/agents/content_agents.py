from math import ceil

from app.core.models import ResearchResult, Scene, Script, Source, VideoRequest


class ResearchAgent:
    """Produces a deterministic research brief until live providers are enabled."""

    def run(self, request: VideoRequest) -> ResearchResult:
        topic = request.topic.strip()
        return ResearchResult(
            topic=topic,
            angle=f"Explain why {topic} matters to {request.audience} in a practical way.",
            key_points=[
                f"Define {topic} in simple language.",
                f"Show the most useful benefit or consequence of {topic}.",
                "Give one concrete example the viewer can remember.",
                "Finish with a practical next step.",
            ],
            sources=[
                Source(
                    title="Provider pending",
                    summary=(
                        "This development result is generated locally. Live source adapters "
                        "will replace it before production publishing."
                    ),
                )
            ],
        )


class ScriptAgent:
    def run(self, request: VideoRequest, research: ResearchResult) -> Script:
        hook = f"Most people misunderstand {research.topic}—here is what actually matters."
        body = " ".join(
            [
                f"First, {research.key_points[0].lower()}",
                f"Next, {research.key_points[1].lower()}",
                f"For example, {research.key_points[2].lower()}",
                f"Finally, {research.key_points[3].lower()}",
            ]
        )
        return Script(
            hook=hook,
            narration=f"{hook} {body}",
            call_to_action="Follow for more useful AI-powered explainers.",
            estimated_duration_seconds=request.duration_seconds,
        )


class StoryboardAgent:
    def run(self, request: VideoRequest, script: Script) -> list[Scene]:
        scene_count = max(3, min(8, ceil(request.duration_seconds / 10)))
        scene_duration = max(3, request.duration_seconds // scene_count)
        lines = [script.hook] + script.narration.split(". ")[1:] + [script.call_to_action]

        scenes: list[Scene] = []
        for index in range(scene_count):
            narration = lines[index % len(lines)].strip().rstrip(".") + "."
            scenes.append(
                Scene(
                    number=index + 1,
                    duration_seconds=scene_duration,
                    narration=narration,
                    visual_prompt=(
                        f"Vertical cinematic scene illustrating '{request.topic}', "
                        f"scene {index + 1}, clean composition, no logos"
                    ),
                    on_screen_text=narration[:80],
                )
            )
        return scenes
