# SimpleFileRemoteSink.py
#
#   part of EfiPy2
#
# Copyright (C) 2025 MaxWu efipy.core@gmail.com
#   GPL-2.0
#
import struct
import socket
import sys
import zlib
import os

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = socket.gethostbyname(socket.gethostname())
    return ip

def receive_file(port):
    local_ip = get_local_ip()
    print(f"Listening on IP: {local_ip}, port: {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"Waiting for connection on port {port}...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            raw = conn.recv(4)
            if len(raw) < 4:
                print("Failed to receive filename length.")
                return
            filename_len = struct.unpack('!I', raw)[0]

            filename = conn.recv(filename_len).decode('utf-8')

            raw = conn.recv(4)
            if len(raw) < 4:
                print("Failed to receive file size.")
                return
            filesize = struct.unpack('!I', raw)[0]

            with open(filename, 'wb') as f:
                received = 0
                checksum = 0
                while received < filesize:
                    chunk = conn.recv(min(4096, filesize - received))
                    if not chunk:
                        break
                    f.write(chunk)
                    checksum = zlib.crc32(chunk, checksum)
                    received += len(chunk)
                    percent = int((received / filesize) * 100)
                    print(f"{percent:3d}% ({received} of {filesize})", end='\r')

            print(f"\nFile '{filename}' received successfully.")
            recv_checksum = struct.unpack(">I", conn.recv(4))[0]
            if recv_checksum == checksum:
                print("Checksum matched.")
            else:
                print(f"Checksum mismatch! (received: {recv_checksum:#010x}, calculated: {checksum:#010x})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Sink.py <TCP Port>")
        sys.exit(1)

    receive_file(int(sys.argv[1]))
