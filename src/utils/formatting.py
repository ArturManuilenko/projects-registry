from typing import Optional
from dateutil import parser


def custom_time(seconds: int) -> Optional[str]:
    """Method for convert seconds to format like '1h30m'"""
    if seconds is None:
        return None
    result = ''
    if seconds // 604800:                       # weeks
        result += str(seconds // 604800) + 'w'
        seconds -= 604800 * (seconds // 604800)
    if seconds // 86400:                        # days
        result += str(seconds // 86400) + 'd'
        seconds -= 86400 * (seconds // 86400)
    if seconds // 3600:                         # hourse
        result += str(seconds // 3600) + 'h'
        seconds -= 3600 * (seconds // 3600)
    if seconds % 3600 // 60:                    # minutes
        result += str(seconds % 3600 // 60) + 'm'
        seconds -= 3600 * (seconds % 3600 // 60)
    return result


def custom_date(date_iso: str) -> Optional[str]:
    """ Method for convert date from iso format to MSK format"""
    if date_iso is None:
        return None
    try:
        return str(parser.parse(date_iso).date().strftime("%d.%m.%Y"))
    except Exception:
        return None
