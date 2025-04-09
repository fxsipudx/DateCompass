from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import logging
from typing import List, Dict
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="DateCompass API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RedditAPI:
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.token = None
        self.token_expiry = None

    async def get_token(self) -> str:
        """Get or refresh Reddit API token."""
        if self.token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.reddit.com/api/v1/access_token",
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
                headers={"User-Agent": "DateCompass/1.0"}
            )
            data = response.json()
            self.token = data["access_token"]
            self.token_expiry = datetime.now() + timedelta(seconds=data["expires_in"] - 60)
            return self.token

    async def search_posts(self, city: str) -> List[Dict]:
        """Search Reddit for date spots."""
        token = await self.get_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://oauth.reddit.com/search",
                headers={
                    "Authorization": f"Bearer {token}",
                    "User-Agent": "DateCompass/1.0"
                },
                params={
                    "q": f"{city} date spots restaurants bars",
                    "sort": "relevance",
                    "t": "year",
                    "limit":10
                }
            )
            posts = response.json()["data"]["children"]
            return [
                {
                    "title": post["data"]["title"],
                    "text": post["data"]["selftext"][:500],
                    "url": post["data"]["url"],
                    "score": post["data"]["score"]
                }
                for post in posts
                if post["data"]["selftext"]
            ]

async def generate_recommendations(posts: List[Dict], city: str) -> List[Dict]:
    """Generate recommendations using OpenAI."""
    if not posts:
        return []

    content = "\n\n".join(
        f"Title: {post['title']}\nContent: {post['text']}"
        for post in posts[:5]
    )

    try:
        completion = await openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"""Based on Reddit posts about {city}, suggest 5 specific date spots.
                Format each as: Name: Description (Price £-£££) | Why it's good for dates
                Example: Skylight: Rooftop bar with city views (££) | Perfect for sunset drinks"""
            }, {
                "role": "user",
                "content": content
            }]
        )
        
        recommendations = []
        for line in completion.choices[0].message.content.split("\n"):
            if ":" in line and "|" in line:
                name, rest = line.split(":", 1)
                desc, reason = rest.split("|")
                recommendations.append({
                    "name": name.strip(),
                    "description": desc.strip(),
                    "reason": reason.strip()
                })
        
        return recommendations

    except Exception as e:
        logger.error(f"OpenAI error: {str(e)}")
        return []

@app.get("/api/search")
async def search(query: str = Query(..., min_length=2, max_length=50)) -> Dict:
    """Search endpoint for date spot recommendations."""
    logger.info(f"Received search request for query: {query}")
    try:
        reddit_api = RedditAPI()
        posts = await reddit_api.search_posts(query)
        recommendations = await generate_recommendations(posts, query)
        
        return {
            "recommendations": recommendations,
            "postCount": len(posts)
        }
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)