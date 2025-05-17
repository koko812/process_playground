import os
import time

r, w = os.pipe()  # パイプ作成（戻り値は読み口、書き口のファイルディスクリプタ）

pid = os.fork()   # プロセスを複製（親と子が同じコードを同時に実行）

if pid == 0:
    # 子プロセス
    print("Child: sleeping before reading...")
    time.sleep(5)  # 5秒寝る（親が先に書き込むようにする）
    data = os.read(r, 1024)  # パイプから読み取る
    print(f"Child: read data: {data}")
else:
    # 親プロセス
    print("Parent: writing to pipe...")
    os.write(w, b'Hello from parent!')  # パイプに書き込む
    print("Parent: done writing, sleeping...")
    time.sleep(10)  # 親は10秒寝る（子が読む間プロセスは存在し続ける）


