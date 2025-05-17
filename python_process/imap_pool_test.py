from multiprocessing import Pool
import time

def light_worker(x):
    return x * x

def heavy_worker(x):
    total = 0
    for _ in range(1000000):
        total += x * x
    return total

def run_single(data, worker_func):
    start = time.time()
    result = [worker_func(x) for x in data]
    print(f"[シングル] 所要時間: {time.time() - start:.2f}秒")
    return result

def run_pool_map(data, worker_func, num_processes):
    start = time.time()
    with Pool(processes=num_processes) as pool:
        result = pool.map(worker_func, data)
    print(f"[Pool map] 所要時間: {time.time() - start:.2f}秒")
    return result

def run_pool_imap(data, worker_func, num_processes):
    start = time.time()
    with Pool(processes=num_processes) as pool:
        for result in pool.imap(worker_func, data):
            results = result
            #print(f"[受信] {result} at {time.time() - start:.2f}秒")
    print(f"[Pool imap] 全部完了: {time.time() - start:.2f}秒")

if __name__ == "__main__":
    data = list(range(100))
    num_processes = 4

    print("=== 軽い処理 ===")
    print("シングル")
    run_single(data, light_worker)
    print("Pool map")
    run_pool_map(data, light_worker, num_processes)
    print("Pool imap")
    run_pool_imap(data, light_worker, num_processes)

    print("\n=== 重い処理 ===")
    print("シングル")
    run_single(data, heavy_worker)
    print("Pool map")
    run_pool_map(data, heavy_worker, num_processes)
    print("Pool imap")
    run_pool_imap(data, heavy_worker, num_processes)

