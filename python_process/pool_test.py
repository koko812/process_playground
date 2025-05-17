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

def run_pool(data, worker_func, num_processes):
    start = time.time()
    with Pool(processes=num_processes) as pool:
        result = pool.map(worker_func, data)
    print(f"[Pool] 所要時間: {time.time() - start:.2f}秒")
    return result

if __name__ == "__main__":
    data = list(range(100))  # 10件
    num_processes = 4

    print("=== 軽い処理 ===")
    print("シングル")
    run_single(data, light_worker)
    print("Pool")
    run_pool(data, light_worker, num_processes)

    print("\n=== 重い処理 ===")
    print("シングル")
    run_single(data, heavy_worker)
    print("Pool")
    run_pool(data, heavy_worker, num_processes)

