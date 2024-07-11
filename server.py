import socket
from bardapi import Bard
import google.generativeai as genai
import threading
import time

genai.configure(api_key='AIzaSyCo53qFQ04GeubsoGGm-2t0WShbyJ3XttY')
model = genai.GenerativeModel('gemini-pro')
print("Model has been loaded")

def generate_response(prompt):
    response = model.generate_content(f"{prompt}, give a response in 10-15 words")
    return response.text

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
    # host = '10.113.21.176'
    # host='192.168.137.1'
    host = '192.168.101.201'
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