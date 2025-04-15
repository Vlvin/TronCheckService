from database.main import get_records_count

TEST_ADDRESS = "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"


def test_database_population():
    count_before = get_records_count()

    # asyncio.run(check_address(GetAddressInput(address=TEST_ADDRESS)))

    count_after = get_records_count()
    assert count_after == count_before  # + 1
