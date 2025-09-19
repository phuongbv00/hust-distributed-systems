import socket
import sys
import threading
from contextlib import closing


class QuitException(Exception):
    pass


STORE = {}
SERVER_START_TS = None
TOTAL_SERVED = 0

_STORE_LOCK = threading.Lock()
_TOTAL_SERVED_LOCK = threading.Lock()


def run_server(host: str, port: int) -> None:
    import time
    global SERVER_START_TS
    SERVER_START_TS = time.time()
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen(5)
        print(f"[server] listening on {host}:{port}")
        try:
            while True:
                conn, addr = srv.accept()
                with closing(conn):
                    print(f"[server] connection from {addr}")
                    buf = b""
                    while True:
                        try:
                            chunk = conn.recv(4096)
                        except ConnectionResetError:
                            print("[server] connection reset by peer during recv")
                            break
                        if not chunk:
                            break
                        buf += chunk
                        while b"\n" in buf:
                            line, _, buf = buf.partition(b"\n")
                            text = line.decode("utf-8", errors="replace").rstrip("\r")
                            if text == "":
                                continue
                            print(f"[server] received: {text!r}")
                            try:
                                reply = _handle_request(text)
                                try:
                                    conn.sendall((reply + "\n").encode("utf-8"))
                                except BrokenPipeError:
                                    print("[server] client closed before send")
                                    break
                                print(f"[server] replied: {reply!r}")
                            except QuitException:
                                try:
                                    conn.sendall("200 OK bye\n".encode("utf-8"))
                                except BrokenPipeError:
                                    print("[server] client closed before send")
                                print("[server] shutting down...")
                                return
        except KeyboardInterrupt:
            print("[server] shutting down...")


def _handle_command(cmd: str, args: list[str]) -> str:
    if cmd == "GET":
        if len(args) < 1:
            return "400 BAD_REQUEST"
        key = args[0]
        if key in STORE:
            return f"200 OK {STORE[key]}"
        else:
            return "404 NOT_FOUND"
    elif cmd == "PUT":
        if len(args) < 2:
            return "400 BAD_REQUEST"
        key = args[0]
        value = " ".join(args[1:])
        with _STORE_LOCK:
            created = key not in STORE
            STORE[key] = value
        return "201 CREATED" if created else "200 OK"
    elif cmd == "DEL":
        if len(args) < 1:
            return "400 BAD_REQUEST"
        key = args[0]
        with _STORE_LOCK:
            if key in STORE:
                del STORE[key]
                existed = True
            else:
                existed = False
        if existed:
            return "204 NO_CONTENT"
        else:
            return "404 NOT_FOUND"
    elif cmd == "STATS":
        import time
        global SERVER_START_TS
        if SERVER_START_TS is None:
            uptime_s = 0
        else:
            uptime_s = int(time.time() - SERVER_START_TS)
        return f"200 OK keys={len(STORE)} uptime={uptime_s}s served={TOTAL_SERVED}"
    elif cmd == "QUIT":
        raise QuitException()
    else:
        return "400 BAD_REQUEST"


def _handle_request(request: str):
    global TOTAL_SERVED
    with _TOTAL_SERVED_LOCK:
        TOTAL_SERVED += 1
    try:
        line = request.strip()
        if not line:
            return "400 BAD_REQUEST"
        parts = line.split()
        if len(parts) < 2:
            return "400 BAD_REQUEST"
        version, cmd, args = parts[0], parts[1], parts[2:]
        if version != "KV/1.0":
            return "426 UPGRADE_REQUIRED"
        cmd = cmd.upper()
        return _handle_command(cmd, args)
    except Exception as e:
        if isinstance(e, QuitException):
            raise e
        return f"500 SERVER_ERROR {str(e)}"


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 9000
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port, must be an integer")
            sys.exit(1)
    run_server(host, port)
