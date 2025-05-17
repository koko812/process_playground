# cpu_thread_test.py
from threading import Thread
import threading
import os
import time

def heavy_work():
    print(f"[スレッド] 名前: {threading.current_thread().name}, PID: {os.getpid()} 開始")
    total = 0
    for i in range(10**7):
        total += i*i
    print(f"[スレッド] 名前: {threading.current_thread().name} 終了")

if __name__ == "__main__":
    start = time.time()
    threads = []
    for _ in range(3):
        t = Thread(target=heavy_work)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"[スレッド] 全部完了: {time.time() - start:.2f}秒")

