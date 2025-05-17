import os

r, w = os.pipe()

pid = os.fork()

if pid == 0:
    # Child exits immediately
    print("Child: exiting immediately")
    os._exit(0)
else:
    print("Parent: writing to pipe...")
    try:
        while True:
            os.write(w, b'A' * 1024)  # write 1KB at a time
            print("Parent: wrote 1KB")
    except BrokenPipeError:
        print("Parent: got BrokenPipeError (expected!)")

