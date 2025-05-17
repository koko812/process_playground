import os
import sys
import time
import datetime
import random

LOGFILE = "/tmp/process_manager_daemon.log"
PIDFILE = "/tmp/process_manager_daemon.pid"
MAX_RESTARTS = 3
RESTART_WINDOW = 30

def log(msg):
    with open(LOGFILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

def daemonize():
    if os.fork() > 0:
        sys.exit(0)  # 親を終了

    os.setsid()  # 新しいセッション

    if os.fork() > 0:
        sys.exit(0)  # セッションリーダーを捨てる

    # 標準入出力を閉じる
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a') as devnull:
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        os.dup2(devnull.fileno(), sys.stderr.fileno())

    # PIDファイル作成
    with open(PIDFILE, "w") as f:
        f.write(str(os.getpid()) + "\n")

def start_child(index):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(w)
        log(f"[子{index}] PID {os.getpid()} 起動")

        if random.random() < 0.5:
            log(f"[子{index}] PID {os.getpid()} 確率的クラッシュ！")
            os._exit(1)

        r = os.fdopen(r)
        try:
            while True:
                msg = r.readline()
                if not msg:
                    break
        finally:
            log(f"[子{index}] PID {os.getpid()} 正常終了")
            os._exit(0)
    else:
        os.close(r)
        return pid, w

def run_manager():
    children = {}
    restarts = {}
    num_children = 3

    for i in range(num_children):
        pid, w = start_child(i)
        children[pid] = (i, w)
        restarts[i] = [time.time()]

    while True:
        for pid, (index, w) in list(children.items()):
            try:
                os.write(w, f"ping\n".encode())
            except BrokenPipeError:
                log(f"[親] 子{index} Broken Pipe!")
                restarts[index].append(time.time())
                windowed_restarts = [t for t in restarts[index] if time.time() - t < RESTART_WINDOW]
                if len(windowed_restarts) > MAX_RESTARTS:
                    log(f"[親] 子{index} 復旧回数超過 → 停止")
                    del children[pid]
                    continue
                new_pid, new_w = start_child(index)
                children[new_pid] = (index, new_w)
                del children[pid]

        try:
            while True:
                finished_pid, status = os.waitpid(-1, os.WNOHANG)
                if finished_pid == 0:
                    break
                if finished_pid in children:
                    index, _ = children[finished_pid]
                    log(f"[親] 子{index} PID {finished_pid} 終了検知")
                    restarts[index].append(time.time())
                    windowed_restarts = [t for t in restarts[index] if time.time() - t < RESTART_WINDOW]
                    if len(windowed_restarts) > MAX_RESTARTS:
                        log(f"[親] 子{index} 復旧回数超過 → 停止")
                        del children[finished_pid]
                        continue
                    new_pid, new_w = start_child(index)
                    children[new_pid] = (index, new_w)
                    del children[finished_pid]
        except ChildProcessError:
            pass

        time.sleep(3)

if __name__ == "__main__":
    daemonize()
    log("[親] デーモン化完了、マネージャ開始")
    run_manager()

