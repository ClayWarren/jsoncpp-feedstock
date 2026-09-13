import json
import pathlib
import struct
import sys

if sys.argv[1] == "metadata":
    prefix = pathlib.Path(sys.prefix)
    records = list((prefix / "conda-meta").glob("jsoncpp-*.json"))
    assert len(records) == 1, records
    record = json.loads(records[0].read_text())
    assert record["subdir"] == "win-arm64", record
    assert record["sha256"] == "5a2f9bf12650f6b49050179aa789ddeb863812fde3f594eebe33232256b7198b", record
    data = pathlib.Path(sys.executable).read_bytes()
else:
    data = pathlib.Path(sys.argv[2]).read_bytes()
assert data[:2] == b"MZ"
offset = struct.unpack_from("<I", data, 0x3C)[0]
assert data[offset:offset+4] == b"PE\0\0"
assert struct.unpack_from("<H", data, offset+4)[0] == 0xAA64
print("Verified native ARM64 executable and requested package checks")
