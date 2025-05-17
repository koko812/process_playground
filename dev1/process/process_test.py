# process_test.py
from multiprocessing import Process
import os
import time

def worker():
    print(f"[プロセス] PID: {os.getpid()}")
    time.sleep(5)

if __name__ == "__main__":
    processes = []
    for i in range(3):
        p = Process(target=worker)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("[プロセス] 完了")

