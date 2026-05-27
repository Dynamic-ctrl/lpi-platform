import json
from pydantic import ValidationError

from models import GoalCreate, SignalCreate, SmilePhase

def test_proxy_ingestion(filepath: str):
    print(f"Loading proxy data from {filepath}...")
    
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}. Make sure the path is correct.")
        return
    
    interns = data
    valid_goals = 0
    valid_signals = 0
    errors = 0
    
    for intern in interns:
        name = intern.get("name", "Unknown Intern")
        
        # --- 1. VALIDATE GOALS ---
        # A. 3-Year Goals
        for goal_text in intern.get("goals", []):
            try:
                goal = GoalCreate(
                    title=f"Aspiration: {name}",
                    description=goal_text,
                    priority=9,
                    smile_phase=SmilePhase.SENSE  
                )
                valid_goals += 1
            except ValidationError as e:
                print(f"Error validating 3-year goal for {name}: {e}")
                errors += 1
                
        # B. Combined Interests Goal
        interests = intern.get("interests", [])
        if interests:
            try:
                combined_goal = GoalCreate(
                    title="Explore Core Interests",
                    description=f"Interests include: {', '.join(interests)}",
                    priority=6,
                    smile_phase=SmilePhase.SENSE  
                )
                valid_goals += 1
            except ValidationError as e:
                print(f"Error validating interest goal for {name}: {e}")
                errors += 1

        # --- 2. VALIDATE SIGNALS ---
        # A. Skills
        for skill in intern.get("skills", []):
            try:
                signal = SignalCreate(
                    stream="intern_proxy",
                    event_type="skill_demonstrated",
                    payload={"skill": skill}
                )
                valid_signals += 1
            except ValidationError as e:
                print(f"Error validating skill signal for {name}: {e}")
                errors += 1
                
        # B. Interests
        for interest in interests:
            try:
                signal = SignalCreate(
                    stream="intern_proxy",
                    event_type="interest_identified",
                    payload={"interest": interest}
                )
                valid_signals += 1
            except ValidationError as e:
                print(f"Error validating interest signal for {name}: {e}")
                errors += 1

    print("\n--- Validation Summary ---")
    print(f"Goals Validated: {valid_goals}")
    print(f"Signals Validated: {valid_signals}")
    print(f"Validation Errors: {errors}")

if __name__ == "__main__":
    # Update this path to point to your actual JSON file
    test_proxy_ingestion("../../data/intern_profiles.json")