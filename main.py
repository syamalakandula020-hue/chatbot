from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai


client = genai.Client(api_key="AIzaSyDmjrtQIOZdGYWKmTjybwNLDbXayw8")
model_id = "gemini-2.5-flash-lite"


app = Flask(__name__)
CORS(app)  # Enable CORS for local development

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        prompt = request.json["message"]
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config={
                "system_instruction": "Your name is Syamala. You are a highly intelligent and friendly science assistant. You MUST ONLY answer questions related to science (Physics, Chemistry, Biology, Astronomy, Earth Science, etc.). If a question is NOT related to science, politely inform the user that you only specialize in scientific topics. Keep responses very short (1-2 sentences) so they sound natural when spoken. Use LaTeX for formulas."
            }
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tts", methods=["POST"])
def tts():
    try:
        text = request.json["text"]
        # Clean text for TTS
        clean_text = text.replace('$', '').replace('#', '').replace('*', '').replace('`', '')[:500]
        
        response = client.models.generate_content(
            model=model_id,
            contents=f"Say clearly and concisely: {clean_text}",
            config={
                "response_modalities": ["AUDIO"],
                "speech_config": {
                    "voice_config": {
                        "prebuilt_voice_config": {
                            "voice_name": "Aoede"
                        }
                    }
                }
            }
        )
        
        # Extract PCM audio data
        if response.candidates and len(response.candidates) > 0:
            parts = response.candidates[0].content.parts
            if parts and len(parts) > 0 and hasattr(parts[0], 'inline_data'):
                pcm_data = parts[0].inline_data.data
                return jsonify({"pcm": pcm_data})
        
        return jsonify({"error": "No audio data received"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    app.run(port=8001, debug=True)

