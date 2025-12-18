import json
import os
import pandas as pd
from datetime import datetime

DATA_FILE = "votes.json"

class DataManager:
    def __init__(self, file_path=DATA_FILE):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            initial_data = {
                "votes": []
            }
            with open(self.file_path, "w") as f:
                json.dump(initial_data, f)

    def load_votes(self):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            return data.get("votes", [])
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_vote(self, category, candidate, voter_name=None):
        votes = self.load_votes()
        new_vote = {
            "category": category,
            "candidate": candidate,
            "timestamp": datetime.now().isoformat(),
            "voter": voter_name  # Optional, if we want to track who voted
        }
        votes.append(new_vote)
        
        with open(self.file_path, "w") as f:
            json.dump({"votes": votes}, f, indent=4)
        
        return True

    def get_candidates(self, category):
        """Get unique list of candidates already voted for in a category for autocomplete"""
        votes = self.load_votes()
        candidates = set()
        for vote in votes:
            if vote["category"] == category:
                candidates.add(vote["candidate"])
        return sorted(list(candidates))

    def get_results_df(self):
        votes = self.load_votes()
        if not votes:
            return pd.DataFrame(columns=["Category", "Candidate", "Count"])
        
        df = pd.DataFrame(votes)
        # Group by category and candidate to get counts
        results = df.groupby(["category", "candidate"]).size().reset_index(name="count")
        results.columns = ["Category", "Candidate", "Count"]
        return results

