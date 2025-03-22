from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from textblob import TextBlob
from dotenv import load_dotenv  # Import dotenv
import os  # Import os to access env variables

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
print("OpenAI API Key:", openai.api_key)

# if not openai.api_key:
#     raise ValueError("⚠️ Missing OpenAI API key! Add it to the .env file.")
app = Flask(__name__)
CORS(app)  # Enables CORS for frontend communication
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Mental Health AI Chatbot!"})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a mental health support AI. Be empathetic and supportive."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500

    return jsonify({"reply": reply})

@app.route("/mood", methods=["POST"])
def mood_analysis():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    analysis = TextBlob(user_message)
    polarity = analysis.sentiment.polarity

    if polarity > 0.3:
        mood = "Positive 😊"
    elif polarity < -0.3:
        mood = "Negative 😞"
    else:
        mood = "Neutral 😐"

    return jsonify({"mood": mood, "score": polarity})

@app.route("/recommend", methods=["POST"])
def recommend_help():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    analysis = TextBlob(user_message)
    polarity = analysis.sentiment.polarity

    if polarity < -0.6:
        recommendation = "It might help to talk to a therapist. You're not alone. 💙"
    elif polarity < -0.3:
        recommendation = "Try practicing mindfulness or talking to a friend. 🧘‍♂️"
    elif polarity > 0.3:
        recommendation = "Keep up the positivity! Maybe write down what made you happy today. 🌟"
    else:
        recommendation = "You're doing okay! Keep checking in with yourself. 🤗"

    return jsonify({"recommendation": recommendation, "score": polarity})

if __name__ == "__main__":
    app.run(debug=True)
