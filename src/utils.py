import contextlib
import time

from loguru import logger


@contextlib.contextmanager
def timer(name):
    start = time.time()

    yield

    elapsed_time = "%.10f" % (time.time() - start)

    logger.info(f"{name}={elapsed_time}, status=succeeded")
