# thread_test.py
from threading import Thread
import threading
import os
import time

def worker():
    print(f"[スレッド] 名前: {threading.current_thread().name}, PID: {os.getpid()}")
    time.sleep(5)

if __name__ == "__main__":
    threads = []
    for i in range(3):
        t = Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[スレッド] 完了")

