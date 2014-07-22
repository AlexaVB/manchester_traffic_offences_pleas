import datetime

from django.test import TestCase

from plea.views import PleaOnlineForms


class TestMultiPleaForms(TestCase):
    def setUp(self):
        self.session = {}
        self.request_context = {}

        self.plea_stage_pre_data_1_charge = {"about": {"date_of_hearing": "2015-01-01",
                                                       "urn_0": "00",
                                                       "urn_1": "AA",
                                                       "urn_2": "0000000",
                                                       "urn_3": "00",
                                                       "name": "Charlie Brown",
                                                       "number_of_charges": "1"}}

        self.plea_stage_pre_data_3_charges = {"about": {"date_of_hearing": "2015-01-01",
                                                       "urn_0": "00",
                                                       "urn_1": "AA",
                                                       "urn_2": "0000000",
                                                       "urn_3": "00",
                                                       "name": "Charlie Brown",
                                                       "number_of_charges": "3"}}

    def test_about_stage_bad_data(self):
        form = PleaOnlineForms("about", "plea_form_step", self.session)
        response = form.load(self.request_context)
        response = form.save({}, self.request_context)

        self.assertEqual(len(form.current_stage.forms[0].errors), 4)

    def test_about_stage_good_data(self):
        form = PleaOnlineForms("about", "plea_form_step", self.session)
        response = form.load(self.request_context)
        response = form.save({"date_of_hearing": "2015-01-01",
                              "urn_0": "00",
                              "urn_1": "AA",
                              "urn_2": "0000000",
                              "urn_3": "00",
                              "name": "Charlie Brown",
                              "number_of_charges": "1"},
                             self.request_context)

        self.assertEqual(response.status_code, 302)

    def test_plea_stage_bad_data_single_charge(self):
        self.session.update(self.plea_stage_pre_data_1_charge)
        form = PleaOnlineForms("plea", "plea_form_step", self.session)

        mgmt_data = {"form-TOTAL_FORMS": "1",
                     "form-INITIAL_FORMS": "0",
                     "form-MAX_NUM_FORMS": "1000"}
        mgmt_data.update({"form-0-guilty": "",
                          "form-0-mitigations": "",
                          "understand": ""})

        # no form data, just the management stuff
        form.save(mgmt_data, self.request_context)

        self.assertEqual(len(form.current_stage.forms[0].errors), 1)
        self.assertEqual(len(form.current_stage.forms[1].errors[0]), 1)

    def test_plea_stage_good_data_single_charge(self):
        self.session.update(self.plea_stage_pre_data_1_charge)
        form = PleaOnlineForms("plea", "plea_form_step", self.session)

        mgmt_data = {"form-TOTAL_FORMS": "1",
                     "form-INITIAL_FORMS": "0",
                     "form-MAX_NUM_FORMS": "1"}

        mgmt_data.update({"form-0-guilty": "guilty",
                          "form-0-mitigations": "lorem ipsum 1",
                          "understand": "True"})

        response = form.save(mgmt_data, self.request_context)

        self.assertEqual(response.status_code, 302)

    def test_plea_stage_bad_data_multiple_charges(self):
        self.session.update(self.plea_stage_pre_data_1_charge)
        form = PleaOnlineForms("plea", "plea_form_step", self.session)

        mgmt_data = {"form-TOTAL_FORMS": "2",
                     "form-INITIAL_FORMS": "0",
                     "form-MAX_NUM_FORMS": "1000"}

        mgmt_data.update({"form-0-guilty": "guilty",
                          "form-0-mitigations": "lorem ipsum 1",
                          "understand": "True"})

        response = form.save(mgmt_data, self.request_context)

        self.assertEqual(len(form.current_stage.forms[1].errors[0]), 0)
        self.assertEqual(len(form.current_stage.forms[1].errors[1]), 1)

    def test_plea_stage_good_data_multiple_charges(self):
        self.session.update(self.plea_stage_pre_data_1_charge)
        form = PleaOnlineForms("plea", "plea_form_step", self.session)

        mgmt_data = {"form-TOTAL_FORMS": "2",
                     "form-INITIAL_FORMS": "0",
                     "form-MAX_NUM_FORMS": "1000"}

        mgmt_data.update({"form-0-guilty": "guilty",
                          "form-0-mitigations": "lorem ipsum 1",
                          "form-1-guilty": "guilty",
                          "form-1-mitigations": "lorem ipsum 1",
                          "understand": "True"})

        response = form.save(mgmt_data, self.request_context)

        self.assertEqual(response.status_code, 302)

    def test_review_stage_loads(self):
        pass

    def test_complete_stage_loads(self):
        pass

    def test_reviewsenderror_stage_loads(self):
        pass

    def test_email_error_redirects_to_reviewsenderror_stage(self):
        pass

    def test_successful_completion_single_charge(self):
        fake_session = {}
        request_context = {}

        form = PleaOnlineForms("about", "plea_form_step", fake_session)
        response = form.load(request_context)
        response = form.save({"date_of_hearing": "2015-01-01",
                              "urn_0": "00",
                              "urn_1": "AA",
                              "urn_2": "0000000",
                              "urn_3": "00",
                              "name": "Charlie Brown",
                              "number_of_charges": "1"},
                             request_context)

        self.assertEqual(response.status_code, 302)

        form = PleaOnlineForms("plea", "plea_form_step", fake_session)
        response = form.load(request_context)

        mgmt_data = {"form-TOTAL_FORMS": "1",
                     "form-INITIAL_FORMS": "0",
                     "form-MAX_NUM_FORMS": "1000"}

        mgmt_data.update({"form-0-guilty": "guilty",
                          "form-0-mitigations": "lorem ipsum 1",
                          "understand": "True"})

        response = form.save(mgmt_data, request_context)

        self.assertEqual(response.status_code, 302)

        form = PleaOnlineForms("review", "plea_form_step", fake_session)
        response = form.load(request_context)
        response = form.save({},
                             request_context)

        self.assertEqual(response.status_code, 302)

        form = PleaOnlineForms("complete", "plea_form_step", fake_session)
        response = form.load(request_context)

        self.assertEqual(fake_session["about"]["date_of_hearing"], datetime.datetime(2015, 1, 1, 0, 0))
        self.assertEqual(fake_session["about"]["urn"], "00/AA/0000000/00")
        self.assertEqual(fake_session["about"]["name"], "Charlie Brown")
        self.assertEqual(fake_session["about"]["number_of_charges"], 1)
        self.assertEqual(fake_session["plea"]["PleaForms"][0]["guilty"], "guilty")
        self.assertEqual(fake_session["plea"]["PleaForms"][0]["mitigations"], "lorem ipsum 1")
        self.assertEqual(fake_session["plea"]["understand"], True)

    def test_successful_completion_multiple_charges(self):
        fake_session = {}
        request_context = {}

        form = PleaOnlineForms("about", "plea_form_step", fake_session)
        response = form.load(request_context)
        response = form.save({"date_of_hearing": "2015-01-01",
                              "urn_0": "00",
                              "urn_1": "AA",
                              "urn_2": "0000000",
                              "urn_3": "00",
                              "name": "Charlie Brown",
                              "number_of_charges": "2"},
                             request_context)

        self.assertEqual(response.status_code, 302)

        form = PleaOnlineForms("plea", "plea_form_step", fake_session)
        response = form.load(request_context)

        mgmt_data = {"form-TOTAL_FORMS": "2",
                     "form-INITIAL_FORMS": "0",
                     "form-MAX_NUM_FORMS": "1000"}

        mgmt_data.update({"form-0-guilty": "guilty",
                          "form-0-mitigations": "lorem ipsum 1",
                          "form-1-guilty": "guilty",
                          "form-1-mitigations": "lorem ipsum 2",
                          "understand": "True"})

        response = form.save(mgmt_data, request_context)

        self.assertEqual(response.status_code, 302)

        form = PleaOnlineForms("review", "plea_form_step", fake_session)
        response = form.load(request_context)
        response = form.save({},
                             request_context)

        self.assertEqual(response.status_code, 302)

        form = PleaOnlineForms("complete", "plea_form_step", fake_session)
        response = form.load(request_context)

        self.assertEqual(fake_session["about"]["date_of_hearing"], datetime.datetime(2015, 1, 1, 0, 0))
        self.assertEqual(fake_session["about"]["urn"], "00/AA/0000000/00")
        self.assertEqual(fake_session["about"]["name"], "Charlie Brown")
        self.assertEqual(fake_session["about"]["number_of_charges"], 2)
        self.assertEqual(fake_session["plea"]["PleaForms"][0]["guilty"], "guilty")
        self.assertEqual(fake_session["plea"]["PleaForms"][0]["mitigations"], "lorem ipsum 1")
        self.assertEqual(fake_session["plea"]["PleaForms"][1]["guilty"], "guilty")
        self.assertEqual(fake_session["plea"]["PleaForms"][1]["mitigations"], "lorem ipsum 2")
        self.assertEqual(fake_session["plea"]["understand"], True)