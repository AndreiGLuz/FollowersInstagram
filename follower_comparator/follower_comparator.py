from typing import List


class FollowerComparator:
    @staticmethod
    def find_new_followers(previous_list: List[str], current_list: List[str]) -> List[str]:
        """Finds new followers by comparing two lists."""
        new_followers = list(set(current_list).difference(previous_list))
        return sorted(new_followers)
