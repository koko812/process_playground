import os
import fcntl
import time
from multiprocessing import Process

def locker():
    with open("lockfile", "w") as f:
        print(f"[locker] PID {os.getpid()} ファイルロック取得")
        fcntl.flock(f, fcntl.LOCK_EX)
        time.sleep(30)  # ロック保持（30秒）
        fcntl.flock(f, fcntl.LOCK_UN)
        print(f"[locker] ロック解除")

def waiter():
    with open("lockfile", "r") as f:
        print(f"[waiter] PID {os.getpid()} ファイルロック取得待機中")
        fcntl.flock(f, fcntl.LOCK_EX)
        print(f"[waiter] ロック取得できた！（解除済み）")

if __name__ == "__main__":
    # locker起動
    p1 = Process(target=locker)
    p1.start()

    time.sleep(1)  # 確実にlockerがロックしてから

    # waiter起動
    p2 = Process(target=waiter)
    p2.start()

    print(f"[メイン] locker PID: {p1.pid}, waiter PID: {p2.pid}")
    print("[メイン] psやhtopで確認してみて！（waiterがI/O待ちっぽくなる可能性あり）")

    # 観察タイム
    p1.join()
    p2.join()

