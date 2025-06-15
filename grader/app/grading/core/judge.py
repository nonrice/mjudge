import requests

def judge_code(submission_id):
    # We'll just send an AC post request to the backend
    
    url = "http://127.0.0.1:5001/api/verdict"
    payload = {
        "submission_id": submission_id,
        "verdict": "Accepted",
        "time_used": 100,
        "memory_used": 256
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code, response.reason)