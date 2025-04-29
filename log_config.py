import logging
import sys
import os


def configure_logging():

    log_file_name_full = (sys.argv[0]).split("/")
    log_file_name = (log_file_name_full[-1]).split(".")[-2]

    log_file = f"log/{log_file_name}.log"
    log_directory = os.path.dirname(log_file)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
