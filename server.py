from flask import Flask, render_template
from flask_socketio import SocketIO
from serial_reader import start_reader
import threading

app = Flask(__name__, template_folder="../frontend")
sio = SocketIO(app, cors_allowed_origins="*")

latest_tasks = []

def on_tasks(tasks):
    global latest_tasks
    latest_tasks = tasks
    sio.emit("task_update", tasks)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks")
def api_tasks():
    return {"tasks": latest_tasks}

if __name__ == "__main__":
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
    print(f"Listening on {port} ...")
    start_reader(port, 115200, on_tasks)
    sio.run(app, host="0.0.0.0", port=5000, debug=False)
