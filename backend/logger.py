import logging

formatter = logging.basicConfig(format="[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s")

logger = logging.getLogger("friends")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)