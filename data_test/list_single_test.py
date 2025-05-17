import time

def single_worker(data):
    result = [x * x for x in data]
    return result

if __name__ == "__main__":
    data = list(range(10**6))  # 大きなデータ（100万個）

    start = time.time()

    result = single_worker(data)

    print(f"合計データ数: {len(result)}")
    print(f"所要時間: {time.time() - start:.2f}秒")

