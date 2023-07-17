import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 8000

# List to store connected clients
clients = []

def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received message from {client_address}: {message}")

                # Broadcast the message to all connected clients
                broadcast(message, client_socket)

        except Exception as e:
            print(f"Error handling client {client_address}: {str(e)}")
            remove_client(client_socket)
            break

def broadcast(message, sender_socket):
    for client in clients:
        # Send the message to all clients except the sender
        if client != sender_socket:
            client.send(message.encode('utf-8'))

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the server socket to a specific host and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen()

        print(f"Server started on {HOST}:{PORT}")

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)

            # Create a new thread to handle the client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.start()

    except Exception as e:
        print(f"Error starting the server: {str(e)}")
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()
