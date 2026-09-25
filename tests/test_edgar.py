from unittest.mock import patch, MagicMock
import pytest
from src.edgar import ticker_to_cik

# Fake version of the SEC JSON — small enough to read at a glance
FAKE_TICKERS = {
    "0": {"cik_str": 320193,  "ticker": "AAPL", "title": "Apple Inc."},
    "1": {"cik_str": 886986,  "ticker": "TECK", "title": "Teck Resources Ltd"},
    "2": {"cik_str": 1,       "ticker": "TINY", "title": "Tiny CIK Corp"},
}


def fake_response(data):
    """Build a mock requests.Response that returns `data` from .json()."""
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = data
    return mock


@patch("src.edgar.requests.get")
def test_known_ticker_returns_correct_cik(mock_get):
    mock_get.return_value = fake_response(FAKE_TICKERS)
    assert ticker_to_cik("AAPL") == "0000320193"


@patch("src.edgar.requests.get")
def test_lookup_is_case_insensitive(mock_get):
    mock_get.return_value = fake_response(FAKE_TICKERS)
    assert ticker_to_cik("teck") == "0000886986"


@patch("src.edgar.requests.get")
def test_unknown_ticker_raises_value_error(mock_get):
    mock_get.return_value = fake_response(FAKE_TICKERS)
    with pytest.raises(ValueError, match="ZZZZ"):
        ticker_to_cik("ZZZZ")


@patch("src.edgar.requests.get")
def test_cik_is_always_10_digits(mock_get):
    mock_get.return_value = fake_response(FAKE_TICKERS)
    cik = ticker_to_cik("TINY")   # cik_str = 1, needs 9 leading zeros
    assert len(cik) == 10
    assert cik == "0000000001"
