# UNIX デーモン設計・標準パターン集

## 1. デーモン化手順（黄金パターン）

```python
def daemonize():
    if os.fork() > 0:
        sys.exit(0)  # 親を終了

    os.setsid()  # 新しいセッション開始

    if os.fork() > 0:
        sys.exit(0)  # セッションリーダーを捨てる

    os.chdir('/')  # カレントディレクトリをルートに
    os.umask(0)    # ファイル作成マスクをリセット

    # 標準入出力を閉じる
    with open('/dev/null', 'r') as devnull:
        os.dup2(devnull.fileno(), 0)
    with open('/dev/null', 'a') as devnull:
        os.dup2(devnull.fileno(), 1)
        os.dup2(devnull.fileno(), 2)
```

## 2. PIDファイル管理

```python
def write_pidfile():
    if os.path.exists(PIDFILE):
        print("すでに実行中？ PIDファイルあり")
        sys.exit(1)
    with open(PIDFILE, "w") as f:
        f.write(str(os.getpid()))

def remove_pidfile():
    if os.path.exists(PIDFILE):
        os.remove(PIDFILE)
```

## 3. ログ管理

```python
import logging
logging.basicConfig(filename='/var/log/mydaemon.log', level=logging.INFO)
```

## 4. シグナル対応

```python
import signal

def sigterm_handler(signum, frame):
    logging.info("SIGTERM 受信 → 終了")
    remove_pidfile()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)
```

## 5. 復旧回数制御（指数バックオフ付き）

```python
retry_count = 0
max_retries = 5
while True:
    try:
        start_child()
        retry_count = 0
    except Exception:
        retry_count += 1
        if retry_count > max_retries:
            logging.error("復旧失敗回数超過 → 終了")
            sys.exit(1)
        time.sleep(2 ** retry_count)
```

## 6. 親・子プロセスの責務分離（監視ループ）

```python
def supervise():
    while True:
        pid = os.fork()
        if pid == 0:
            do_child_work()
            os._exit(0)
        else:
            pid_dead, status = os.wait()
            logging.warning(f"子プロセス {pid_dead} が終了 → 再起動")
```

## 実務的な流れまとめ

1. デーモン化（ダブル fork、セッション切り離し、FD閉じる）
2. PID ファイル管理
3. ログ管理（ローテート対応）
4. 復旧回数制御（バックオフ対応）
5. シグナル対応（優雅な終了 or 再読み込み）
6. 親と子の責務分離（監視ループ）

**このパターンを押さえれば、UNIX デーモンとしての標準的な設計になる。**
`sshd`、`nginx`、`cron` もほぼこの構成。

