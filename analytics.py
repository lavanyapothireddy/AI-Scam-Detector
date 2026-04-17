analytics = {
    "total": 0,
    "scam": 0,
    "safe": 0,
    "suspicious": 0,
    "history": []
}

def update_analytics(result, text):
    analytics["total"] += 1

    label = result["label"]

    if label == "Scam":
        analytics["scam"] += 1
    elif label == "Safe":
        analytics["safe"] += 1
    else:
        analytics["suspicious"] += 1

    analytics["history"].append({
        "text": text[:50],
        "label": label,
        "confidence": result["confidence"]
    })

    # keep only last 20
    analytics["history"] = analytics["history"][-20:]

def get_analytics():
    return analytics