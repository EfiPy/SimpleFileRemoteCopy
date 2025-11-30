# Introduction
Simple File transfer script run in as simple as possible.

SimpleFileRemoteSource.py - File copy to.
```
python SimpleFileRemoteSource.py <host> <TCP port> <file_path>
```
SimpleFileRemoteSink.py - File copy from.
```
python SimpleFileRemoteSink.py <TCP port>
```
# Description
We do not want complex protocol and complex multitask process.

This just do simple file transfer over Network TCP protocol.

# Protocol
```
#pragma pack(1)
struct {
  UINT32 FileNameLenght;                    // Big endian
  UINT8  FileNameBuffer [FileNameLength];
  UINT32 FileLength;                        // Big endian
  UINT8  FileBuff [FileLength];
  UINT32 CRC32;                             // Big endian
}
```
# Working Environment

* UEFI shell
* Windows
* Linux
