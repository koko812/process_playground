import os
import time

r, w = os.pipe()

pid = os.fork()

if pid == 0:
    # Child closes the read end immediately and exits
    os.close(r)
    print("Child: closing and exiting")
    os._exit(0)
else:
    os.close(r)  # Parent only keeps write end
    time.sleep(1)  # Wait to ensure child exits
    try:
        print("Parent: trying to write")
        os.write(w, b'Hello?')
        print("Parent: write succeeded (unexpected!)")
    except BrokenPipeError:
        print("Parent: got BrokenPipeError as expected!")

