import socket
import time
import threading 
import sys

active_clients = 0
active_clients_lock = threading.Lock()

terminate_server = False # вказівка завершення роботи сервера

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def client_handler(client_socket):
    global active_clients

    with active_clients_lock:
        active_clients += 1

    while True:
        data_size = client_socket.recv(1024).decode()

        try:
            data_size = int(data_size)
        except ValueError:
            print("Помилка: Невірний розмір даних від клієнта.")
            client_socket.close()
            break

        data_received = b""
        while len(data_received) < data_size:
            data_chunk = client_socket.recv(1024)
            if not data_chunk:
                print(f"Виникла помилка під час отримання даних від клієнта.")
                break

            data_received += data_chunk

        if len(data_received) == data_size:
            time.sleep(5)

            data_received = data_received.decode()
            if data_received != "exit":
                print(f"Отримано від клієнта: {data_received}")
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"Час отримання: {current_time}")
                response = "Дані отримано успішно."
                client_socket.send(response.encode())
            else:
                print(f"Клієнт {client_address} відключився.")
                client_socket.close()
                break
        else:
            print("Помилка: Не вдалося отримати всі дані від клієнта.")
            client_socket.close()

    with active_clients_lock:
        active_clients -= 1

# функція перевірки активних клієнтів і закриття сервера
def check_active_clients():
    global active_clients
    global terminate_server

    while not terminate_server:
        time.sleep(10)
        with active_clients_lock:
            if active_clients == 0:
                # перевірка на закриття сокетів
                if server_socket.fileno() != -1:
                    print("Всі клієнти відключилися. Відключення серверу.")
                    server_socket.close()
                    terminate_server = True
                break

server_address = ('127.0.0.1', 12345)
server_socket.bind(server_address)

server_socket.listen(1)

print("Сервер очікує підключення...")

# створення окремого потоку
active_clients_thread = threading.Thread(target=check_active_clients)
active_clients_thread.daemon = True
active_clients_thread.start()

while not terminate_server:
    try:
        client_socket, client_address = server_socket.accept()
        print(f"З'єднання від клієнта {client_address} встановлено.")
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()
    except socket.error as e:
        if terminate_server:
            break
        else:
            raise e

sys.exit()
