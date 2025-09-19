import argparse
import socket
import sys
from contextlib import closing


def _send_message(host: str, port: int, message: str, timeout: float = 5.0) -> str:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        data = (message.rstrip("\r\n") + "\n").encode("utf-8")
        sock.sendall(data)
        buf = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf += chunk
            if b"\n" in buf:
                line, _, _ = buf.partition(b"\n")
                buf = line
                break
        return buf.decode("utf-8", errors="replace").strip()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="KV/1.0 TCP client")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9000, help="Server port (default: 9000)")

    subparsers = parser.add_subparsers(dest="cmd", required=False)

    get_p = subparsers.add_parser("get", help="GET <key>")
    get_p.add_argument("key")

    put_p = subparsers.add_parser("put", help="PUT <key> <value>")
    put_p.add_argument("key")
    put_p.add_argument("value")

    del_p = subparsers.add_parser("del", help="DEL <key>")
    del_p.add_argument("key")

    subparsers.add_parser("stats", help="STATS")
    subparsers.add_parser("quit", help="QUIT")

    args = parser.parse_args(argv)

    if args.cmd is None:
        parser.print_help()
        return 1

    if args.cmd == "get":
        msg = f"KV/1.0 GET {args.key}\n"
    elif args.cmd == "put":
        if args.value:
            value = " ".join(args.value)
        else:
            parser.print_help()
            return 1
        msg = f"KV/1.0 PUT {args.key} {value}\n"
    elif args.cmd == "del":
        msg = f"KV/1.0 DEL {args.key}\n"
    elif args.cmd == "stats":
        msg = "KV/1.0 STATS\n"
    elif args.cmd == "quit":
        msg = "KV/1.0 QUIT\n"
    else:
        parser.print_help()
        return 1

    try:
        response = _send_message(args.host, args.port, msg)
        print(response)
        return 0
    except Exception as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
