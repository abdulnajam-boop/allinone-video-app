from app.agents.content_agents import ResearchAgent, ScriptAgent, StoryboardAgent
from app.core.models import VideoJob, VideoRequest


class VideoPlanningPipeline:
    def __init__(self) -> None:
        self.research_agent = ResearchAgent()
        self.script_agent = ScriptAgent()
        self.storyboard_agent = StoryboardAgent()

    def run(self, request: VideoRequest) -> VideoJob:
        research = self.research_agent.run(request)
        script = self.script_agent.run(request, research)
        scenes = self.storyboard_agent.run(request, script)
        return VideoJob(
            request=request,
            research=research,
            script=script,
            scenes=scenes,
        )
