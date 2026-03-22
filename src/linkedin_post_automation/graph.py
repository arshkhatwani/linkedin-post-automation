from typing import Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

from linkedin_post_automation.nodes.generate import generate_posts
from linkedin_post_automation.nodes.publish import publish_post
from linkedin_post_automation.nodes.review import review_posts
from linkedin_post_automation.prompts.templates import LinkedInPost


class GraphState(TypedDict, total=False):
    topic: str
    posts: list[LinkedInPost]
    selected_post: LinkedInPost
    result: dict[str, Any]


def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("generate", generate_posts)
    workflow.add_node("review", review_posts)
    workflow.add_node("publish", publish_post)

    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "review")
    workflow.add_edge("review", "publish")
    workflow.add_edge("publish", END)

    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)
