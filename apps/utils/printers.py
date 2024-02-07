import logging


def show_query_sets(d: dict) -> None:
    logging.info(" Query sets ".center(100, "*"))
    for i in d:
        logging.info(i)
    logging.info("*" * 100)
