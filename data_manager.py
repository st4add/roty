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
                "votes": [],
                "settings": {
                    "results_locked": False
                }
            }
            with open(self.file_path, "w") as f:
                json.dump(initial_data, f, indent=4)
        else:
            # Migration: Ensure settings key exists in existing file
            data = self._read_all()
            if "settings" not in data:
                data["settings"] = {"results_locked": False}
                self._write_all(data)

    def _read_all(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"votes": [], "settings": {"results_locked": False}}

    def _write_all(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def load_votes(self):
        return self._read_all().get("votes", [])

    def save_vote(self, category, candidate, voter_name):
        data = self._read_all()
        new_vote = {
            "category": category,
            "candidate": candidate,
            "timestamp": datetime.now().isoformat(),
            "voter": voter_name 
        }
        data["votes"].append(new_vote)
        self._write_all(data)
        return True

    def clear_votes(self):
        """Clears all votes but preserves settings"""
        data = self._read_all()
        data["votes"] = []
        self._write_all(data)
        return True

    def delete_votes_for_voter(self, voter_name: str) -> int:
        """Delete ALL votes cast by a specific voter. Returns the number of deleted votes."""
        data = self._read_all()
        votes = data.get("votes", [])
        if not votes:
            return 0

        remaining = [v for v in votes if v.get("voter") != voter_name]
        deleted_count = len(votes) - len(remaining)
        
        data["votes"] = remaining
        self._write_all(data)

        return deleted_count

    def get_settings(self):
        """Get application settings"""
        return self._read_all().get("settings", {"results_locked": False})

    def update_settings(self, new_settings):
        """Update application settings"""
        data = self._read_all()
        data["settings"] = new_settings
        self._write_all(data)
        return True

    def list_voters(self):
        """Return sorted unique voter names that have cast at least one vote."""
        votes = self.load_votes()
        voters = sorted({v.get("voter") for v in votes if v.get("voter")})
        return voters

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

    def has_voted(self, voter_name):
        """Check if a voter has already cast any votes"""
        votes = self.load_votes()
        for vote in votes:
            if vote.get("voter") == voter_name:
                return True
        return False

    def get_voter_stats(self):
        """Get stats on who has voted"""
        votes = self.load_votes()
        if not votes:
            return pd.DataFrame(columns=["Voter", "Votes Cast", "Last Voted"])
        
        df = pd.DataFrame(votes)
        if "voter" not in df.columns:
             return pd.DataFrame(columns=["Voter", "Votes Cast", "Last Voted"])
             
        # Group by voter
        stats = df.groupby("voter").agg({
            "category": "count",
            "timestamp": "max"
        }).reset_index()
        
        stats.columns = ["Voter", "Votes Cast", "Last Voted"]
        
        # Format timestamp for better readability
        stats["Last Voted"] = pd.to_datetime(stats["Last Voted"]).dt.strftime('%Y-%m-%d %H:%M')
        
        return stats.sort_values("Last Voted", ascending=False)
