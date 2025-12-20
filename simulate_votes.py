import time
import random
from data_manager import DataManager
import utils

def simulate_voting_session():
    dm = DataManager()
    
    print("🚀 Starting Vote Simulation...")
    print("--------------------------------")

    # List of categories
    categories = ["Ranelad of the Year", "Worst Ranelad of the Year", "Most Improved Ranelad"]
    
    # Selection of potential voters (using the real list)
    voters = utils.RANELADS.copy()
    random.shuffle(voters)
    
    # Simulated devices and IPs
    devices = ["iPhone", "Android Phone", "iPad", "Mac Desktop", "Windows Desktop"]
    
    # We'll simulate 10 people voting
    num_simulated_voters = min(10, len(voters))
    
    for i in range(num_simulated_voters):
        voter = voters[i]
        
        # Clean the name for logic (remove emojis if present)
        voter_base = voter.replace(" 👑", "").replace(" 💩💩", "").strip()
        
        print(f"👤 {voter} is entering the booth...")
        
        # Simulated metadata
        metadata = {
            "ip": f"192.168.1.{random.randint(10, 254)}",
            "user_agent": random.choice(devices),
            "raw_ua": "Simulated/1.0"
        }
        
        # Pick random candidates (but not themselves)
        candidates = [r for r in utils.RANELADS if r != voter]
        
        for category in categories:
            choice = random.choice(candidates)
            dm.save_vote(category, choice, voter, metadata=metadata)
            print(f"   ✅ Voted for {choice} in '{category}'")
            
            # Small realistic delay between category selections
            time.sleep(random.uniform(0.5, 1.5))
            
        print(f"🏁 {voter} has submitted their ballot.\n")
        
        # Wait a few seconds before the next person "arrives"
        if i < num_simulated_voters - 1:
            wait_time = random.randint(2, 5)
            print(f"--- Waiting {wait_time}s for next voter... ---\n")
            time.sleep(wait_time)

    print("--------------------------------")
    print("✅ Simulation Complete! Check your Live Leaderboard and Voter Log.")

if __name__ == "__main__":
    simulate_voting_session()

