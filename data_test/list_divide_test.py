from multiprocessing import Process, Queue
import time

def process_worker(sub_data, q):
    # 各プロセスが受け取ったデータを加工
    result = [x * x for x in sub_data]
    q.put(result)

if __name__ == "__main__":
    data = list(range(10**6))  # 大きなデータ（100万個）
    num_processes = 4
    chunk_size = len(data) // num_processes

    q = Queue()
    processes = []
    start = time.time()

    # 分割して各プロセスに投げる
    for i in range(num_processes):
        sub_data = data[i*chunk_size : (i+1)*chunk_size]
        p = Process(target=process_worker, args=(sub_data, q))
        p.start()
        processes.append(p)

    # 結果を集約
    result = []
    for _ in range(num_processes):
        result.extend(q.get())

    for p in processes:
        p.join()

    print(f"合計データ数: {len(result)}")
    print(f"所要時間: {time.time() - start:.2f}秒")

