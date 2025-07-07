import json
from typing import List, Optional


class FollowersRepository:
    @staticmethod
    def load_followers(file_path: str) -> Optional[List[str]]:
        """Loads the followers list from a JSON file."""
        try:
            with open(file_path) as file:
                followers_data = json.load(file)
                followers = [
                    follower["string_list_data"][0]["value"]
                    for follower in followers_data
                ]
                return sorted(followers)
        except Exception:
            return None
