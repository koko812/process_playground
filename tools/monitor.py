from multiprocessing import Process
from threading import Thread
import os
import time
import psutil

def monitor(interval=1):
    process = psutil.Process(os.getpid())
    while True:
        mem = process.memory_info().rss / 1024 / 1024
        cpu = process.cpu_percent(interval=interval)
        print(f"[モニタ] PID: {os.getpid()} メモリ: {mem:.2f} MB, CPU: {cpu:.2f}%")

def cpu_heavy_task():
    while True:
        _ = sum(i*i for i in range(10000))

def io_task():
    while True:
        time.sleep(0.1)

def process_worker():
    # CPUヘビー＆I/Oスレッドを同時に立てる
    for _ in range(2):
        Thread(target=cpu_heavy_task, daemon=True).start()
        Thread(target=io_task, daemon=True).start()

    # プロセス内のモニタを立てる
    monitor()

if __name__ == "__main__":
    # プロセスを2つ立てる
    processes = []
    for _ in range(2):
        p = Process(target=process_worker)
        p.start()
        processes.append(p)

    # メインプロセスでも監視（メインはほぼアイドルのはず）
    monitor()

