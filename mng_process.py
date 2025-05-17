import os
import time
import datetime

LOGFILE = "process_manager.log"

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
        r = os.fdopen(r)
        try:
            while True:
                msg = r.readline()
                if not msg:
                    break
                print(f"[子{index}] 受信: {msg.strip()}")
        finally:
            log(f"[子{index}] PID {os.getpid()} 終了")
            os._exit(1)
    else:
        os.close(r)
        return pid, w

if __name__ == "__main__":
    children = {}
    num_children = 3

    for i in range(num_children):
        pid, w = start_child(i)
        children[pid] = (i, w)

    while True:
        for pid, (index, w) in list(children.items()):
            try:
                os.write(w, f"ping from manager\n".encode())
            except BrokenPipeError:
                log(f"[親] 子{index} Broken Pipe! 復旧")
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
                    log(f"[親] 子{index} PID {finished_pid} 終了検知 → 復旧")
                    new_pid, new_w = start_child(index)
                    children[new_pid] = (index, new_w)
                    del children[finished_pid]
        except ChildProcessError:
            pass

        time.sleep(3)

