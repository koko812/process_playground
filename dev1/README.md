# Process Playground

このリポジトリは、**プロセス、スレッド、IPC、ソケット通信、I/Oハングなど、プロセスまわりの挙動を手を動かしながら学ぶための実験場**です。

## 目的
- BashとPythonを使って**プロセスとスレッドの正体を体感的に理解**
- プロセス生成・監視・終了などの**基礎操作を実践**
- pipeやsocketを使って**プロセス間通信（IPC）の地獄を体感**
- Broken Pipe、I/Oハング、swap地獄も実際に体験
- 現場で使える**プロセス管理スキルとデバッグ術を習得**

## ディレクトリ構成
```
process_playground/
├── docker/         # Dockerfileなど実験環境
├── process/        # プロセス操作系（fork, kill, zombieなど）
├── thread/         # スレッド実験（thread, queue, pool）
├── pipe_ipc/       # pipe, queue, broken pipeなどIPC
├── socket/         # TCPクライアント＆サーバ通信
├── io_hang/        # I/Oハング体験（fusepyなど）
├── tools/          # プロセス監視、killツール、整理スクリプト
├── data_test/      # リスト処理など負荷テスト用
└── log/            # ログ・キャプチャ保存
```

## 使い方例

### プロセス操作（Python）
```bash
cd process
python3 process_test.py
```

### スレッドとプロセス比較
```bash
cd thread
python3 cpu_thread_test.py
python3 cpu_process_test.py
```

### Pipe通信とBroken Pipe体験
```bash
cd pipe_ipc
python3 pipe_hang.py
python3 broken_pipe.py
```

### TCPソケット通信
```bash
cd socket
python3 host.py  # サーバ起動
python3 client.py  # クライアント実行
```

### I/Oハング体験（Docker内推奨）
```bash
cd io_hang
python3 hang.py
```

### ログ確認
```bash
less log/my_log.txt
```

### プロセス整理スクリプト実行
```bash
cd tools
bash organize.sh
```

## 注意
- `pipe`, `socket`実験は**事前に`tcpdump`で可視化推奨**
- I/OハングやBroken Pipeは**Docker内実行が安全**
- 実行環境：Mac, Linux（Docker対応）