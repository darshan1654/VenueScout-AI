import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

AGENT_URL = "https://agent.tinyfish.ai/v1/automation/run-sse"
SEARCH_URL = "https://api.search.tinyfish.ai/"


class TinyFishError(Exception):
    pass


def _headers():
    api_key = os.getenv("TINYFISH_API_KEY")

    if not api_key:
        raise TinyFishError(
            "TINYFISH_API_KEY is missing. Check your .env file."
        )

    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }


def research_website(website_url: str, goal: str) -> dict:
    """Run a TinyFish browser task and return its final result."""

    try:
        with requests.post(
            AGENT_URL,
            headers=_headers(),
            json={
                "url": website_url,
                "goal": goal,
                "browser_profile": "lite",
            },
            stream=True,
            timeout=(20, 240),
        ) as response:
            response.raise_for_status()

            final_result = None
            final_status = None
            final_error = None

            #for line in response.iter_lines(decode_unicode=True):
            for line in response.iter_lines():
                
                if isinstance(line, bytes):
                    line = line.decode("utf-8", errors="replace")

                if not line:
                    continue

                if line.startswith("data:"):
                    raw_data = line[len("data:"):].strip()

                    if not raw_data:
                        continue

                    try:
                        event = json.loads(raw_data)
                    except json.JSONDecodeError:
                        continue

                    event_type = event.get("type")

                    if event_type == "STREAMING_URL":
                        print(
                            "Live browser:",
                            event.get("streaming_url")
                            or event.get("streamingUrl")
                            or "",
                        )

                    elif event_type == "PROGRESS":
                        print(
                            "TinyFish:",
                            event.get("purpose", "Working"),
                        )

                    elif event_type == "COMPLETE":
                        final_status = event.get("status")
                        final_result = (
                            event.get("resultJson")
                            or event.get("result")
                        )
                        final_error = event.get("error")

            if final_status and final_status.upper() not in {
                "COMPLETED", "COMPLETE", "SUCCESS"
            }:
                raise TinyFishError(
                    f"TinyFish status: {final_status}. "
                    f"Details: {final_error}"
                )

            if final_result is None:
                raise TinyFishError(
                    "No final result received from TinyFish."
                )

            if isinstance(final_result, str):
                try:
                    final_result = json.loads(final_result)
                except json.JSONDecodeError:
                    return {"raw_result": final_result}

            if isinstance(final_result, dict):
                return final_result

            return {"raw_result": final_result}

    except requests.RequestException as exc:
        raise TinyFishError(f"TinyFish request failed: {exc}") from exc


def search_web(query: str) -> dict:
    """Search for candidate websites using TinyFish Search."""

    try:
        response = requests.get(
            SEARCH_URL,
            headers=_headers(),
            params={"query": query},
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        raise TinyFishError(f"Venue search failed: {exc}") from exc
