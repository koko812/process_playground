from multiprocessing import Process
import os
import time
import psutil

def worker():
    print(f"[子プロセス] PID: {os.getpid()} 開始")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"[子プロセス] 強制終了された？")

def monitor_process(p):
    proc = psutil.Process(p.pid)
    try:
        while True:
            if not proc.is_running():
                print(f"[親プロセス] 子プロセス {p.pid} が終了を検知")
                break
            time.sleep(1)
    except psutil.NoSuchProcess:
        print(f"[親プロセス] 子プロセス {p.pid} が既に存在しない")
    print("[親プロセス] モニタ終了")

if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    print(f"[親プロセス] 子プロセス PID: {p.pid} を監視開始")

    # モニタリング開始
    monitor_process(p)

