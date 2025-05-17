import os

r, w = os.pipe()

pid = os.fork()

if pid == 0:
    # Child does nothing (never reads)
    print("Child: doing nothing, not reading...")
    while True:
        pass  # keep child alive doing nothing
else:
    print("Parent: writing large data to pipe...")
    try:
        while True:
            os.write(w, b'A' * 1024)  # write 1KB at a time
            print("Parent: wrote 1KB")
    except BrokenPipeError:
        print("Parent: pipe broken")

