# cpu_process_test.py
from multiprocessing import Process
import os
import time

def heavy_work():
    print(f"[プロセス] PID: {os.getpid()} 開始")
    total = 0
    for i in range(10**7):
        total += i*i
    print(f"[プロセス] PID: {os.getpid()} 終了")

if __name__ == "__main__":
    start = time.time()
    processes = []
    for _ in range(3):
        p = Process(target=heavy_work)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f"[プロセス] 全部完了: {time.time() - start:.2f}秒")

