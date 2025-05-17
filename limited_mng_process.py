import os
import time
import datetime
import random

LOGFILE = "process_manager_with_limit.log"
MAX_RESTARTS = 3  # 最大復旧回数
RESTART_WINDOW = 30  # この秒数内に MAX_RESTARTS を超えたらストップ

def log(msg):
    with open(LOGFILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")
    print(msg)

def start_child(index):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(w)
        log(f"[子{index}] PID {os.getpid()} 起動")

        # 確率で異常終了（50%）
        if random.random() < 0.5:
            log(f"[子{index}] PID {os.getpid()} 確率的クラッシュ！")
            os._exit(1)

        # 生き残ったら親からメッセージを読み続ける
        r = os.fdopen(r)
        try:
            while True:
                msg = r.readline()
                if not msg:
                    break
                print(f"[子{index}] 受信: {msg.strip()}")
        finally:
            log(f"[子{index}] PID {os.getpid()} 正常終了")
            os._exit(0)
    else:
        os.close(r)
        return pid, w

if __name__ == "__main__":
    children = {}
    restarts = {}  # {index: [restart_timestamps]}
    num_children = 3

    for i in range(num_children):
        pid, w = start_child(i)
        children[pid] = (i, w)
        restarts[i] = [time.time()]

    while True:
        for pid, (index, w) in list(children.items()):
            try:
                os.write(w, f"ping from manager\n".encode())
            except BrokenPipeError:
                log(f"[親] 子{index} Broken Pipe!")
                restarts[index].append(time.time())
                # 復旧回数制限チェック
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

