import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

# Set up basic logging
logger = logging.getLogger(__name__)


def get_http_session() -> requests.Session:
    """
    Creates a requests Session with automatic retries and exponential backoff.
    """
    session = requests.Session()

    # Define retry strategy: retry 3 times, backoff factor of 1 (1s, 2s, 4s)
    # Retry on common transient errors: 429 (Too Many Requests) and 500/502/503/504
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    # Mount the adapter to both HTTP and HTTPS
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def fetch_json(url: str, params: dict = None, timeout: int = 10) -> dict:
    """
    Fetches JSON from a URL with retries and a strict timeout.
    """
    session = get_http_session()
    logger.info(f"Fetching URL: {url}")

    try:
        # We enforce a timeout (connect timeout, read timeout)
        response = session.get(url, params=params, timeout=timeout)
        response.raise_for_status()  # Raises an exception for 4xx/5xx errors
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Request failed: {e}")
        raise
