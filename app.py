from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def classify(msg):
    msg = msg.lower()

    if any(x in msg for x in ["suicide", "kill myself", "want to die", "hurt myself", "self harm"]):
        return "urgent_help"

    if any(x in msg for x in ["overwhelmed", "too much", "can't handle", "cannot handle", "everything at once"]):
        return "overwhelmed"

    if any(x in msg for x in ["anxious", "anxiety", "panic", "worried", "nervous", "overthinking"]):
        return "anxious"

    if any(x in msg for x in ["sad", "lonely", "cry", "crying", "empty", "down"]):
        return "sad"

    if any(x in msg for x in ["motivation", "unmotivated", "lazy", "procrastinate", "can't focus", "no energy"]):
        return "motivation"

    return "stressed"

@app.route("/")
def home():
    return "Mental health API is running."

@app.route("/classify", methods=["POST"])
def classify_api():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    category = classify(message)

    replies = {
        "stressed": "It sounds like you're feeling stressed. Let's slow things down.",
        "anxious": "It sounds like you're feeling anxious. Take a deep breath with me.",
        "sad": "I'm sorry you're feeling this way. You're not alone.",
        "overwhelmed": "It sounds like things feel like too much right now. Let's take one step at a time.",
        "motivation": "It seems like you're struggling with motivation. Starting small is okay.",
        "urgent_help": "It sounds serious. Please reach out to emergency support or someone you trust right now."
    }

    return jsonify({
        "category": category,
        "reply": replies[category]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)