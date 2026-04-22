from flask import Flask, request, jsonify, render_template
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔐 Get API key from environment
API_KEY = os.getenv("MODELSLAB_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "")

        # 🔥 Improve prompt quality automatically
        enhanced_prompt = f"""
        ultra detailed cinematic planet, {user_prompt},
        glowing atmosphere, space background,
        4k, highly realistic, sci-fi, dramatic lighting
        """

        url = "https://modelslab.com/api/v6/images/text2img"

        payload = {
            "key": API_KEY,
            "prompt": enhanced_prompt,
            "width": "512",
            "height": "512",
            "samples": "1",
            "num_inference_steps": "20",
            "guidance_scale": 7.5
        }

        response = requests.post(url, json=payload)
        result = response.json()

        # ✅ Handle success
        if "output" in result and len(result["output"]) > 0:
            return jsonify({"image": result["output"][0]})

        # ❌ Handle failure
        return jsonify({"error": result}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()