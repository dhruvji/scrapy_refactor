from typing import Dict, List, Tuple, Union
from twisted.web import http
from scrapy.utils.python import to_bytes

def get_header_size(
    headers: Dict[str, Union[List[Union[str, bytes]], Tuple[Union[str, bytes], ...]]]
) -> int:
    size = 0
    for key, value in headers.items():
        if isinstance(value, (list, tuple)):
            for v in value:
                size += len(b": ") + len(key) + len(v)
    return size + len(b"\r\n") * (len(headers.keys()) - 1)


def get_status_size(response_status: int) -> int:
    return len(to_bytes(http.RESPONSES.get(response_status, b""))) + 15
    # resp.status + b"\r\n" + b"HTTP/1.1 <100-599> "