
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool
import logging
load_dotenv()

logger=logging.getLogger(__name__)

tavily = TavilyClient(
    api_key=os.environ["TAVILY_API_KEY"]
)


@tool
def web_search(query: str) -> list[dict]:
    """
    Search the web for travel-related information such as
    transport options, accommodation, attractions, prices,
    and activities.

    Input should be a specific search query.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    try:
        response = tavily.search(
            query=query,
            max_results=5,
        )
    except Exception as e:
        logger.exception("Tavily search failed")
        raise

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
        })

    return results
