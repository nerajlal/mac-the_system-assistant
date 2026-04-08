from flask import Flask, render_template, jsonify, request
import logging

# We will use this module-level variable to communicate between the web server and the main assistant loop.
# True = Assistant is listening. False = Assistant ignores microphone.
assistant_state = {
    "is_active": True,
    "last_spoken": "",
    "last_heard": "",
    "api_active": False
}

app = Flask(__name__)

# Reduce Flask logging spam
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    from assistant.llm_engine import model, GEMINI_API_KEY
    assistant_state["api_active"] = (model is not None and GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE")
    return jsonify(assistant_state)

@app.route("/api/toggle", methods=["POST"])
def toggle_status():
    data = request.json
    if "is_active" in data:
        assistant_state["is_active"] = data["is_active"]
    return jsonify(assistant_state)

def run_server():
    # Run the web server quietly on port 5050
    app.run(host="0.0.0.0", port=5050, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_server()
