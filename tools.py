import re


def check(v) -> bool:
    return v.__cverify__()


def get_hex(v):
    return v.__get_compiled__()

