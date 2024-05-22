import speech_recognition as sr
import json
import threading
import msvcrt

def listen_and_recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio_data = r.record(source, duration=20)
        print("Recognizing...")
        text = r.recognize_google(audio_data)
        print(text)

        try:
            with open('recognized_eng_text.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {"text": []}

        data["text"].append(text)

        with open('recognized_eng_text.json', 'w') as f:
            json.dump(data, f)

while True:
    listen_thread = threading.Thread(target=listen_and_recognize)
    listen_thread.start()

    print("Press Enter to stop listening...")
    while True:
        if msvcrt.kbhit() and msvcrt.getch() in [b'\r', b'\n']:
            break

    listen_thread.join()

    continue_listening = input("Do you want to continue listening? (yes/no): ")
    if continue_listening.lower() != "yes":
        break