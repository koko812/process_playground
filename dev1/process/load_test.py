from multiprocessing import Process
from threading import Thread
import os
import time

def heavy_work(n):
    # わざと計算負荷を作る
    total = 0
    for i in range(n):
        total += i * i

def run_process(n, workers):
    processes = []
    start = time.time()
    for _ in range(workers):
        p = Process(target=heavy_work, args=(n,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    return time.time() - start

def run_thread(n, workers):
    threads = []
    start = time.time()
    for _ in range(workers):
        t = Thread(target=heavy_work, args=(n,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    return time.time() - start

if __name__ == "__main__":
    N_list = [10**4, 10**5, 10**6, 10**7, 10**8]
    workers = 4

    print(f"比較: プロセス vs スレッド (ワーカー数: {workers})\n")

    for N in N_list:
        print(f"=== 負荷: {N} ===")
        t1 = run_process(N, workers)
        t2 = run_thread(N, workers)
        print(f"[プロセス] {t1:.4f} 秒")
        print(f"[スレッド] {t2:.4f} 秒")
        print("------------------------")

