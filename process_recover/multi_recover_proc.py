import os
import time

def start_child(index):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(w)
        print(f"[子{index}] PID {os.getpid()} 起動 (htop で確認してね)")
        r = os.fdopen(r)
        try:
            while True:
                msg = r.readline()
                if not msg:
                    break
                print(f"[子{index}] 受信: {msg.strip()}")
        finally:
            print(f"[子{index}] PID {os.getpid()} 終了")
            os._exit(0)
    else:
        os.close(r)
        return pid, w

if __name__ == "__main__":
    children = {}
    num_children = 3

    # 子プロセス起動
    for i in range(num_children):
        pid, w = start_child(i)
        children[pid] = (i, w)

    for i in range(10):
        for pid in list(children):
            index, w = children[pid]
            try:
                os.write(w, f"[親] 子{index}へ メッセージ {i}\n".encode())
                if i == 4 and index == 1:
                    print(f"[親] 子{index} PID {pid} を kill")
                    os.kill(pid, 9)
                    os.waitpid(pid, 0)
                    time.sleep(2)
                    print(f"[親] 子{index} 復旧開始")
                    new_pid, new_w = start_child(index)
                    children[new_pid] = (index, new_w)
                    del children[pid]
            except BrokenPipeError:
                print(f"[親] 子{index} Broken Pipe! 再生成")
                new_pid, new_w = start_child(index)
                children[new_pid] = (index, new_w)
                del children[pid]

        time.sleep(2)

    print("[親] 完了、30秒待機（htop で確認）")
    time.sleep(30)

