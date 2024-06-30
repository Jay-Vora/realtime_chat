import socket
import select   
import sys

my_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

my_client.connect(("localhost", 7007))

user_name_prefix = input("name: ")

while True:
    read_socket, _, _ = select.select([socket.socket(), my_client],[], [])

    for sock in read_socket :
        if sock == socket.socket():
            user_input = sys.stdin.readline().strip()
            if user_input.lower() == 'quit' :
                break
            my_client.sendall((user_name_prefix + ":" + user_input).encode("utf-8"))
            print(f"{user_name_prefix}: {user_input}")
        elif sock == my_client:
            server_response = my_client.recv(4096).decode()

            if not server_response:
                print("Server disconnected.")
                break

            print(f"recv: {server_response}")

    
    if user_input.lower() == "quit":
        break

my_client.close()
