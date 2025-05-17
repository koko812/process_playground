from multiprocessing import Process, current_process
from threading import Thread, current_thread
import os
import time
import psutil

def monitor(process_name, interval=1):
    process = psutil.Process(os.getpid())
    while True:
        mem = process.memory_info().rss / 1024 / 1024
        cpu = process.cpu_percent(interval=interval)
        print(f"[{process_name}] PID: {os.getpid()} メモリ: {mem:.2f} MB, CPU: {cpu:.2f}%")

def cpu_heavy_task(task_name):
    while True:
        _ = sum(i*i for i in range(10000))
        # スレッド確認ログ
        print(f"[{task_name}] PID: {os.getpid()} スレッド: {current_thread().name} 動いてる")

def io_task(task_name):
    while True:
        time.sleep(0.1)
        print(f"[{task_name}] PID: {os.getpid()} スレッド: {current_thread().name} I/O中")

def process_worker(proc_id):
    process_name = f"WorkerProc-{proc_id}"
    print(f"[{process_name}] 起動 (PID: {os.getpid()})")
    # CPU & I/O スレッド起動
    for i in range(2):
        Thread(target=cpu_heavy_task, args=(f"{process_name}-CPU-{i}",), daemon=True).start()
        Thread(target=io_task, args=(f"{process_name}-IO-{i}",), daemon=True).start()

    monitor(process_name)

if __name__ == "__main__":
    processes = []
    for i in range(2):
        p = Process(target=process_worker, args=(i,))
        p.start()
        processes.append(p)

    # メインプロセスでも監視
    monitor("MainProcess")

