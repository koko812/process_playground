import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ソケット作成（TCP用）
server.bind(('localhost', 12345))  # 127.0.0.1:12345で待ち受け開始
server.listen(1)  # 接続待ち状態にする（最大1接続まで待ち受け）

print("Server: Waiting for connection...")

conn, addr = server.accept()  # 接続を受け付ける（ブロックする）
print(f"Server: Connected by {addr}")

data = conn.recv(1024)  # クライアントから受信（最大1024バイト）
print(f"Server: Received: {data.decode()}")

conn.sendall(b'Hello from server!')  # クライアントへデータ送信
print("Server: Sent reply")

conn.close()  # 接続を閉じる
server.close()  # サーバソケットも閉じる

