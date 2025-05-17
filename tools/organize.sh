mkdir -p docker process thread pipe_ipc socket io_hang tools log data_test

# Docker
mv python_process/Dockerfile docker/

# プロセス関連
mv python_process/process_test.py process/
mv python_process/cpu_process_test.py process/
mv python_process/zombiee.py process/
mv python_process/kill_process.py process/

# スレッド関連
mv python_process/thread_test.py thread/
mv python_process/cpu_thread_test.py thread/
mv python_process/thread_queue_test.py thread/
mv python_process/imap_pool_test.py thread/

# IPC (pipe, queue, broken pipeなど)
mv python_process/pipe.py pipe_ipc/
mv python_process/pipe_hang.py pipe_ipc/
mv python_process/broken_pipe.py pipe_ipc/
mv python_process/broken_pipe2.py pipe_ipc/
mv python_process/process_queue_test.py pipe_ipc/
mv python_process/pool_test.py pipe_ipc/

# ソケット通信
mv python_process/client.py socket/
mv python_process/host.py socket/

# I/O ハング系
mv python_process/hang.py io_hang/

# ツール類
mv python_process/monitor.py tools/
mv python_process/b_monitor.py tools/
mv python_process/re_kill_process.py tools/

# ログ類
mv python_process/my_log.txt log/

# データ処理系
mv python_process/list_divide_test.py data_test/
mv python_process/list_single_test.py data_test/

