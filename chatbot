from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from textblob import TextBlob

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI key

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a mental health support AI. Be empathetic and supportive."},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

@app.route("/mood", methods=["POST"])
def mood_analysis():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    analysis = TextBlob(user_message)
    mood = "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"
    return jsonify({"mood": mood})

@app.route("/recommend", methods=["POST"])
def recommend_help():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    analysis = TextBlob(user_message)
    if analysis.sentiment.polarity < -0.5:
        recommendation = "You may want to consult a psychologist for support."
    else:
        recommendation = "You're doing great! Keep practicing self-care."
    
    return jsonify({"recommendation": recommendation})

if __name__ == "__main__":
    app.run(debug=True)
