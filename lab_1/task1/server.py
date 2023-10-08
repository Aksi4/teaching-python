import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 12345)
server_socket.bind(server_address)

server_socket.listen(1)

print("Сервер очікує підключення...")

client_socket, client_address = server_socket.accept()
print(f"З'єднання від клієнта {client_address} встановлено.")

while True:
    data_size = client_socket.recv(1024).decode()
    
    try:
        data_size = int(data_size)
    except ValueError:
        print("Помилка: Невірний розмір даних від клієнта.")
        break

    data_received = b""
    while len(data_received) < data_size:
        data_chunk = client_socket.recv(1024)
        if not data_chunk:
            break
        data_received += data_chunk

    if len(data_received) == data_size:
        data_received = data_received.decode()
        print(f"Отримано від клієнта: {data_received}")
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Час отримання: {current_time}")

        if data_received.lower() == "exit":
            response = "Сервер закрив з'єднання."
            client_socket.send(response.encode())
            break

        response = "Дані отримано успішно."
        client_socket.send(response.encode())
    else:
        print("Помилка: Не вдалося отримати всі дані від клієнта.")

client_socket.close()
server_socket.close()
