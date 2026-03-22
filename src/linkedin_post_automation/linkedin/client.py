import os

import httpx


LINKEDIN_API_VERSION = "202603"
POSTS_URL = "https://api.linkedin.com/rest/posts"


class LinkedInClientError(Exception):
    pass


def post_to_linkedin(post_text: str) -> dict:
    access_token = os.environ["LINKEDIN_ACCESS_TOKEN"]
    person_urn = os.environ["LINKEDIN_PERSON_URN"]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": LINKEDIN_API_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
    }

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "commentary": post_text,
    }

    response = httpx.post(POSTS_URL, headers=headers, json=payload)

    if response.status_code == 201:
        post_id = response.headers.get("x-restli-id", "unknown")
        return {
            "success": True,
            "post_id": post_id,
            "message": "Post published successfully!",
        }

    raise LinkedInClientError(
        f"LinkedIn API error ({response.status_code}): {response.text}"
    )
