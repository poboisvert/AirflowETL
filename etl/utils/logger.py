import os
import sys
from loguru import logger
logger.add("logger.log", format="{extra[ip]} {extra[user]} {message}")

format = \
    '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>' \
    ' | ' \
    "<level>{level: <8}</level> | " \
    ' | ' \
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'


logger.add("logger.log", format=format)
