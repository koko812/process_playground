import os
import sys
import time
import datetime

LOGFILE = "/tmp/my_daemon_heartbeat.log"
PIDFILE = "/tmp/my_daemon_heartbeat.pid"

def log(msg):
    with open(LOGFILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

def daemonize():
    if os.fork() > 0:
        sys.exit(0)
    os.setsid()
    if os.fork() > 0:
        sys.exit(0)

    os.chdir('/')
    os.umask(0)
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a') as devnull:
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        os.dup2(devnull.fileno(), sys.stderr.fileno())

    with open(PIDFILE, "w") as f:
        f.write(str(os.getpid()) + "\n")

def heartbeat_loop():
    log("[デーモン] 起動しました。")
    while True:
        log("[デーモン] heartbeat 生きてます。")
        time.sleep(1)

if __name__ == "__main__":
    daemonize()
    heartbeat_loop()

