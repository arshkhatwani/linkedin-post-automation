from langgraph.types import interrupt


def review_posts(state: dict) -> dict:
    posts = state["posts"]

    selected_index = interrupt({"posts": [p.model_dump() for p in posts]})

    return {"selected_post": posts[selected_index]}
