
import loguru
import time
from datetime import date
from pathlib import Path

logger = loguru.logger


def log_file() -> str:
    file_name = f'{str(date.today())}_{str(int(time.time()))}.log'
    file_path = Path('./logs').joinpath(file_name)
    return file_path


logger.add(log_file(),level= 'DEBUG')
