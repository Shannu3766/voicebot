import speech_recognition as sr
import socket
from gtts import gTTS
import os
import pygame
import time

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
    except Exception as e:
        print("say that again please.....")
        return "None"
    return query

def speak(text, count):
    tts = gTTS(text=text, lang='en')
    filename = f"response{count}.mp3"
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    pygame.mixer.quit()
    os.remove(filename)

def start_client():
    count = 0
    host = '10.113.21.176'
    port = 12345

    while True:
        try:
            query = input("Enter the string: ")
            if query == "None":
                continue
            if query.lower() == 'exit':
                print("Exiting.")
                break

            # Connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(10)  # Set a higher timeout for connection
            client_socket.connect((host, port))
            print("Connected to the server.")

            # Send the query to the server
            client_socket.send(query.encode('utf-8'))

            # Receive the response from the server
            response = client_socket.recv(4096).decode('utf-8')  # Increased buffer size
            print(f"Received from the server: '{response}'")

            # Speak the response
            speak(response, count)
            count += 1

            # Close the connection
            client_socket.close()
            print("Connection closed.")

            # Wait before the next command
            time.sleep(2)

        except socket.timeout:
            print("Connection timed out. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if client_socket:
                client_socket.close()
            time.sleep(5)  # Wait before retrying the connection

if _name_ == "_main_":
    start_client()