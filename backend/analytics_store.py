from datetime import datetime

store = {
    "total": 0,
    "scam": 0,
    "safe": 0,
    "suspicious": 0,
    "history": []
}

def log_prediction(result, text):
    store["total"] += 1

    label = result["label"]

    if label == "Scam":
        store["scam"] += 1
    elif label == "Safe":
        store["safe"] += 1
    else:
        store["suspicious"] += 1

    store["history"].append({
        "text": text[:60],
        "label": label,
        "confidence": result["confidence"],
        "time": datetime.now().strftime("%H:%M:%S")
    })

    store["history"] = store["history"][-30:]
