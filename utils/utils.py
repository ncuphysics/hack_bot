from datetime import datetime
from pytz import timezone


def get_time() -> datetime:
    return datetime.now(timezone("Asia/Shanghai"))