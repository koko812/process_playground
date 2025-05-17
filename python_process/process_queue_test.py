# process_queue_test.py
from multiprocessing import Process, Queue
import os
import time

def worker(q, num):
    print(f"[プロセス] PID: {os.getpid()} で計算開始")
    result = sum([i*i for i in range(num)])
    q.put((os.getpid(), result))
    print(f"[プロセス] PID: {os.getpid()} で計算終了")

if __name__ == "__main__":
    q = Queue()
    processes = []
    for i in range(3):
        p = Process(target=worker, args=(q, 10**6))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    # 結果を受け取る
    while not q.empty():
        pid, result = q.get()
        print(f"[メイン] 受信: PID {pid} → 計算結果: {result}")

