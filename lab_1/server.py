import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 12345)  
server_socket.bind(server_address)


server_socket.listen(1)

print("Сервер очікує підключення...")

client_socket, client_address = server_socket.accept()
print(f"З'єднання від клієнта {client_address} встановлено.")

data = client_socket.recv(1024)
print(f"Отримано від клієнта: {data.decode()}")

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"Час отримання: {current_time}")

client_socket.close()
server_socket.close()
