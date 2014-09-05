from __future__ import absolute_import
import unittest

from django.core import mail

from ..email import TemplateAttachmentEmail, send_plea_email


class EmailGenerationTests(unittest.TestCase):
    def setUp(self):
        mail.outbox = []

    def test_template_attachment_sends_email(self):
        email_context = {"URN": "1A2B3C4D5E"}
        email = TemplateAttachmentEmail("test_from@example.org",
                                        "test.html",
                                        "plea/plea_email_attachment.html",
                                        email_context,
                                        "<p>Test Content</p><br><p>{{ URN }}</p>")
        email.send(["test_to@example.org", ],
                   "Subject line",
                   "Body Text")

        self.assertEqual(mail.outbox[0].subject, "Subject line")
        self.assertEqual(mail.outbox[0].body, "Body Text")

    def test_plea_email_sends(self):
        context_data = {"case": {"date_of_hearing": "2014-06-30",
                                 "time_of_hearing": "12:00",
                                 "urn": "cvxcvx89"},
                        "your_details": {"name": "vcx"},
                        "plea": {"PleaForms": [{"mitigations": "test1", "guilty": "guilty"},
                                               {"mitigations": "test2", "guilty": "guilty"}],
                                 "understand": True}}

        send_plea_email(context_data)

        # only expecting 1 email for now, PLP email cancelled for the time being
        self.assertEqual(len(mail.outbox), 2)