# エラー図鑑（Process Playground版）

## 🐍 Python実験中のトラブル

### BrokenPipeError が出ない
- 状況：pipeを作っても読み手を先に殺すだけではエラーが出なかった
- 原因：**書き込み時にしかBrokenPipeErrorは発生しない**
- 対策：読み手を閉じた後に`os.write()`で書くと確実に発生

### fuse: failed to open /dev/fuse: Operation not permitted
- 状況：fusepyでマウントしようとしたがエラー
- 原因：**Dockerの--privilegedオプションが不足**
- 対策：`--privileged`をつけることで解消

### fuse: device not found, try 'modprobe fuse' first
- 状況：Docker内でfuseを使おうとして失敗
- 原因：**/dev/fuseが存在しない、もしくはパーミッション不足**
- 対策：
  - `--device /dev/fuse`を付ける（ただしMacでは不可）
  - 最初から`--privileged`で逃げるのが楽

---

## 🐋 Docker周りのハマり所

### libfuse不足
- 状況：fusepyが`RuntimeError`を出す
- 原因：`libfuse2`が入ってなかった
- 対策：Dockerfileで`apt install -y libfuse2`追加

### Mac環境ではD状態が出ない
- 状況：fusepyでI/Oハングを起こそうとしても`D`にならない
- 原因：Macではカーネルが異なり、**I/O待ちはDにならずハングだけ発生**
- 対策：**Docker内のLinux環境でのみ再現可**

---

## 🔧 OS/ツール周り

### tcpdumpでデータが見えない
- 状況：PSH, ACKのデータ送受信が確認できない
- 原因：`tcpdump`デフォルトではデータ部非表示
- 対策：
  - `-A`（ASCII表示）
  - `-X`（HEX＋ASCII表示）を使う

### swapが減らない
- 状況：メモリ逼迫してもswapが解放されない
- 原因：プロセスがメモリ保持したまま終了していない
- 対策：
  - swapを強制的に減らすには`swapoff -a && swapon -a`など必要
  - 根本的にはメモリリーク解消＆プロセスkill

### htopでswap列が見えない
- 状況：`htop`でswap使用量が確認できない
- 対策：
  - `F2` → `Columns`で`SWAP`列を追加
  - `htop`3.x系以降だと標準で見えることも

---

## 💡 補足tips
- MacではDockerは**Linux VM上で動いているため、ホストの/dev/fuseとは別物**
- Broken Pipeを意図的に出すには**常に読み手を閉じた後に書き込み必須**
- TCP通信は**3-way handshakeと4-way closeをtcpdumpで見ると超理解できる**


