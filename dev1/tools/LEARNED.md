# Process Playground 学習メモ

## 📌 プロセスとスレッドの違い体感
- プロセス → メモリ空間独立、重い、forkで生成
- スレッド → 同じメモリ空間、軽い、threadingで生成
- → 実際にCPU負荷を与えて、プロセスとスレッドの使い分けを体感

## 📌 psutil, ps, top, htop でプロセス監視
- プロセスの状態（R, S, D, Z）を確認
- 特に `D` 状態（I/O待ち）を狙って疑似ハング体験
- `htop`のカラム追加、フィルタも習得

## 📌 I/Oハング（fusepyを使って）
- Macでは`D`状態にならない（カーネルの違い）
- Docker内（Linux）でのみ`D`状態体験
- Dockerは`--privileged`を使えばFuse動作OK

## 📌 Broken Pipe体験
- pipe作成 → 読み手をkill → 書き込み → BrokenPipeError
- → 読み手を閉じた後に書き込みしないとBroken Pipeは起きない

## 📌 Dockerの正しい使い方
- Fuseなど特殊デバイスを使うには`--privileged` or `--device /dev/fuse`
- MacとLinuxの違いを理解
- Dockerfile内では`set -euxo pipefail`でプロ風に書く

## 📌 ソケット通信（TCP）
- PythonのsocketモジュールでTCP通信
- 3-way handshake、データ送受信、4-way closeを実践
- Broken Pipeになるパターンも体感

## 📌 tcpdumpとWiresharkで通信可視化
- `tcpdump -i lo0 port 12345 -nn -A`で全パケット＆データを確認
- SYN, PSH, FINなどフラグを観察
- Wiresharkを使えばより直感的に見える

## 📌 swapとメモリ状況のデバッグ
- swapが逼迫した時の観察
- swap解放には`swapoff -a`など必要
- `smem`はMacでは使えない、`ps aux`や`top`を工夫して見る

## 📌 現場流ディレクトリ整理
- docker/, process/, thread/, pipe_ipc/, socket/, io_hang/ に分類
- log/やtools/を分けてゴミをコードと分離
- `README.md`や`ERRORS.md`でナレッジを残す習慣

---

## 🎯 現場で得たスキル
- OSプロセス管理、スレッド管理の基礎を体験的に理解
- I/Oハング、Broken Pipe、TCP通信の挙動をパケットレベルで可視化
- Docker内で安全に地獄を再現しつつ、カーネルとデバイスの違いを理解
- htop, tcpdump, ps, smemなどツールの現場流使い方習得
- 失敗とハマりをエラー図鑑化する習慣が身についた


