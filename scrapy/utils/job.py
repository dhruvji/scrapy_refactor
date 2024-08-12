from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional
import logging

if TYPE_CHECKING:
    from scrapy.settings import BaseSettings


def job_dir(settings: BaseSettings, log: bool = False) -> Optional[str]:
    path: Optional[str] = settings["JOBDIR"]
    if not path:
        if log:
            logging.info("No JOBDIR setting found.")
        return None
    
    job_dir_path = Path(path)
    
    if not job_dir_path.exists():
        if log:
            logging.info(f"Creating job directory at: {job_dir_path}")
        job_dir_path.mkdir(parents=True)
    else:
        if log:
            logging.info(f"Job directory already exists at: {job_dir_path}")
    
    return path
