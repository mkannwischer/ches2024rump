#!/usr/bin/env python3
import http.server, urllib.parse, threading, string, time, sys, socketserver, hashlib

token = 'r3m7oafMN38vjYbn'
path = '/ches24'
adminpath = '/636bca3b39fd4defc3f17070030f4547'

powbits = 18
nonces = set()
def check_pow(s):
    h = int.from_bytes(hashlib.sha256(s.encode()).digest(), 'little')
    if h % 2**powbits:
        return False
    if h in nonces:
        return False
    nonces.add(h)
    print(nonces)
    return True

################################################################

code = '''

    const the_form = document.getElementById('the_form');
    const the_button = document.getElementById('the_button');
    var random;
    the_form.addEventListener('submit', (event) => submitPow(event));
    function sha256(str) {
        var buffer = new TextEncoder("utf-8").encode(str)
        return crypto.subtle.digest("SHA-256", buffer).then(function(hash) {
            return hash
        })
    }

    function randombytes(length) {
        var result           = '';
        var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }
    function isSmall(value){
        value = new Int32Array(value)[0] & POW_MASK; 
        return value == 0;
    }
    async function findSolution(){
        the_button.setAttribute('disabled', '');
        the_result.innerHTML = "<b>Computing PoW. please wait</b>";
        do {
            random = randombytes(32);
            hash = await sha256(random);
        } while (!isSmall(hash));
        
        the_result.innerHTML = "";
        the_button.removeAttribute('disabled');
    }

    async function submitPow(){
        const response = await fetch('/ches24/increment-counter?pow='+random, { method: 'POST'});
        findSolution();
    }
    findSolution();

'''.replace("POW_MASK", hex(2**powbits-1)).strip()


form = f'''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title>CHES 2024 Rump Session</title>
    <body>
        <h1>Welcome to the CHES 2024 Rump Session</h1>
        <noscript style="margin-bottom:1ex;font-weight:bold;color:red">This needs JavaScript.</noscript>
        <form id="the_form" action="javascript:void(0)">
            <div id="the_result"></div>
            <input type="submit" id="the_button" value="Call the angry seals!!!"/ style="min-width: 400px; min-height:100px;>
        </form>

        <script>
            {code}
        </script>
'''.strip()

adminform = f'''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title>CHES 2024 Rump Session Admin</title>
    <body>
        <form action="{adminpath}/set-threshold" method="get">
            threshold: <input type="input" name="threshold" autofocus/>
            <input type="submit" value="submit"/>
        </form>
        <form action="{adminpath}/disable" method="get">
            enable: <input type="checkbox" name="enabled" value="enabled"/>
            <input type="submit" value="submit"/>
        </form>

         <form action="{adminpath}/reset" method="get">
            <input type="submit" value="reset ctr and kill the seals"/>
        </form>
'''.strip()

class HTTPServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True

class HTTPHandler(http.server.BaseHTTPRequestHandler):

    def log_message(*_):
        return

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'not found')

    def send_303(self, loc):
        self.send_response(303)
        self.send_header('Location', loc)
        self.end_headers()

    def send_418(self, s):
        self.send_response(418)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(s)

    def send_form(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(form.encode())

    def do_GET(self):
        try:
            url = urllib.parse.urlparse(self.path)
            if url.path.rstrip('/') == path:
                return self.send_form()
            elif urllib.parse.unquote(url.path).rstrip('/') == adminpath:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(adminform.encode())
            elif urllib.parse.unquote(url.path) == f'{adminpath}/set-threshold':
                data = urllib.parse.parse_qs(url.query)
                set_threshold(int(data['threshold'][0]))
                return self.send_303(urllib.parse.quote(adminpath))
            elif urllib.parse.unquote(url.path) == f'{adminpath}/disable':
                data = urllib.parse.parse_qs(url.query)
                set_enable('enabled' in data)
                return self.send_303(urllib.parse.quote(adminpath))
            elif urllib.parse.unquote(url.path) == f'{adminpath}/reset':
                reset_ctr()
                return self.send_303(urllib.parse.quote(adminpath))
            else:
                return self.send_404()
        except Exception as e:
            print(f'\x1b[39m{e}\x1b[0m', file=sys.stderr)

    def do_POST(self):
        try:
            url = urllib.parse.urlparse(self.path)
            clen = int(self.headers['Content-Length'])
            data = urllib.parse.parse_qs(url.query)
            if url.path == f'{path}/increment-counter':
                if 'pow' not in data:
                    return self.send_303(path)
                if check_pow(data['pow'][0]):
                    increment_counter()
                else:
                    self.send_418('invalid PoW')
                return self.send_303(path)
            else:
                return self.send_404()
        except Exception as e:
            print(f'\x1b[39m{e}\x1b[0m', file=sys.stderr)

################################################################

mutex = threading.Lock()
sock = None
stuff = None
threshold = 5
counter = 0
enabled=True

class TCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    def shutdown_request(self, req):    # keep connection open
        pass

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(5)
        s = self.request.recv(len(token)).decode(errors='replace')
        if s == token:
            with mutex:
                global sock
                sock = self.request
                print(f'\x1b[33m{sock}\x1b[0m', file=sys.stderr)
                send('stuff', stuff)
                send('threshold', threshold)
                send('counter', counter)
                send('enabled', enabled)

def send(key, val):
    if sock:
        try:
            sock.sendall(f'{key}: {val!r}\n'.encode())
        except ConnectionError:
            pass

def update_stuff(s):
    with mutex:
        global stuff
        stuff = s
        print(f'{stuff!r} {threshold} {counter}', file=sys.stderr)
        send('stuff', stuff)

def set_threshold(t):
    t = int(t)
    if t < 1:
        return  # nope
    with mutex:
        global threshold
        threshold = t
        print(f'{stuff!r} {threshold} {counter}', file=sys.stderr)
        send('threshold', threshold)

def set_enable(e):
    t = bool(e)
    with mutex:
        global enabled
        enabled = t
        print(f'{stuff!r} {threshold} {counter} {enabled}', file=sys.stderr)
        send('enabled', enabled)

def reset_ctr():
    with mutex:
        global counter
        counter = 0
        send('counter', counter)
        send('reset', True)

def increment_counter():
    with mutex:
        global counter
        counter += 1
        print(f'{stuff!r} {threshold} {counter}', file=sys.stderr)
        send('counter', counter)

################################################################

if __name__ == '__main__':

    servers = [
            HTTPServer(('0.0.0.0', 8888), HTTPHandler),   # put behind nginx
            TCPServer(('0.0.0.0', 8889), TCPHandler),
        ]

    threads = [threading.Thread(target=srv.serve_forever) for srv in servers]
    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    for s in servers:
        s.shutdown()

    for t in threads:
        t.join()

