import json
import websocket

def on_message(ws, message):
    msg = json.loads(message)
    print(f"Received: {msg}")

def on_open(ws):
    cmd = {"cmd": "RUN_AUTH", "tcTokenURL": "https://test.governikus-eid.de/DEMO"}
    ws.send(json.dumps(cmd))
    print(f"Sent: {cmd}")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:24727/eID-Kernel",
                                on_open=on_open,
                                on_message=on_message)
    ws.run_forever()
