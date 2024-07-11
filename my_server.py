import socket
import threading
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import json
import os

# Load the trained model
model_path = 'C:/Users/91809/OneDrive/Desktop/siddhartha_114/S4/IoT/serverside/chatbot_model.h5'
model = load_model(model_path)

# Load the tokenizer
tokenizer_path = 'C:/Users/91809/OneDrive/Desktop/siddhartha_114/S4/IoT/serverside/tokenizer.pickle'
with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the label encoder
label_encoder_path = 'C:/Users/91809/OneDrive/Desktop/siddhartha_114/S4/IoT/serverside/label_encoder.pickle'
with open(label_encoder_path, 'rb') as handle:
    label_encoder = pickle.load(handle)

# Load intents data
intents_path = 'C:/Users/91809/OneDrive/Desktop/siddhartha_114/S4/IoT/serverside/intents.json'
with open(intents_path, 'r') as f:
    data = json.load(f)

def generate_response(prompt):
    # Preprocess the input
    sequences = tokenizer.texts_to_sequences([prompt])
    padded_sequences = pad_sequences(sequences, truncating='post', maxlen=20)

    # Predict the intent
    predictions = model.predict(padded_sequences)
    predicted_label_index = np.argmax(predictions)
    predicted_tag = label_encoder.inverse_transform([predicted_label_index])[0]

    # Find the response
    for intent in data['intents']:
        if intent['tag'] == predicted_tag:
            return np.random.choice(intent['responses'])
    return "Sorry, I don't understand."

def handle_client(client_socket, addr):
    print(f"Got a connection from {addr}")
    try:
        while True:
            data = client_socket.recv(4096).decode('utf-8')  # Increased buffer size
            if data == 'KEEP_ALIVE':
                # Ignore keep-alive messages
                continue
            if not data:
                print(f"Client {addr} disconnected")
                break
            response = generate_response(data)
            print(f"Sending '{response}' back to the client")
            client_socket.send(response.encode('utf-8'))
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '192.168.137.1'
    port = 12345
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse the socket address
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started and listening on {host}:{port}")
    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_socket.settimeout(60)  # Set a higher timeout for socket operations
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
