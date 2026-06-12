# RTOS Task Monitor

A real-time web dashboard that monitors FreeRTOS tasks over UART/USB.

## Structure
```
firmware/   → C code for your MCU (FreeRTOS hooks + UART sender)
backend/    → Python serial reader + Flask/SocketIO server
frontend/   → Web dashboard (HTML + Chart.js)
simulator/  → Fake RTOS data generator (no hardware needed)
```

## Quick Start (no hardware)

```bash
cd backend
pip install -r requirements.txt

# Start the fake simulator + server
python server.py --simulate
```

Open http://localhost:5000

## With Real Hardware

1. Add `FreeRTOSConfig_snippet.h` lines to your `FreeRTOSConfig.h`
2. Add `monitor_hooks.c` and `serial_sender.c` to your firmware project
3. Flash to your MCU
4. Run:

```bash
python backend/server.py /dev/ttyUSB0
```

## Hardware
- Any MCU running FreeRTOS (STM32, ESP32, Arduino, etc.)
- USB-to-UART adapter or built-in USB

## License
MIT
