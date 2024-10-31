import os
import json

data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

def load_history(user_id):
    """Load user chat history from JSON file."""
    history_file = os.path.join(data_folder, f"{user_id}_history.json")
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []

def save_history(user_id, message):
    """Save user chat history to JSON file."""
    history = load_history(user_id)
    history.append(message)
    history_file = os.path.join(data_folder, f"{user_id}_history.json")
    with open(history_file, 'w') as file:
        json.dump(history, file)
