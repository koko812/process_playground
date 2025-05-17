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
    try:
        while True:
            # p.exitcode が None の間は生きてる
            if p.exitcode is not None:
                print(f"[親プロセス] 子プロセス {p.pid} が終了を検知 (exitcode: {p.exitcode})")
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("[親プロセス] モニタ中断")

if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    print(f"[親プロセス] 子プロセス PID: {p.pid} を監視開始")

    # こっちで監視
    monitor_process(p)

    # 最後は必ず join でゾンビ回収
    p.join()
    print("[親プロセス] 終了")

