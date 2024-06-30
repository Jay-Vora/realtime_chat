import socket

# Create a TCP/IP socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
my_socket.bind(("localhost", 7007))

# Listen for incoming connections
my_socket.listen(5)
print("Server listening on port 7007...")

try:
    while True:
        # Accept a connection
        incoming_socket, incoming_address = my_socket.accept()
        print(f"Connection from {incoming_address}")

        while True:
            # Initialize an empty buffer
            received_buffer = b''

            # Receive data from the client
            while True:
                chunk = incoming_socket.recv(4096)
                if not chunk:  # Handle client disconnection
                    break
                received_buffer += chunk
                if chunk.endswith(b"\n"):  # Assuming messages are newline-terminated
                    break

            # If the connection was closed by the client
            if not received_buffer:
                print(f"Connection from {incoming_address} closed.")
                break

            # Decode the received data to check for the "quit" command
            received_message = received_buffer.decode().strip()
            if received_message.lower() == "quit":
                print("Termination signal received. Shutting down server.")
                incoming_socket.close()
                my_socket.close()
                exit(0)

            # Send the received data back to the client
            incoming_socket.sendall(received_buffer)

        incoming_socket.close()

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    my_socket.close()