from langchain_google_genai import ChatGoogleGenerativeAI

from linkedin_post_automation.prompts.templates import (
    POST_GENERATION_PROMPT,
    PostSuggestions,
)


def generate_posts(state: dict) -> dict:
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
    structured_llm = llm.with_structured_output(PostSuggestions)

    chain = POST_GENERATION_PROMPT | structured_llm
    result = chain.invoke({"topic": state["topic"]})

    return {"posts": result.posts}
