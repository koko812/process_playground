# thread_queue_test.py
from threading import Thread
from queue import Queue
import threading
import os
import time

def worker(q, num):
    print(f"[スレッド] 名前: {threading.current_thread().name} で計算開始")
    result = sum([i*i for i in range(num)])
    q.put((threading.current_thread().name, result))
    print(f"[スレッド] 名前: {threading.current_thread().name} で計算終了")

if __name__ == "__main__":
    q = Queue()
    threads = []
    for i in range(3):
        t = Thread(target=worker, args=(q, 10**6))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    while not q.empty():
        name, result = q.get()
        print(f"[メイン] 受信: スレッド {name} → 計算結果: {result}")

