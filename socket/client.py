import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ソケット作成（TCP用）
client.connect(('localhost', 12345))  # サーバに接続
print("Client: Connected to server")

client.sendall(b'Hello from client!')  # データ送信
data = client.recv(1024)  # サーバから受信
print(f"Client: Received: {data.decode()}")

client.close()  # 接続を閉じる

