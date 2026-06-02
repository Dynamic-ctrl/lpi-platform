import json
import random
import httpx
from pathlib import Path

# Configuration
JSON_PATH = Path("data/intern_profiles.json") 
API_URL = "http://localhost:8000/api/v1/goals/"

SMILE_PHASES = ["sense", "model", "intervene", "learn", "evolve"]

def main():
    if not JSON_PATH.exists():
        print(f"❌ Error: Could not find '{JSON_PATH}'. Run this from the root directory.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as file:
        profiles = json.load(file)

    print(f"Found {len(profiles)} profiles. Starting seed process...\n")
    success_count = 0

    # Using httpx to POST to the local API
    with httpx.Client() as client:
        for profile in profiles:
            # 1. Extract Title (first goal in the array)
            goals = profile.get("goals", [])
            if not goals:
                continue
            title = goals[0]

            # 2. Extract Description (remaining goals + interests)
            remaining_goals = goals[1:]
            interests = profile.get("interests", [])
            description_parts = remaining_goals + interests
            description = ". ".join(description_parts) + "." if description_parts else ""

            # 3. Generate missing fields to guarantee diversity
            priority = random.randint(3, 9)
            smile_phase = random.choice(SMILE_PHASES)

            # 4. Construct GoalCreate payload
            payload = {
                "title": title,
                "description": description,
                "priority": priority,
                "smile_phase": smile_phase
            }

            # 5. POST to API
            try:
                response = client.post(API_URL, json=payload)
                if response.status_code == 201:
                    print(f"✅ Created: '{title[:35]}...' | Priority: {priority} | Phase: {smile_phase}")
                    success_count += 1
                else:
                    print(f"⚠️ Failed: {title} | Status: {response.status_code} | Error: {response.text}")
            except httpx.ConnectError:
                print("❌ Connection Error: Is your FastAPI server running on port 8000?")
                break

    print(f"\n🎉 Seeding complete! {success_count}/{len(profiles)} goals successfully added.")

if __name__ == "__main__":
    main()