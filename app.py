from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def classify(msg: str) -> str:
    msg = str(msg).lower().strip()

    if not msg:
        return "stressed"

    urgent_keywords = [
        "suicide", "kill myself", "want to die", "hurt myself",
        "self harm", "self-harm", "i am not safe", "not safe",
        "end my life", "die"
    ]

    overwhelmed_keywords = [
        "overwhelmed", "too much", "can't handle", "cannot handle",
        "everything at once", "too many things", "i can't cope",
        "so much work", "too much pressure"
    ]

    anxious_keywords = [
        "anxious", "anxiety", "panic", "panicking", "worried",
        "nervous", "overthinking", "fear", "scared", "stress out"
    ]

    sad_keywords = [
        "sad", "lonely", "cry", "crying", "empty", "down",
        "heartbroken", "upset", "depressed", "unhappy"
    ]

    motivation_keywords = [
        "motivation", "motivated", "unmotivated", "lazy",
        "procrastinate", "procrastinating", "can't focus",
        "cannot focus", "no energy", "need motivation",
        "i need motivation"
    ]

    stressed_keywords = [
        "stressed", "stress", "pressure", "busy", "tired",
        "exhausted", "burnt out", "burned out", "deadline",
        "workload"
    ]

    if any(keyword in msg for keyword in urgent_keywords):
        return "urgent_help"

    if any(keyword in msg for keyword in overwhelmed_keywords):
        return "overwhelmed"

    if any(keyword in msg for keyword in anxious_keywords):
        return "anxious"

    if any(keyword in msg for keyword in sad_keywords):
        return "sad"

    if any(keyword in msg for keyword in motivation_keywords):
        return "motivation"

    if any(keyword in msg for keyword in stressed_keywords):
        return "stressed"

    return "stressed"


@app.route("/")
def home():
    return "Mental health API is running."


@app.route("/classify", methods=["POST"])
def classify_api():
    try:
        data = request.get_json(silent=True) or {}

        message = data.get("message", "")
        if message is None:
            message = ""

        message = str(message).strip()
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
            "received_message": message,
            "category": category,
            "reply": replies[category]
        })

    except Exception as e:
        return jsonify({
            "received_message": "",
            "category": "stressed",
            "reply": "It sounds like you're feeling stressed. Let's slow things down.",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)