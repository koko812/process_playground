# Process Playground

このリポジトリは、**プロセスの挙動を実際に手を動かしながら学ぶための遊び場**です。

## 目的
- BashとPythonを使って「プロセス」の正体を理解する
- プロセスの生成、監視、終了などの基本操作を実践する
- スレッドとの違いも体感して、実務で使える知識に落とし込む

## 構成
```
process_playground/
├── bash/
│ ├── sleep_test.sh # Bashでプロセス生成・確認・kill
│ └── ps_grep_kill.sh # psとgrepでプロセス調査
└── python/
├── subprocess_test.py # Pythonでプロセス生成・監視・終了
└── multi_process_watch.py # 複数プロセスの管理サンプル
```

## 使い方
### Bash編
```bash
cd bash
./sleep_test.sh
```

### Python編
```bash
cd python
python subprocess_test.py
```
