import json
import websocket

def on_message(ws, message):
    msg = json.loads(message)
    print(f"Received: {msg}")

    if msg.get("msg") == "ACCESS_RIGHTS":
        cmd = {"cmd": "ACCEPT"}
        ws.send(json.dumps(cmd))
        print(f"Sent: {cmd}")

    elif msg.get("msg") == "ENTER_PIN":
        cmd = {"cmd": "SET_PIN", "value": "123456"}  # replace with actual PIN
        ws.send(json.dumps(cmd))
        print(f"Sent: {cmd}")

    elif msg.get("msg") == "AUTH":
        if msg.get("result", {}).get("major") == "http://www.bsi.bund.de/ecard/api/1.1/resultmajor#ok":
            print("Authentication successful!")
        else:
            print("Authentication failed!")

def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, status_code, reason):
    print(f"Connection closed with status code {status_code} and reason {reason}")

def on_open(ws):
    cmd = {"cmd": "RUN_AUTH", "tcTokenURL": "https://127.0.0.1:24727/eID-Client?tcTokenURL=", "developerMode": True, "status": True}
    #cmd = {"cmd": "RUN_AUTH", "tcTokenURL": "https://test.governikus-eid.de/DEMO"}
    #cmd = {"cmd": "RUN_AUTH", "tcTokenURL": "https://test.governikus-eid.de/AusweisAuskunft/WebServiceReq"}
    ws.send(json.dumps(cmd))
    print(f"Sent: {cmd}")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:24727/eID-Kernel",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
