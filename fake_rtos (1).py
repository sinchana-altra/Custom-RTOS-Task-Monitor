"""
Run this instead of serial_reader.py to simulate RTOS data
without real hardware. Feeds fake tasks into the server.
"""
import time
import random

TASKS = [
    {"name": "SensorTask",  "priority": 3, "base_state": "Blocked"},
    {"name": "CommsTask",   "priority": 5, "base_state": "Running"},
    {"name": "ControlTask", "priority": 4, "base_state": "Ready"},
    {"name": "LoggerTask",  "priority": 1, "base_state": "Sleeping"},
    {"name": "IdleTask",    "priority": 0, "base_state": "Running"},
]

STATES = ["Running", "Ready", "Blocked", "Suspended"]

def simulate(callback, interval=0.5):
    ticks = {t["name"]: 0 for t in TASKS}
    while True:
        snapshot = []
        for t in TASKS:
            ticks[t["name"]] += random.randint(10, 500)
            snapshot.append({
                "name":      t["name"],
                "priority":  t["priority"],
                "state":     random.choice(STATES),
                "stack_hwm": random.randint(64, 2048),
                "cpu_ticks": ticks[t["name"]],
                "id":        TASKS.index(t),
            })
        callback(snapshot)
        time.sleep(interval)

if __name__ == "__main__":
    def show(tasks):
        print("\n".join(f"{t['name']:16s} {t['state']}" for t in tasks))
        print("---")
    simulate(show)
