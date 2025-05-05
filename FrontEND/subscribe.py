import requests
from datetime import datetime, timedelta

BACKEND_URL = "https://kivyapp.onrender.com"  # Update if needed
subscription_prices = {
    "hour": 10,
    "day": 50,
    "month": 500,
    "6month": 2000
}


def get_subscription_end_time(plan):
    now = datetime.utcnow()
    if plan == "hour":
        return now + timedelta(hours=1)
    elif plan == "day":
        return now + timedelta(days=1)
    elif plan == "month":
        return now + timedelta(days=30)
    elif plan == "6month":
        return now + timedelta(days=180)
    return now


def subscribe_user(user_id, plan):
    if plan not in subscription_prices:
        return {"status": "error", "message": "Invalid plan"}
    end_time = get_subscription_end_time(plan)
    payload = {
        "user_id": user_id,
        "plan": plan,
        "start_time": datetime.utcnow().isoformat(),
        "end_time": end_time.isoformat()
    }
    try:
        response = requests.post(f"{BACKEND_URL}/subscribe", json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
