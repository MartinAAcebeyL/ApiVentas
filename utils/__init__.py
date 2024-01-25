from dateutil.relativedelta import relativedelta
from django.utils import timezone

import logging


def get_date_minus_period(period: int, per: str):
    current_date = timezone.now()
    start_date = None
    match per:
        case "day":
            start_date = current_date - relativedelta(days=period)
        case "month":
            start_date = current_date - relativedelta(months=period)
        case "year":
            start_date = current_date - relativedelta(years=period)
        case _:
            raise ValueError("Invalid period")
    return start_date


def show_query_sets(d: dict) -> None:
    logging.info(" Query sets ".center(100, "*"))
    for i in d:
        logging.info(i)
    logging.info("*" * 100)
