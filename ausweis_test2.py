import json
import websocket
import argparse

def on_message(ws, message):
    msg = json.loads(message)
    print(f"Received: {msg}")

    if msg.get("msg") == "ACCESS_RIGHTS":
        cmd = {"cmd": "ACCEPT"}
        ws.send(json.dumps(cmd))
        print(f"Sent: {cmd}")

    elif msg.get("msg") == "ENTER_PIN":
        cmd = {"cmd": "SET_PIN", "value": pin}  # use the globally set PIN
        ws.send(json.dumps(cmd))
        print(f"Sent: {cmd}")

    elif msg.get("msg") == "AUTH":
        if msg.get("result", {}).get("major") == "http://www.bsi.bund.de/ecard/api/1.1/resultmajor#ok":
            print("Authentication successful!")
        else:
            print("Authentication failed!")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    cmd = {"cmd": "RUN_AUTH", "tcTokenURL": tcTokenURL}  # use the globally set URL
    ws.send(json.dumps(cmd))
    print(f"Sent: {cmd}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connect to the OnlineAusweis service')
    parser.add_argument('--pin', required=True, help='the pin to use for authentication')
    parser.add_argument('--url', default='ws://localhost:24727/eID-Client', help='the url to connect to')
    parser.add_argument('--token', default='https://test.governikus-eid.de/DEMO', help='the token url to use')
    args = parser.parse_args()

    global pin
    pin = args.pin
    global tcTokenURL
    tcTokenURL = args.token

    ws = websocket.WebSocketApp(args.url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()