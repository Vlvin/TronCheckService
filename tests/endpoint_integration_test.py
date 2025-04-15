# run server
# send few requests
# compare data to what you've sent'
# compare database data to what you've got from request'
from contextlib import contextmanager
from math import ceil
import multiprocessing
import time
from typing import Generator
import dotenv
import requests

from database.main import get_records_count
from main import main
from mytypes import GetAddressOutput, GetLastDataOutput

ELEMENTS_PER_PAGE = int(dotenv.get_key("config.env", "MAX_PER_PAGE"))

SERVER_URL = "http://localhost:8000"

TEST_ADDRESS = (
    "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"  # this is truly correct tron address
)


def waitForServiceStartup(method: str, url: str, timeout: int = 5, *args, **kwargs):
    """Generic wait for url accessibility"""
    start = time.time()
    while True:
        try:
            requests.request(method, url, *args, **kwargs)
            return True
        except Exception:
            if time.time() - start > timeout:
                return False
            time.sleep(0.01)


def waitForServiceShutdown(method: str, url: str, timeout: int = 5, *args, **kwargs):
    """Generic wait for url accessibility"""
    start = time.time()
    while True:
        try:
            requests.request(method, url, *args, **kwargs)
            time.sleep(0.01)
            if time.time() - start > timeout:
                return False
        except Exception:
            return True


@contextmanager
def runServer() -> Generator[None, None, None]:
    """Starts main app and manages to shut it down"""
    server = multiprocessing.Process(target=main)
    try:
        server.start()
        result = waitForServiceStartup(
            "get", f"{SERVER_URL}/get_page", params={"page": 1}
        )
        yield result
    finally:
        server.terminate()
        waitForServiceShutdown("get", f"{SERVER_URL}/get_page", params={"page": 1})


def get_page(page: int, expected_status: int) -> bool:
    with runServer() as result:
        assert result and "Failed to start server"
        response = requests.get(f"{SERVER_URL}/get_page", {"page": page})
        assert response.status_code == expected_status

        answer = response.json()
        print(answer)
        if response.status_code == 200:
            valid_model = GetLastDataOutput.model_validate(answer)
            assert valid_model.page == page
            elements_count = len(valid_model.data)
            assert elements_count <= ELEMENTS_PER_PAGE
            assert elements_count > 0 or get_records_count() == 0


def check_address(address: str, expected_status: int, count_increment: int = 1):
    with runServer() as result:
        assert result and "Failed to start server"
        count = get_records_count()
        response = requests.post(
            f"{SERVER_URL}/check_address",
            json={"address": address},
        )
        assert response.status_code == expected_status
        assert count + count_increment == get_records_count()
        if response.status_code == 200:
            valid_model = GetAddressOutput.model_validate(response.json())
            assert valid_model.account_data.address == address


def test_get_from_correct_page():
    get_page(1, 200)


def test_get_data_from_invalid_page():
    get_page(-1, 500)
    pages = ceil(get_records_count() / ELEMENTS_PER_PAGE)
    get_page(pages, 500)


def test_check_correct_address():
    check_address(TEST_ADDRESS, 200)


def test_check_invalid_address():
    check_address("INVALID_ADDRESS", 500, count_increment=0)
