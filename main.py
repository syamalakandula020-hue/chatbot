from flask import Flask,request,jsonify,render_template
from google import genai

client=genai.Client(api_key="SECRET_KEY")

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/chat",methods=["POST"])
def chat():
    prompt=request.json["message"]
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "system_instruction": "Your name is Syamala. You are a highly intelligent and friendly science assistant. You MUST ONLY answer questions related to science (Physics, Chemistry, Biology, Astronomy, Earth Science, etc.). If a question is NOT related to science, politely inform the user that you only specialize in scientific topics. Keep responses very short (1-2 sentences) so they sound natural when spoken. Use LaTeX for formulas."
        }
    )
    return jsonify({"reply":response.text})
if __name__ == '__main__':
    app.run(port=8000)