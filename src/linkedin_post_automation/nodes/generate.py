from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

from linkedin_post_automation.prompts.templates import (
    POST_GENERATION_PROMPT,
    PostSuggestions,
)


def generate_posts(state: dict) -> dict:
    tool = TavilySearch(max_results=5, search_depth="advanced")
    search_results = tool.invoke(state["topic"])

    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
    structured_llm = llm.with_structured_output(PostSuggestions)

    chain = POST_GENERATION_PROMPT | structured_llm
    result = chain.invoke({
        "topic": state["topic"],
        "search_context": search_results,
    })

    return {"posts": result.posts}
