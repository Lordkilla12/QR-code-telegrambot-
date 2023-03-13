import qrcode
import requests
import json
import time

from PIL import Image

TOKEN = "5840286193:AAGRhqaFOAZE7x-FjWioctCLhpUTCUi6S2w"

def get_updates():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    return response.json()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
    requests.get(url)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")

processed_messages = set()

def handle_updates(updates):
    for update in updates["result"]:
        if "message" in update:
            if "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"]
                if text not in processed_messages:
                    processed_messages.add(text)
                    generate_qr_code(text)
                    with open("qr_code.png", "rb") as f:
                        requests.post(
                            f"https://api.telegram.org/bot{TOKEN}/sendPhoto",
                            files={"photo": f},
                            data={"chat_id": chat_id}
                        )






if __name__ == "__main__":
    updates = get_updates()
    handle_updates(updates)



if __name__ == "__main__":
    while True:
        updates = get_updates()
        handle_updates(updates)
        time.sleep(5)


