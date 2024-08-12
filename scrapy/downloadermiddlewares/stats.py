from __future__ import annotations

from typing import TYPE_CHECKING, Union

from scrapy.exceptions import NotConfigured
from scrapy.utils.python import global_object_name
from scrapy.utils.request import request_httprepr
from scrapy.utils.downloadermiddlewares import get_header_size, get_status_size

if TYPE_CHECKING:
    # typing.Self requires Python 3.11
    from typing_extensions import Self

    from scrapy import Request, Spider
    from scrapy.crawler import Crawler
    from scrapy.http import Response
    from scrapy.statscollectors import StatsCollector


class DownloaderStats:
    def __init__(self, stats: StatsCollector):
        self.stats: StatsCollector = stats

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        if not crawler.settings.getbool("DOWNLOADER_STATS"):
            raise NotConfigured
        assert crawler.stats
        return cls(crawler.stats)

    def process_request(
        self, request: Request, spider: Spider
    ) -> Union[Request, Response, None]:
        self.stats.inc_value("downloader/request_count", spider=spider)
        self.stats.inc_value(
            f"downloader/request_method_count/{request.method}", spider=spider
        )
        reqlen = len(request_httprepr(request))
        self.stats.inc_value("downloader/request_bytes", reqlen, spider=spider)
        return None

    def process_response(
        self, request: Request, response: Response, spider: Spider
    ) -> Union[Request, Response]:
        self.stats.inc_value("downloader/response_count", spider=spider)
        self.stats.inc_value(
            f"downloader/response_status_count/{response.status}", spider=spider
        )
        reslen = (
            len(response.body)
            + get_header_size(response.headers)
            + get_status_size(response.status)
            + 4
        )
        # response.body + b"\r\n"+ response.header + b"\r\n" + response.status
        self.stats.inc_value("downloader/response_bytes", reslen, spider=spider)
        return response

    def process_exception(
        self, request: Request, exception: Exception, spider: Spider
    ) -> Union[Request, Response, None]:
        ex_class = global_object_name(exception.__class__)
        self.stats.inc_value("downloader/exception_count", spider=spider)
        self.stats.inc_value(
            f"downloader/exception_type_count/{ex_class}", spider=spider
        )
        return None
