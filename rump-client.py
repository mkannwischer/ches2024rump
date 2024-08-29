#!/usr/bin/env python3
import sys, socket, re, ast, time
import threading
import subprocess
token = 'r3m7oafMN38vjYbn'
host, port = 'rump.kannwischer.eu', 8889
#host, port = '127.0.0.1', 8889

################################################################

def conn():
    sock = socket.socket()
    sock.settimeout(5)
    sock.connect((host, port))
    sock.sendall(token.encode())
    sock.settimeout(None)
    return sock

rx = re.compile('^([a-z]+): (.+)$')
def proc(s):
    m = rx.match(s)
    assert m is not None
    key, val = m.groups()
    val = ast.literal_eval(val)
    return key, val

def run(callback):
    while True:
        try:
            sock = conn()
        except ConnectionRefusedError:
            time.sleep(1)
            continue
        try:
            while True:
                s = b''
                while True:
                    while b'\n' not in s:
                        tmp = sock.recv(0x100)
                        if not tmp:
                            raise EOFError
                        s += tmp
                    idx = s.index(b'\n')
                    line, s = s[:idx], s[idx+1:]
                    data = proc(line.decode(errors='replace'))
                    callback(*data)
        except (ConnectionError, EOFError, OSError):
            pass


################################################################

if __name__ == '__main__':
    msg = [""]
    startCtr = -1
    ctr = -1
    threshold = 3
    enabled = True

    def call_the_seals():
        subprocess.Popen(["./overlay/halifaxseal"])
        subprocess.Popen(["mpv", "--no-audio-display", "seal.m4a"])

    def kill_the_seals():
        subprocess.Popen(["killall", "halifaxseal"])


    def update_label():
        global msg, ctr, startCtr, threshold, enabled
        if enabled:
            s = f"{threshold+startCtr-ctr}"
        else:
            s = f"-1"

        subprocess.call(["killall", "halifaxcounter"])
        subprocess.Popen(["./overlay/halifaxcounter", str(s)])
    

    def socket_callback(name, m):
        global msg, ctr, startCtr, threshold, enabled
        print(name, m)
        if name == "counter" and enabled == True:
            ctr = int(m)
            if startCtr == -1 or ctr < startCtr:
                startCtr = ctr

            if ctr > startCtr + threshold - 1:
                call_the_seals()
                startCtr = ctr

        elif name == "stuff" and m != None:
            msg = [m] + msg[:2]
        elif name == "threshold":
            threshold = int(m)

            if ctr > startCtr + threshold - 1:
                call_the_seals()
                startCtr = ctr
        elif name == "reset":
            kill_the_seals()
        elif name =="enabled":
            enabled = bool(m)

        update_label()


    t = threading.Thread(target=run, args=(socket_callback,))
    update_label()
    t.start()




