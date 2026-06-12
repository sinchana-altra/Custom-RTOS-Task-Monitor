import serial
import struct
import threading

TASK_FMT  = "=16sBBIII"
TASK_SIZE = struct.calcsize(TASK_FMT)
HEADER    = 0xAB

STATES = ["Running", "Ready", "Blocked", "Suspended", "Deleted"]

def parse_task(raw: bytes) -> dict:
    name, prio, state, hwm, ticks, tid = struct.unpack(TASK_FMT, raw)
    return {
        "name":      name.decode(errors="replace").rstrip("\x00"),
        "priority":  prio,
        "state":     STATES[state] if state < len(STATES) else "Unknown",
        "stack_hwm": hwm,
        "cpu_ticks": ticks,
        "id":        tid,
    }

def read_serial(port: str, baud: int, callback):
    with serial.Serial(port, baud, timeout=2) as ser:
        while True:
            byte = ser.read(1)
            if not byte or byte[0] != HEADER:
                continue
            count_b = ser.read(1)
            if not count_b:
                continue
            count = count_b[0]
            raw = ser.read(count * TASK_SIZE)
            if len(raw) < count * TASK_SIZE:
                continue
            tasks = [parse_task(raw[i*TASK_SIZE:(i+1)*TASK_SIZE]) for i in range(count)]
            callback(tasks)

def start_reader(port="/dev/ttyUSB0", baud=115200, callback=print):
    t = threading.Thread(target=read_serial, args=(port, baud, callback), daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    import time
    def on_tasks(tasks):
        print("\n--- Task snapshot ---")
        for t in tasks:
            print(f"  {t['name']:16s} {t['state']:10s} prio={t['priority']} hwm={t['stack_hwm']}")

    start_reader("/dev/ttyUSB0", 115200, on_tasks)
    while True:
        time.sleep(1)
