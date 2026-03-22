from linkedin_post_automation.linkedin.client import (
    LinkedInClientError,
    post_to_linkedin,
)
from linkedin_post_automation.prompts.templates import LinkedInPost


def _format_post(post: LinkedInPost) -> str:
    hashtags_str = " ".join(f"#{tag}" for tag in post.hashtags)
    return f"{post.title}\n\n{post.content}\n\n{hashtags_str}"


def publish_post(state: dict) -> dict:
    selected_post: LinkedInPost = state["selected_post"]
    post_text = _format_post(selected_post)

    try:
        result = post_to_linkedin(post_text)
        return {"result": result}
    except LinkedInClientError as e:
        return {"result": {"success": False, "message": str(e)}}
