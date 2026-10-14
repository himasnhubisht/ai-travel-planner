
from app.graph import app

config = {
    "configurable": {
        "thread_id": "travel-test-rishikesh-001"
    }
}

snapshot = app.get_state(config)
state = snapshot.values

print("Next nodes:", snapshot.next)
print("Approved:", state.get("approved"))
print("Revision count:", state.get("retry_count"))
print("Feedback:", state.get("evaluation_feedback"))
print("Itinerary exists:", bool(state.get("itinerary")))
