#!/usr/bin/env python3

import sys
import subprocess
import pyttsx3
import speech_recognition as sr


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def command_not_found():
    text = "Command not found"
    engine = pyttsx3.init()
    print(text)
    engine.say(text)
    engine.runAndWait()


def open_app(subprocess_ls, app):
    subprocess_ls.append(subprocess.Popen([app]))


def close_app(subprocess_ls, app):
    for process in subprocess_ls:
        if app.lower() in "".join(process.args).lower():
            try:
                process.terminate()
                process.wait(timeout=1)
                if process.poll() is None:
                    process.kill()
                    process.wait()
                print(f"Closed {app}")
            except OSError as e:
                print(f"Error terminating process {app}: {e}")
    subprocess_ls[:] = [p for p in subprocess_ls if p.poll()]



def close_all(subprocess_ls):
    for process in subprocess_ls:
        try:
            process.terminate()
            process.wait(timeout=1)
            if process.poll() is None:
                process.kill()
                process.wait()
        except OSError as e:
            print(f"Error terminating process: {e}")
    subprocess_ls.clear()


def execute_command(command, subprocess_ls):
    if "open firefox" in command:
        open_app(subprocess_ls, "firefox")
    elif "open notepad" in command:
        open_app(subprocess_ls, "gedit")
    elif "open terminal" in command:
        open_app(subprocess_ls, "gnome-terminal")
    elif "open file manager" in command:
        open_app(subprocess_ls, "nautilus")
    elif "open calculator" in command:
        open_app(subprocess_ls, "gnome-calculator")
    elif "open vlc" in command:
        open_app(subprocess_ls, "vlc")
    elif "open mail" in command:
        open_app(subprocess_ls, "thunderbird")
    elif "close firefox" in command:
        close_app(subprocess_ls, "firefox")
    elif "close notepad" in command:
        close_app(subprocess_ls, "gedit")
    elif "close terminal" in command:
        close_app(subprocess_ls, "gnome-terminal")
    elif "close file manager" in command:
        close_app(subprocess_ls, "nautilus")
    elif "close calculator" in command:
        close_app(subprocess_ls, "gnome-calculator")
    elif "close vlc" in command:
        close_app(subprocess_ls, "vlc")
    elif "close mail" in command:
        close_app(subprocess_ls, "thunderbird")
    elif "close all" in command:
        close_all(subprocess_ls)
    elif "exit" in command:
        sys.exit()
    else:
        command_not_found()


def listen_and_execute():
    recognizer = sr.Recognizer()
    subprocess_ls = []

    while True:
        with sr.Microphone() as mic:
            speak("I listen to commands")
            print("I listen to commands")
            recognizer.adjust_for_ambient_noise(mic)
            audio = recognizer.listen(mic)

        try:
            command = recognizer.recognize_google(audio, language='en-in').lower()
            print(f"You said: {command}")
            speak(f"You said: {command}")
            execute_command(command, subprocess_ls)
        except sr.UnknownValueError:
            print("Failed to recognize audio.")
            speak("Sorry, I couldn't recognize what you said.")
        except sr.RequestError as error:
            print(f"Error sending request: {error}")
            speak("An error occurred while sending the request.")


def main():
    listen_and_execute()


if __name__ == "__main__":
    main()
