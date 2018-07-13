# coding: utf-8
from piiregex import PiiRegex
import pytest


@pytest.fixture
def pii_regex():
    return PiiRegex()


def test_dates_numeric(pii_regex):
    matching = ["1-19-14", "1.19.14", "1.19.14", "01.19.14"]
    for s in matching:
        assert pii_regex.dates(s) == [s]


def test_dates_verbose(pii_regex):
    matching = [
        "January 19th, 2014",
        "Jan. 19th, 2014",
        "Jan 19 2014",
        "19 Jan 2014",
    ]
    for s in matching:
        assert pii_regex.dates(s) == [s]


def test_times(pii_regex):
    matching = ["09:45", "9:45", "23:45", "9:00am", "9am", "9:00 A.M.", "9:00 pm"]
    for s in matching:
        assert pii_regex.times(s) == [s]


def test_phones(pii_regex):
    matching = [
        "12345678900",
        "1234567890",
        "+1 234 567 8900",
        "234-567-8900",
        "1-234-567-8900",
        "1.234.567.8900",
        "5678900",
        "567-8900",
        "(123) 456 7890",
        "+41 22 730 5989",
        "(+41) 22 730 5989",
        "+442345678900",
    ]
    for s in matching:
        assert pii_regex.phones(s) == [s]


def test_emails(pii_regex):
    matching = ["john.smith@gmail.com", "john_smith@gmail.com", "john@example.net"]
    non_matching = ["john.smith@gmail..com"]
    for s in matching:
        assert pii_regex.emails(s) == [s]
    for s in non_matching:
        assert pii_regex.phones(s) != [s]


def test_ips(pii_regex):
    matching = ["127.0.0.1", "192.168.1.1", "8.8.8.8"]
    for s in matching:
        assert pii_regex.ips(s) == [s]


def test_ipv6s(pii_regex):
    matching = [
        "fe80:0000:0000:0000:0204:61ff:fe9d:f156",
        "fe80:0:0:0:204:61ff:fe9d:f156",
        "fe80::204:61ff:fe9d:f156",
        "fe80:0000:0000:0000:0204:61ff:254.157.241.86",
        "fe80:0:0:0:0204:61ff:254.157.241.86",
        "fe80::204:61ff:254.157.241.86",
        "::1",
    ]
    for s in matching:
        assert pii_regex.ipv6s(s) == [s]


def test_creditcards(pii_regex):
    matching = [
        "0000-0000-0000-0000",
        "0123456789012345",
        "0000 0000 0000 0000",
        "012345678901234",
    ]
    for s in matching:
        assert pii_regex.credit_cards(s) == [s]


def test_btc_addresses(pii_regex):
    matching = [
        "1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2",
        "19P6EYhu6kZzRy9Au4wRRZVE8RemrxPbZP",
        "1bones8KbQge9euDn523z5wVhwkTP3uc1",
        "1Bow5EMqtDGV5n5xZVgdpRPJiiDK6XSjiC",
    ]
    non_matching = [
        "2LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2",
        "19Ry9Au4wRRZVE8RemrxPbZP",
        "1bones8KbQge9euDn523z5wVhwkTP3uc12939",
        "1Bow5EMqtDGV5n5xZVgdpR",
    ]
    for s in matching:
        assert pii_regex.btc_addresses(s) == [s]
    for s in non_matching:
        assert pii_regex.btc_addresses(s) != [s]


def test_street_addresses(pii_regex):
    matching = [
        "checkout the new place at 101 main st.",
        "504 parkwood drive",
        "3 elm boulevard",
        "500 elm street ",
    ]
    non_matching = ["101 main straight"]

    for s in matching:
        # Strings evaluate true.
        assert pii_regex.street_addresses(s)
    for s in non_matching:
        assert pii_regex.street_addresses(s) != [s]


def test_po_boxes(pii_regex):
    matching = ["PO Box 123456", "hey p.o. box 234234 hey"]
    non_matching = ["101 main straight"]

    for s in matching:
        # Strings evaluate true.
        assert pii_regex.po_boxes(s)
    for s in non_matching:
        assert pii_regex.po_boxes(s) == []


def test_zip_codes(pii_regex):
    matching = ["02540", "02540-4119"]
    non_matching = ["101 main straight", "123456"]

    for s in matching:
        # Strings evaluate true.
        assert pii_regex.zip_codes(s)
    for s in non_matching:
        assert pii_regex.zip_codes(s) == []


def test_postcodes(pii_regex):
    matching = ["E1 5JH", "EC1V 2NX", "SE1 1AA", "e15jh", "e151aa"]
    non_matching = ["E1", "ec1v"]

    for s in matching:
        assert pii_regex.postcodes(s)
    for s in non_matching:
        assert pii_regex.postcodes(s) == []


def test_ukphones(pii_regex):
    matching = ["07123123123", "07123 123123"]
    non_matching = ["07123 123123123"]

    for s in matching:
        assert pii_regex.ukphones(s)
    for s in non_matching:
        assert pii_regex.ukphones(s) == []


def test_any_match(pii_regex):
    # This matches a phone number.
    assert pii_regex.any_match('07123 123123') is True
    # This should match nothing.
    assert pii_regex.any_match('asdasdasdasdasd') is False
