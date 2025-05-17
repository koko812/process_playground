import os
import time

def start_child():
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(w)
        print(f"[子] PID {os.getpid()} 起動 (htop で見てね)")
        r = os.fdopen(r)
        try:
            while True:
                msg = r.readline()
                if not msg:
                    break
                print(f"[子] 受信: {msg.strip()}")
        finally:
            print(f"[子] PID {os.getpid()} 終了")
            os._exit(0)
    else:
        os.close(r)
        return pid, w

if __name__ == "__main__":
    pid, w = start_child()
    print(f"[親] PID {os.getpid()} 子 PID {pid}")

    for i in range(10):
        try:
            os.write(w, f"メッセージ {i}\n".encode())
            if i == 4:
                print(f"[親] 子 PID {pid} を kill")
                os.kill(pid, 9)
                os.wait()
                time.sleep(5)
                print("[親] 復旧開始")
                pid, w = start_child()
            time.sleep(2)
        except BrokenPipeError:
            print("[親] Broken Pipe! 再生成")
            pid, w = start_child()

    print("[親] 完了、30秒待機（htop 確認）")
    time.sleep(30)

