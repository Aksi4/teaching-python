import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 12345)
client_socket.connect(server_address)

while True:
    message = input("Введіть текст для відправки на сервер (або 'exit' для завершення): ")

    data_size = len(message)

    client_socket.send(str(data_size).encode())

    client_socket.send(message.encode())

    response = client_socket.recv(1024).decode()
    print(f"Відповідь від сервера: {response}")

    if message.lower() == "exit":
        print(f"З'єднання з сервером втрачено.")
        break
    


client_socket.close()
