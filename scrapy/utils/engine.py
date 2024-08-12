"""Some debugging functions for working with the Scrapy engine"""

from __future__ import annotations

# used in global tests code
from time import time  # noqa: F401
from typing import TYPE_CHECKING, Any, List, Tuple

if TYPE_CHECKING:
    from scrapy.core.engine import ExecutionEngine


def _get_engine_status(engine: ExecutionEngine) -> List[Tuple[str, Any]]:
    """Return a report of the current engine status"""
    tests = [
        "time()-engine.start_time",
        "len(engine.downloader.active)",
        "engine.scraper.is_idle()",
        "engine.spider.name",
        "engine.spider_is_idle()",
        "engine.slot.closing",
        "len(engine.slot.inprogress)",
        "len(engine.slot.scheduler.dqs or [])",
        "len(engine.slot.scheduler.mqs)",
        "len(engine.scraper.slot.queue)",
        "len(engine.scraper.slot.active)",
        "engine.scraper.slot.active_size",
        "engine.scraper.slot.itemproc_size",
        "engine.scraper.slot.needs_backout()",
    ]

    checks: List[Tuple[str, Any]] = []
    for test in tests:
        try:
            checks += [(test, eval(test))]  # nosec
        except Exception as e:
            checks += [(test, f"{type(e).__name__} (exception)")]

    return checks


def _format_engine_status(engine: ExecutionEngine) -> str:
    checks = _get_engine_status(engine)
    s = "Execution engine status\n\n"
    for test, result in checks:
        s += f"{test:<47} : {result}\n"
    s += "\n"

    return s


def _print_engine_status(engine: ExecutionEngine) -> None:
    print(_format_engine_status(engine))
