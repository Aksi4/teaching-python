import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 12345)
client_socket.connect(server_address)

message = input("Введіть текст для відправки на сервер: ")

data_size = len(message)

client_socket.send(str(data_size).encode())

client_socket.send(message.encode())

response = client_socket.recv(1024).decode()
print(f"Відповідь від сервера: {response}")

client_socket.close()
