import socket
import subprocess
import sys
import time
from contextlib import closing

HOST = "127.0.0.1"
PORT = 9001


def start_server():
    proc = subprocess.Popen(
        [sys.executable, "-u", "server.py", HOST, str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    deadline = time.time() + 5
    out_buf = []
    while time.time() < deadline:
        line = proc.stdout.readline().strip() if proc.stdout else ""
        if line:
            out_buf.append(line)
        try:
            with closing(socket.create_connection((HOST, PORT), timeout=0.2)) as s:
                return proc
        except OSError:
            time.sleep(0.05)
            continue
    try:
        proc.terminate()
    except Exception:
        pass
    raise RuntimeError("Server failed to start. Output: \n" + "\n".join(out_buf))


def stop_server(proc: subprocess.Popen):
    if proc.poll() is not None:
        return
    try:
        send_cmd("KV/1.0 QUIT")
        try:
            proc.wait(timeout=2)
            return
        except subprocess.TimeoutExpired:
            pass
    except Exception:
        pass
    try:
        proc.kill()
    except Exception:
        pass


def send_cmd(line: str, timeout: float = 2.0) -> str:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        sock.connect((HOST, PORT))
        sock.sendall((line.rstrip("\r\n") + "\n").encode("utf-8"))
        buf = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
            if b"\n" in buf:
                reply, _, _ = buf.partition(b"\n")
                return reply.decode("utf-8", errors="replace").strip()
        return buf.decode("utf-8", errors="replace").strip()


class TestKVServer:
    @classmethod
    def setup_class(cls):
        cls.proc = start_server()

    @classmethod
    def teardown_class(cls):
        stop_server(cls.proc)

    def test_put_create_returns_201(self):
        resp = send_cmd("KV/1.0 PUT foo bar")
        assert resp == "201 CREATED"

    def test_put_update_returns_200(self):
        resp1 = send_cmd("KV/1.0 PUT ukey val1")
        assert resp1 == "201 CREATED"
        resp2 = send_cmd("KV/1.0 PUT ukey val2")
        assert resp2 == "200 OK"

    def test_get_existing_returns_200_with_value(self):
        send_cmd("KV/1.0 PUT k1 v1")
        resp = send_cmd("KV/1.0 GET k1")
        assert resp == "200 OK v1"

    def test_get_missing_returns_404(self):
        resp = send_cmd("KV/1.0 GET no_such_key")
        assert resp == "404 NOT_FOUND"

    def test_del_existing_returns_204(self):
        send_cmd("KV/1.0 PUT todel v")
        resp = send_cmd("KV/1.0 DEL todel")
        assert resp == "204 NO_CONTENT"

    def test_del_missing_returns_404(self):
        resp = send_cmd("KV/1.0 DEL missing")
        assert resp == "404 NOT_FOUND"

    def test_missing_version_returns_426(self):
        resp = send_cmd("GET key")
        assert resp == "426 UPGRADE_REQUIRED"

    def test_wrong_version_returns_426(self):
        resp = send_cmd("KV/2.0 GET key")
        assert resp == "426 UPGRADE_REQUIRED"

    def test_put_missing_value_returns_400(self):
        resp = send_cmd("KV/1.0 PUT key")
        assert resp == "400 BAD_REQUEST"

    def test_bad_command_returns_400(self):
        resp = send_cmd("KV/1.0 UNKNOWN something")
        assert resp == "400 BAD_REQUEST"

    def test_stats_format(self):
        resp = send_cmd("KV/1.0 STATS")
        assert resp.startswith("200 OK ")
        assert "keys=" in resp and "uptime=" in resp and "served=" in resp
