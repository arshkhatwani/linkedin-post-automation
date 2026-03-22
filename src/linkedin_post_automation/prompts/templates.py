from pydantic import BaseModel, Field, field_validator
from langchain_core.prompts import ChatPromptTemplate


class LinkedInPost(BaseModel):
    title: str = Field(description="An attention-grabbing hook or first line for the post")
    content: str = Field(
        description=(
            "The full body of the LinkedIn post (excluding the title). "
            "Use real newlines to separate paragraphs, never literal backslash-n sequences."
        )
    )
    hashtags: list[str] = Field(description="3-5 relevant hashtags without the # symbol")

    @field_validator("title", "content")
    @classmethod
    def clean_newlines(cls, v: str) -> str:
        return v.replace("\\n", "\n").strip()


class PostSuggestions(BaseModel):
    posts: list[LinkedInPost] = Field(
        description="Exactly 3 LinkedIn post suggestions",
        min_length=3,
        max_length=3,
    )


POST_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a LinkedIn content strategist. You write engaging, professional "
            "posts that drive meaningful engagement. Your posts are concise, authentic, "
            "and provide genuine value to readers. Avoid being overly salesy or using "
            "corporate jargon. Use line breaks for readability.",
        ),
        (
            "human",
            "Generate exactly 3 different LinkedIn post suggestions about the "
            "following topic:\n\n"
            "Topic: {topic}\n\n"
            "Below are factual excerpts scraped from the web (including tech docs) "
            "about this topic. Use these as the factual basis for your posts — "
            "ensure claims, stats, and technical details are accurate and grounded "
            "in this research:\n"
            "{search_context}\n\n"
            "Each post should have a different angle or style:\n"
            "1. A thought-leadership / opinion post\n"
            "2. A storytelling / personal experience post\n"
            "3. A practical tips / how-to post\n\n"
            "Make each post between 100-300 words. Use line breaks between paragraphs "
            "for readability.",
        ),
    ]
)
