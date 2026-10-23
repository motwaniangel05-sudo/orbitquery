import requests
from django.conf import settings
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class LaunchLibrary2Client:
    def __init__(self):
        self.base_url = settings.LL2_API_URL
        self.timeout = 30

    def get_launches(
        self,
        limit: int = 100,
        offset: int = 0,
        mode: str = 'detailed'
    ) -> Dict:
        url = f"{self.base_url}/launch/"
        params = {
            'limit': limit,
            'offset': offset,
            'mode': mode,
        }
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching launches: {e}")
            raise

    def get_launch(self, launch_id: str) -> Optional[Dict]:
        url = f"{self.base_url}/launch/{launch_id}/"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching launch {launch_id}: {e}")
            return None
