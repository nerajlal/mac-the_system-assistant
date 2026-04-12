from flask import Flask, render_template, jsonify, request
import logging
from assistant import memory

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
        # Clear logs on manual toggle to keep it fresh
        assistant_state["last_heard"] = ""
        assistant_state["last_spoken"] = ""
    return jsonify(assistant_state)

    return jsonify({"status": "snoozed", "duration_minutes": 5})

@app.route("/api/memories", methods=["GET"])
def get_memories():
    """Returns all stored facts about the user."""
    memories = memory.get_all_memories()
    return jsonify(memories)

@app.route("/api/memories/<key>", methods=["DELETE"])
def remove_memory(key):
    """Deletes a specific memory."""
    memory.delete_memory(key)
    return jsonify({"status": "success", "deleted": key})

def run_server():
    # Run the web server quietly on port 5050
    app.run(host="0.0.0.0", port=5050, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_server()
