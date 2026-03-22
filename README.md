# LinkedIn Post Automation

CLI tool that generates AI-powered LinkedIn posts using Gemini and publishes them via the LinkedIn API.

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

You'll need:
- **GOOGLE_API_KEY** — Get from [Google AI Studio](https://aistudio.google.com/apikey)
- **LINKEDIN_ACCESS_TOKEN** — See [Obtaining LinkedIn Access Token](#obtaining-linkedin-access-token) below
- **LINKEDIN_PERSON_URN** — See [Getting your Person URN](#getting-your-person-urn) below

### Obtaining LinkedIn Access Token

1. Go to [https://developer.linkedin.com](https://developer.linkedin.com) and create an app
   - You'll need a LinkedIn Page — if you're an individual developer, select the default page associated with your profile
   - Upload any placeholder image as the app logo
2. In your app's **Auth** tab, note your **Client ID** and **Client Secret**
3. Under **OAuth 2.0 settings**, add `https://localhost:8080/callback` as a **Redirect URL**
4. Go to the **Products** tab and request access to **"Share on LinkedIn"** (grants `w_member_social` scope)
5. Open this URL in your browser (replace `{YOUR_CLIENT_ID}`):

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={YOUR_CLIENT_ID}&redirect_uri=https://localhost:8080/callback&scope=openid%20profile%20w_member_social
```

6. Sign in and authorize the app
7. You'll be redirected to a URL like `https://localhost:8080/callback?code=SOME_CODE`. The page won't load — that's expected. Copy the `code` value from the URL bar
8. **Immediately** exchange the code for a token (the code expires in ~30 seconds):

```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d "grant_type=authorization_code" \
  -d "code={THE_CODE_YOU_COPIED}" \
  -d "redirect_uri=https://localhost:8080/callback" \
  -d "client_id={YOUR_CLIENT_ID}" \
  -d "client_secret={YOUR_CLIENT_SECRET}"
```

9. The response will contain your access token:

```json
{
  "access_token": "AQV...",
  "expires_in": 5184000
}
```

Paste the `access_token` value into your `.env` file. The token is valid for **60 days**.

### Getting your Person URN

With your access token, run:

```bash
curl -H "Authorization: Bearer {YOUR_ACCESS_TOKEN}" \
     https://api.linkedin.com/v2/userinfo
```

The `sub` field in the response is your person ID. Set `LINKEDIN_PERSON_URN=urn:li:person:{sub}` in your `.env`.

## Usage

```bash
uv run python main.py
```

The tool will:
1. Ask you for a topic
2. Generate 3 LinkedIn post suggestions using Gemini
3. Display the posts for you to choose from
4. Publish the selected post to LinkedIn
