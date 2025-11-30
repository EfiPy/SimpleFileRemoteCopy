# SimpleFileRemoteSource.py
#
#   part of EfiPy2
#
# Copyright (C) 2025 MaxWu efipy.core@gmail.com
#   GPL-2.0
#
import socket
import struct
import sys
import zlib
import os

def send_file(host, port, file_path):
    with socket.create_connection((host, port)) as s:
        filename = os.path.basename(file_path).encode('utf-8')
        filesize = os.path.getsize(file_path)

        # Send filename length (4 bytes)
        s.sendall(struct.pack('!I', len(filename)))

        # Send filename
        s.sendall(filename)

        # Send file size (4 bytes)
        s.sendall(struct.pack('!I', filesize))

        # Send file content with progress
        sent = 0
        checksum = 0
        with open(file_path, 'rb') as f:
            chunk = f.read(4096)
            while chunk:
                s.sendall(chunk)
                checksum = zlib.crc32(chunk, checksum)
                sent += len(chunk)
                percent = int((sent / filesize) * 100)
                print(f"{percent:3d}% ({sent} of {filesize})", end='\r')
                chunk = f.read(4096)

        print("\nFile sent successfully.")
        s.sendall(struct.pack(">I", checksum))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Source.py <host> <TCP Port> <file_path>")
        sys.exit(1)

    send_file(sys.argv[1], int(sys.argv[2]), sys.argv[3])
