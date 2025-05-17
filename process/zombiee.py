from multiprocessing import Process
import os
import time

def worker():
    print(f"[子プロセス] PID: {os.getpid()} 開始")
    time.sleep(2)  # すぐ終了
    print(f"[子プロセス] PID: {os.getpid()} 終了")

if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    print(f"[親プロセス] PID: {os.getpid()} 子PID: {p.pid}")

    print("[親プロセス] これから待機（joinしない）")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[親プロセス] Ctrl+Cで終了")

