import datetime as dt
import json

from django.core import mail
from django.test import TestCase

from mock import Mock, patch

from apps.plea.models import CourtEmailCount, CourtEmailPlea
from apps.receipt.models import ReceiptLog
from apps.receipt.process import (extract_data_from_email, InvalidFormatError,
                                  process_receipts)


class TestEmailSubjectProcessing(TestCase):

    def setUp(self):

        self.failed_email_subject = "Receipt (Failed) RE: ONLINE PLEA: 66/XX/0050782/14 DOH: 2014-11-07 XXXXXX Xxxxxx"
        self.passed_email_subject = "Receipt (Passed) RE: FILED! ONLINE PLEA: 06/xa/0051925/14 DOH: 2014-10-31 XXXXXX xxxxx"

        self.email_body_valid = """
        Random content.
        <<<makeaplea-ref: 1/1>>>
        Random content.
        """

        self.mock_email = Mock(body=self.email_body_valid,
                               subject=self.failed_email_subject)

    def test_failed_match(self):
        self.mock_email.subject = self.failed_email_subject

        plea_id, count_id, status, urn, doh = \
            extract_data_from_email(self.mock_email)

        self.assertEquals(status, "Failed")

    def test_passed_match(self):
        self.mock_email.subject = self.passed_email_subject

        plea_id, count_id, status, urn, doh = \
            extract_data_from_email(self.mock_email)

        self.assertEquals(status, "Passed")

    def test_error_match(self):

        self.mock_email.subject = 'a totally invalid email subject'

        with self.assertRaises(InvalidFormatError):
            extract_data_from_email(self.mock_email)

    def test_email_body_valid(self):
        plea_id, count_id, status, urn, doh = \
            extract_data_from_email(self.mock_email)

        self.assertEquals(plea_id, 1)
        self.assertEquals(count_id, 1)

    def test_email_body_invaild(self):

        self.mock_email.body = "This is an invalid body"

        with self.assertRaises(InvalidFormatError):
            extract_data_from_email(self.mock_email)


class TestProcessReceipts(TestCase):

    def setUp(self):
        mail.outbox = []

        self.urn = "00/AA/0000000/00"
        self.doh = dt.datetime.now()+dt.timedelta(5)

        context_data = {
            'case': {
                'urn': self.urn
            }
        }

        self.email_audit = CourtEmailPlea.objects.create(
            urn=self.urn,
            hearing_date=self.doh,
            status="sent",
            dict_sent=json.dumps(context_data)
        )

        self.email_count = CourtEmailCount.objects.create(
            hearing_date=self.doh,
            total_pleas=1,
            total_guilty=1,
            total_not_guilty=0
        )

        patcher = patch('apps.receipt.process.get_receipt_emails')
        self.addCleanup(patcher.stop)
        self.get_emails_mock = patcher.start()

    def _get_email_mock(self, body, subject):

        email = Mock()
        email.body = body
        email.subject = subject

        return email

    def _get_context_mock(self, **kwargs):
        """
        Mock the get_receipt_emails context manager
        """

        inner_mock = Mock()
        inner_mock.__enter__ = Mock(**kwargs)
        inner_mock.__exit__ = Mock(return_value=False)

        return inner_mock

    def test_exception_is_logged(self):

        email_obj_mock = Mock()
        email_obj_mock.fetch = Mock(side_effect=IOError("Broken"))

        self.get_emails_mock.return_value = \
            self._get_context_mock(return_value=[email_obj_mock])

        process_receipts()

        self.assertEquals(ReceiptLog.objects.all().count(), 1)
        log = ReceiptLog.objects.latest('id')

        self.assertEquals(log.status, ReceiptLog.STATUS_ERROR)
        self.assertIn('Broken', log.status_detail)

    def test_query_to_date_is_previous_query_from_date(self):
        pass

    def test_success_responses_are_recorded(self):

        ref = "<<<makeaplea-ref: {}/{}>>>"\
            .format(self.email_audit.id, self.email_count.id)

        subject = "Receipt (Passed) RE: FILED! ONLINE PLEA: {} DOH: {}"\
            .format(self.urn, self.doh.strftime("%G-%m-%d"))

        email_obj_mock = self._get_email_mock(ref, subject)

        self.get_emails_mock.return_value = \
        self._get_context_mock(return_value=[email_obj_mock])

        process_receipts()

        self.assertEquals(ReceiptLog.objects.all().count(), 1)
        log = ReceiptLog.objects.latest('id')
        self.assertEquals(log.total_success, 1)
        self.assertEquals(log.total_emails, 1)
        self.assertEquals(log.total_failed, 0)

    def test_failed_responses_are_recorded(self):
        ref = "<<<makeaplea-ref: {}/{}>>>"\
            .format(self.email_audit.id, self.email_count.id)

        subject = "Receipt (Failed) RE: ONLINE PLEA: {} DOH: {}"\
            .format(self.urn, self.doh.strftime("%G-%m-%d"))

        email_obj_mock = self._get_email_mock(ref, subject)

        self.get_emails_mock.return_value = \
        self._get_context_mock(return_value=[email_obj_mock])

        process_receipts()

        self.assertEquals(ReceiptLog.objects.all().count(), 1)
        log = ReceiptLog.objects.latest('id')
        self.assertEquals(log.total_emails, 1)
        self.assertEquals(log.total_success, 0)
        self.assertEquals(log.total_failed, 1)

    def test_mismatched_ref_id(self):
        ref = "<<<makeaplea-ref: {}/{}>>>"\
            .format(self.email_audit.id, self.email_count.id+1)

        subject = "Receipt (Failed) RE: ONLINE PLEA: {} DOH: {}"\
            .format(self.urn, self.doh.strftime("%G-%m-%d"))

        email_obj_mock = self._get_email_mock(ref, subject)

        self.get_emails_mock.return_value = \
        self._get_context_mock(return_value=[email_obj_mock])

        process_receipts()

        log = ReceiptLog.objects.latest('id')

        self.assertEquals(log.total_emails, 1)
        self.assertEquals(log.total_failed, 0)
        self.assertEquals(log.total_errors, 1)

    def test_invalid_email_subjects_are_ignored_but_logged(self):
        ref = "<<<makeaplea-ref: {}/{}>>>"\
            .format(self.email_audit.id, self.email_count.id+1)

        subject = "gibberish"

        email_obj_mock = self._get_email_mock(ref, subject)

        self.get_emails_mock.return_value = \
        self._get_context_mock(return_value=[email_obj_mock])

        process_receipts()

        log = ReceiptLog.objects.latest('id')

        self.assertEquals(log.total_emails, 1)
        self.assertEquals(log.total_failed, 0)
        self.assertEquals(log.total_errors, 1)

    def test_records_changed_on_changed_doh(self):
        """
        We can't complete this test due to missing hearing times in
        the HMCTS receipt emails
        """

    def test_records_changed_on_changed_urn(self):
        updated_urn = "00/BB/0000000/00"

        ref = "<<<makeaplea-ref: {}/{}>>>"\
            .format(self.email_audit.id, self.email_count.id)

        subject = "Receipt (Passed) RE: FILED! ONLINE PLEA: {} DOH: {}"\
            .format(updated_urn, self.doh.strftime("%G-%m-%d"))

        email_obj_mock = self._get_email_mock(ref, subject)

        self.get_emails_mock.return_value = \
        self._get_context_mock(return_value=[email_obj_mock])

        process_receipts()

        log = ReceiptLog.objects.latest('id')
        self.assertEquals(log.total_emails, 1)
        self.assertEquals(log.total_success, 1)

        email_audit = CourtEmailPlea.objects.get(pk=self.email_audit.id)

        self.assertEquals(email_audit.urn, updated_urn)

        self.assertIn(self.urn, email_audit.status_info)
        self.assertIn("URN CHANGED!", email_audit.status_info)

        data = json.loads(email_audit.dict_sent)
        self.assertEquals(data['case']['urn'], updated_urn)

    def test_monitoring_email_is_sent_when_enabled(self):

        self.get_emails_mock.return_value = \
        self._get_context_mock(return_value=[])

        with self.settings(RECEIPT_ADMIN_EMAIL_ENABLED=True):
            process_receipts()

        self.assertEquals(len(mail.outbox), 1)