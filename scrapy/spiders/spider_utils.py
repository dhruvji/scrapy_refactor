
from __future__ import annotations
import re
import logging

from typing import (
    Any,
    Dict,
    Iterable,
    Callable,
    Optional,
    TypeVar,
    Union,
)

from scrapy.http import Request, Response
from scrapy.spiders import Spider


logger = logging.getLogger(__name__)

_T = TypeVar("_T")

def _identity(x: _T) -> _T:
    return x


def _identity_process_request(
    request: Request, response: Response
) -> Optional[Request]:
    return request


def _get_method(
    method: Union[Callable, str, None], spider: Spider
) -> Optional[Callable]:
    if callable(method):
        return method
    if isinstance(method, str):
        return getattr(spider, method, None)
    return None

def regex(x: Union[re.Pattern[str], str]) -> re.Pattern[str]:
    if isinstance(x, str):
        return re.compile(x)
    return x


def iterloc(it: Iterable[Dict[str, Any]], alt: bool = False) -> Iterable[str]:
    for d in it:
        yield d["loc"]

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and "alternate" in d:
            yield from d["alternate"]