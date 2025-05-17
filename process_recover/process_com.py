from multiprocessing import Process, Pipe

def child(conn):
    print("[子] 受信待ち...")
    msg = conn.recv()
    print(f"[子] 受信: {msg}")
    conn.send("[子] 了解だ！")

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=child, args=(child_conn,))
    p.start()
    parent_conn.send("[親] やあ！")
    reply = parent_conn.recv()
    print(f"[親] 子から返信: {reply}")
    p.join()

