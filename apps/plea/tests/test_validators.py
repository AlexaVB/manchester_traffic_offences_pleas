from datetime import date, timedelta

from django.test import TestCase
from django import forms
from django.forms import ValidationError

from ..models import Court, Case
from ..standardisers import standardise_urn
from ..validators import *


class TestValidators(TestCase):
    urls = 'defendant.tests.urls'

    def setUp(self):
        self.court06 = Court.objects.create(
            court_code="0000",
            region_code="06",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="court@example.org",
            submission_email="court@example.org",
            plp_email="plp@example.org",
            enabled=True,
            test_mode=False)

        self.court02 = Court.objects.create(
            court_code="0000",
            region_code="02",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="court@example.org",
            submission_email="court@example.org",
            plp_email="plp@example.org",
            enabled=True,
            test_mode=False)

        self.court05 = Court.objects.create(
            court_code="0000",
            region_code="05",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="court@example.org",
            submission_email="court@example.org",
            plp_email="plp@example.org",
            enabled=True,
            test_mode=False)

        self.court10 = Court.objects.create(
            court_code="0000",
            region_code="10",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="court@example.org",
            submission_email="court@example.org",
            plp_email="plp@example.org",
            enabled=True,
            test_mode=False)

        self.court17 = Court.objects.create(
            court_code="0000",
            region_code="17",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="court@example.org",
            submission_email="court@example.org",
            plp_email="plp@example.org",
            enabled=True,
            test_mode=False)

        self.court20 = Court.objects.create(
            court_code="0000",
            region_code="20",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="court@example.org",
            submission_email="court@example.org",
            plp_email="plp@example.org",
            enabled=True,
            test_mode=False)

        self.court32 = Court.objects.create(
            court_code="0000",
            region_code="32",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="court@example.org",
            submission_email="court@example.org",
            plp_email="plp@example.org",
            enabled=True,
            test_mode=False)

        self.court41 = Court.objects.create(
            court_code="0000",
            region_code="41",
            court_name="test court",
            court_address="test address",
            court_telephone="0800 MAKEAPLEA",
            court_email="court@example.org",
            submission_email="court@example.org",
            plp_email="plp@example.org",
            enabled=True,
            test_mode=False)

    def test_urn_valid_database(self):
        self.court06.validate_urn = True
        self.court06.save()

        case = Case(urn="06QQ0000000", sent=False)
        case.save()

        self.assertTrue(is_urn_valid("06/QQ/00000/00"))

    def test_is_valid_urn_format(self):
        good_urns = [
            "02TJDS0479/15/0014AP",
            "05/A1/12345/01",
            "10/A1/12345/01",
            "17/A1/12345/01",
            "20/AA/12345/01",
            "20/A1/12345/01",
            "06/AA/12345/99",
            "06/AA/0012345/99",
            "06/bb/1234567/12",
            "06/JJ/50563/14",
            "06/JJ/50534/14",
            "06AB/12345/99",
            "06AB12345/99",
            "06AB123456711",
            "32C90000000",
            "41/A9/00000/00"
        ]
        bad_urns = [
            "123",
            "AAA",
            "0/BB/12345/99",
            "0/BB/0012345/99",
            "06/B/12345/99",
            "06/BB/1234/99",
            "06/BB/123456/99",
            "06/BB/12345/9",
            "06/BB/1234567/9",
            "32CC0000000",
            "41/AA/00000/00"
        ]

        for URN in good_urns:
            self.assertTrue(is_urn_valid(URN))

        for URN in bad_urns:
            with self.assertRaises(forms.ValidationError):
                is_urn_valid(URN)

    def test_is_valid_met_urn_format(self):
        good_urns = [
            "02TJDS0479/15/0014AP",
            "02TjDs0479/15/0014aP",
            "02TJ/AA0000/00/0015aa",
            "02TJ/AA0000/00/00151aa",
            "02TJ/AA0000/00/00151aaa",
            "02TJC00000000aa",
            "02TJC00000000aaa",
            "02TJ0000000000000000aa",
            "02TJ0000000000000000aaa",
            "02TJ0000000/00aa",
            "02TJ0000000/00aaa"
        ]

        for URN in good_urns:
            test_urn = standardise_urn(URN)
            self.assertTrue(is_urn_valid(test_urn))

    def test_date_is_in_past(self):
        yesterday = date.today() - timedelta(1)

        self.assertTrue(is_date_in_past(yesterday))

    def test_date_is_not_in_past(self):
        tomorrow = date.today() + timedelta(1)

        with self.assertRaises(forms.ValidationError):
            is_date_in_past(tomorrow)

    def test_date_is_in_future(self):
        tomorrow = date.today() + timedelta(1)

        self.assertTrue(is_date_in_future(tomorrow))

    def test_date_is_not_in_future(self):
        yesterday = date.today() - timedelta(1)

        with self.assertRaises(forms.ValidationError):
            is_date_in_future(yesterday)

    def test_date_is_in_last_28_days(self):
        yesterday = date.today() - timedelta(1)

        self.assertTrue(is_date_in_last_28_days(yesterday))

    def test_date_is_not_in_last_28_days(self):
        more_than_28_days_ago = date.today() - timedelta(30)

        with self.assertRaises(forms.ValidationError):
            is_date_in_last_28_days(more_than_28_days_ago)

    def test_date_is_in_next_6_months(self):
        tomorrow = date.today() + timedelta(1)

        self.assertTrue(is_date_in_next_6_months(tomorrow))

    def test_date_is_not_in_next_6_months(self):
        more_than_6_months_from_now = date.today() + timedelta(200)

        with self.assertRaises(forms.ValidationError):
            is_date_in_next_6_months(more_than_6_months_from_now)
