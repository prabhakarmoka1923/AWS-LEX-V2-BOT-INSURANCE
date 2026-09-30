"""Test case for handling kendra search results"""

import os
import json
import unittest
import test_utils
from src.utils import Handler
from src.prulogger import Decrypter
from src.intents import (
    welcome,
    faq_intents,
    fallback,
    handle_feedback,
    duplicate_tax_form,
    kendra,
    api_handler,
    suggestions,
    intent_utils
)


class TestAnnClientBot(unittest.TestCase):
    """"class having test cases"""
    # pylint: disable=too-many-public-methods
    def load_req_resp(self, file_name):
        """Load JSON file with request and response"""
        with open("payloads/" + file_name, encoding='utf-8') as json_fid:
            event = json.load(json_fid)
            return event["request"], event["response"]

    def set_handler_with_encryption(self, event):
        """Setting the Handler object"""
        logencryption = True
        this_handler = Handler(event, logencryption)
        return this_handler

    def setup_conf(self, env):
        """Function to set up configuration"""
        conf = {'dev' : {"SAGE_MAKER_BASEURL": "https://api-dev.prudential.com/co/cdo/public"\
                                                "/annuitiesfaqchatbot/v1/invocations",
                         "SECRET_NAME": "/cdo/lex/lex-proxy/pruxpress-proxy"},
                'qa': {"SAGE_MAKER_BASEURL": "https://api-dev.prudential.com/co/cdo/public"\
                                                "/annuitiesfaqchatbot/v1/invocations",
                       "SECRET_NAME": "/cdo/lex/lex-proxy/pruxpress-proxy-qa"}
                }
        return conf, env

    def load_conf(self):
        """Function to load the configuration"""
        conf, env_to_load = self.setup_conf("dev")
        os.environ['SMARN']= conf.get(env_to_load,{}).get("SECRET_NAME")
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        os.environ['SAGE_MAKER_BASEURL'] = conf.get(env_to_load,{}).get("SAGE_MAKER_BASEURL")

    def get_response(self, handler, test_handler = False):
        """Function to generate response"""
        if test_handler:
            return handler.process()["messages"]
        return handler.generate_response()["messages"]

    def test_event_welcome(self):
        """Testing welcome message"""
        event, expected_resp = self.load_req_resp('event_welcome.json')
        this_handler = self.set_handler_with_encryption(event)
        welcome.welcome(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_menu(self):
        """Testing menu functionality"""
        event, expected_resp = self.load_req_resp('event_menu.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQOtherMenuIntent"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_fallback(self):
        """Testing fallback functionality"""
        self.load_conf()
        event, expected_resp = self.load_req_resp('event_fallback.json')
        this_handler = self.set_handler_with_encryption(event)
        fallback.process_fallback(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_long_fallback(self):
        """Testing fallback functionality"""
        self.load_conf()
        event, expected_resp = self.load_req_resp('event_long_fallback.json')
        this_handler = self.set_handler_with_encryption(event)
        fallback.process_fallback(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_fallback_second_time(self):
        """Testing second fallback"""
        self.load_conf()
        event, expected_resp = self.load_req_resp('event_fallback_second_time.json')
        this_handler = self.set_handler_with_encryption(event)
        fallback.process_fallback(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_submit_feedback_again(self):
        """Testing the scenario of submitting the feedback again"""
        event, expected_resp = self.load_req_resp('event_submit_feedback_again.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQOtherFeedbackIntent"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_feedback(self):
        """Testing feedback flow"""
        event, expected_resp = self.load_req_resp('event_feedback.json')
        this_handler = self.set_handler_with_encryption(event)
        handle_feedback.feedback(this_handler)
        actual_resp =self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_feedback_invalid_rating(self):
        """Testing the flow of storing feedback, invalid rating"""
        event, expected_resp = self.load_req_resp('event_feedback_providing_invalid_rating.json')
        this_handler = self.set_handler_with_encryption(event)
        handle_feedback.store_feedback(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_store_feedback(self):
        """Testing the flow of storing feedback"""
        event, expected_resp = self.load_req_resp('event_store_feedback.json')
        this_handler = self.set_handler_with_encryption(event)
        handle_feedback.store_feedback(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_working_long_utterance(self):
        """Testing fallback with long utterance flow"""
        event, expected_resp = self.load_req_resp('event_long_utterance.json')
        this_handler = self.set_handler_with_encryption(event)
        fallback.process_fallback(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_long_fallback_second_time(self):
        """Testing feedback flow, triggering fallback second time"""
        event, expected_resp = self.load_req_resp('event_long_utterance_second_time.json')
        this_handler = self.set_handler_with_encryption(event)
        fallback.process_fallback(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_more_info_on_topic(self):
        """Testing more info intent"""
        event, expected_resp = self.load_req_resp('event_more_info_on_topic.json')
        this_handler = self.set_handler_with_encryption(event)
        faq_intents.process_question_more_info(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_quest_not_answered(self):
        """Testing scenario, my question not answered"""
        event, expected_resp = self.load_req_resp('event_question_not_answered.json')
        this_handler = self.set_handler_with_encryption(event)
        faq_intents.process_question_not_answered(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_faq_casual_talk(self):
        """Testing casual talk intent"""
        event, expected_resp = self.load_req_resp('event_faq_casual_talk.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQCasualTalkHelpIntent"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_faq_rmd(self):
        """Testing rmd faq"""
        event, expected_resp = self.load_req_resp('event_faq_rmd.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQDoINeedToTakeRMDFromThisAccount"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_interpreted_slot_functions(self):
        """Testing the interpreted slot function"""
        with open("payloads/" + "interpreted_slots.json", encoding='utf-8') as json_fid:
            slots = json.load(json_fid)
        actual_resp = intent_utils.get_interpreted_slots(slots, "ssn")
        self.assertEqual(None, actual_resp)

    def test_event_more_info_on_topic_text(self):
        """Testing more info intent with text in context attrb"""
        event, expected_resp = self.load_req_resp('event_more_info_on_topic_text.json')
        this_handler = self.set_handler_with_encryption(event)
        faq_intents.process_question_more_info(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_more_suggestions(self):
        """Testing more info intent"""
        event, expected_resp = self.load_req_resp('event_more_suggestions.json')
        this_handler = self.set_handler_with_encryption(event)
        suggestions.process_more_suggestions(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_more_suggestions_ready_to_move_on(self):
        """Testing more info intent"""
        event, expected_resp = self.load_req_resp('event_more_suggestions_with_move_on.json')
        this_handler = self.set_handler_with_encryption(event)
        suggestions.process_more_suggestions(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_move_on(self):
        """Testing ready to move on scenario"""
        event, expected_resp = self.load_req_resp('event_move_on.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQOtherScenariosMoveOnIntent"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_form(self):
        """Testing tax form intent"""
        event, expected_resp = self.load_req_resp('event_tax_form.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQSIMP_Generic_Intent"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_form_through_mail(self):
        """Testing tax form functionality"""
        event, expected_resp = self.load_req_resp('event_tax_form_through_mail.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_request_contract(self):
        """Testing tax form functionality, entering contract number"""
        event, expected_resp = self.load_req_resp('event_tax_request_contract.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_request_dob(self):
        """Testing tax form functionality, entering dob"""
        event, expected_resp = self.load_req_resp('event_tax_request_dob.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_request_no_tax_form(self):
        """Testing tax form functionality, entering ssn and there are no tax forms"""
        event, expected_resp = self.load_req_resp('event_tax_request_no_tax_form.json')
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp[0], actual_resp)

    def test_event_tax_request_doc_search_other_resp(self):
        """Testing tax form functionality, entering ssn and getting 500 response code"""
        event, expected_resp = self.load_req_resp('event_tax_request_no_tax_form.json')
        custom_data = {"response": {}, "responseCode": 500}
        event["requestAttributes"]["annuities.TaxDNPQ30Error"] = json.dumps(custom_data)
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp[1], actual_resp)

    def test_event_api_handler_other_scenario(self):
        """Testing tax form functionality, entering ssn and there are no tax forms"""
        event, expected_resp = self.load_req_resp('test_event_api_handler_other_scenario.json')
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_request_ssn_cust_not_found(self):
        """Testing tax form functionality, cust validation failed"""
        event, expected_resp = self.load_req_resp('event_tax_request_cust_not_found.json')
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_request_ssn_cust_validation_other_scenario(self):
        """Testing tax form functionality, cust validation failed other scenario"""
        event, expected_resp = self.load_req_resp\
            ('event_tax_request_cust_validtn_other_scenario.json')
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)


    def test_event_tax_request_proxy(self):
        """Testing tax form functionality, passing cust data to proxy for API call"""
        event, expected_resp = self.load_req_resp('event_tax_form_proxy_hand_over.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_request_no_doc_to_mail(self):
        """Testing tax form functionality, passing cust data to proxy for API call"""
        event, expected_resp = self.\
            load_req_resp('event_tax_form_no_tax_doc_to_mail_edge_scenario.json')
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp[0], actual_resp)

    def test_event_tax_request_other_scenario_mail(self):
        """Testing tax form functionality, passing cust data to proxy for API call"""
        event, expected_resp = self.\
            load_req_resp('event_tax_form_no_tax_doc_to_mail_edge_scenario.json')
        event["requestAttributes"]\
            ["annuities.TaxDNPQ20Response"]= json.dumps({"test":"test"})
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp[1], actual_resp)


    def test_event_tax_request_contract1(self):
        """Testing tax form functionality, entering contract id"""
        event, expected_resp = self.load_req_resp('event_tax_request_contract1.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_request_contract2(self):
        """Testing tax form functionality, entering contract id second time"""
        event, expected_resp = self.load_req_resp('event_tax_request_contract2.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_invalid_date_1(self):
        """Testing tax form functionality, entering invalid date"""
        event, expected_resp = self.load_req_resp('event_tax_invalid_date1.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_invalid_date_2(self):
        """Testing tax form functionality, entering invalid date 2nd attempt"""
        event, expected_resp = self.load_req_resp('event_tax_invalid_date2.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_invalid_ssn_1(self):
        """Testing tax form functionality, entering invalid ssn"""
        event, expected_resp = self.load_req_resp('event_tax_invalid_ssn1.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_invalid_ssn_2(self):
        """Testing tax form functionality, entering invalid ssn 2nd attempt"""
        event, expected_resp = self.load_req_resp('event_tax_invalid_ssn2.json')
        this_handler = self.set_handler_with_encryption(event)
        duplicate_tax_form.process_dup_tax_form(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_store_feedback_desc(self):
        """Testing store feedback functionality"""
        event, expected_resp = self.load_req_resp('event_store_feedback_desc.json')
        this_handler = self.set_handler_with_encryption(event)
        handle_feedback.store_feedback_desc(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_death_claim(self):
        """Testing filing death claim scenario"""
        event, expected_resp = self.load_req_resp('event_death_claim.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQHowDoIFileDeathClaimIntent"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_i_dont_have_questions(self):
        """Testing filing death claim scenario"""
        event, expected_resp = self.load_req_resp('event_i_dont_have_questions.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQOtherFeedbackIntent"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_withdrawals(self):
        """Testing withdrawals scenario"""
        event, expected_resp = self.load_req_resp('event_withdrawals.json')
        this_handler = self.set_handler_with_encryption(event)
        intent_name = "FAQWithdrawals"
        faq_intents.process_faq_intent(this_handler, intent_name)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_event_withdrawal_kendra(self):
        """Testing kendra intent"""
        event, expected_resp = self.load_req_resp('event_withdrawal_kendra.json')
        this_handler = self.set_handler_with_encryption(event)
        kendra.process_kendra(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_form_mail_all_form_success(self):
        """Testing tax form mail success Tax_DNPQ20 failed"""
        event, expected_resp = self.load_req_resp('event_tax_form_mail_all_form_success.json')
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp[0], actual_resp)

    def test_event_tax_form_all_fail_on_mailing(self):
        """Testing tax form mail success Tax_DNPQ20 failed"""
        event, expected_resp = self.load_req_resp('event_tax_form_mail_all_form_success.json')
        custom_data = [{"2022-1099-INT": "Failed"}, {"2022-1099-R": "Failed"}]
        event["requestAttributes"]["annuities.TaxDNPQ20Response"] = json.dumps(custom_data)
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp[1], actual_resp)

    def test_event_tax_form_partial_success_on_mailing(self):
        """Testing tax form mail partial success Tax_DNPQ20"""
        event, expected_resp = self.load_req_resp('event_tax_form_mail_all_form_success.json')
        custom_data = [{"2022-1099-INT": "Success"}, {"2022-1099-R": "Failed"}]
        event["requestAttributes"]["annuities.TaxDNPQ20Response"] = json.dumps(custom_data)
        this_handler = self.set_handler_with_encryption(event)
        api_handler.handle_proxy_req_response(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp[2], actual_resp)


    def test_event_feedback_yes(self):
        """Testing feedback flow"""
        event, expected_resp = self.load_req_resp('event_feedback_yes.json')
        this_handler = self.set_handler_with_encryption(event)
        handle_feedback.feedback(this_handler)
        actual_resp = self.get_response(this_handler)
        self.assertEqual(expected_resp, actual_resp)

    def test_handler_other_intent(self):
        """Testing scenario of unsupported intent"""
        event, expected_resp = self.load_req_resp('event_other_intent.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_welcome_from_utils(self):
        """Testing welcome message from utils"""
        event, expected_resp = self.load_req_resp('event_welcome.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_menu_from_utils(self):
        """Testing FAQ menu functionality from utils"""
        event, expected_resp = self.load_req_resp('event_menu.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_store_feedback_desc_from_utils(self):
        """Testing store feedback functionality from utils"""
        event, expected_resp = self.load_req_resp('event_store_feedback_desc.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_more_info_on_topic_from_utils(self):
        """Testing more info intent from utils"""
        event, expected_resp = self.load_req_resp('event_more_info_on_topic.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_feedback_from_utils(self):
        """Testing feedback flow from utils"""
        event, expected_resp = self.load_req_resp('event_feedback.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_answered_my_question_from_utils(self):
        """Testing answered my question functionality from utils"""
        event, expected_resp = self.load_req_resp('event_answered_my_question.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_not_answered_my_question_from_utils(self):
        """Testing does not answered my question functionality from utils"""
        event, expected_resp = self.load_req_resp('event_not_answered_my_question.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_store_feedback_from_utils(self):
        """Testing the flow of storing feedback from utils"""
        event, expected_resp = self.load_req_resp('event_feedback_providing_invalid_rating.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_fallback_from_utils(self):
        """Testing fallback functionality"""
        self.load_conf()
        event, expected_resp = self.load_req_resp('event_fallback.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_more_suggestions_from_utils(self):
        """Testing more info intent from utils"""
        event, expected_resp = self.load_req_resp('event_more_suggestions.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_event_withdrawal_kendra_from_utils(self):
        """Testing kendra intent from utils"""
        event, expected_resp = self.load_req_resp('event_withdrawal_kendra.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_request_from_utils(self):
        """Testing tax form functionality from utils"""
        event, expected_resp = self.load_req_resp('event_tax_form_through_mail.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)

    def test_event_tax_proxy_request_from_utils(self):
        """Testing tax form functionality, from utils"""
        event, expected_resp = self.load_req_resp('event_tax_request_no_tax_form.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp = self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp[0], actual_resp)

    def test_event_encryption(self):
        """Testing hybrid encryption decryption"""
        asym_prefix = "enc2201_"
        sym_prefix = "symenc:"
        event, expected_resp = self.load_req_resp('event_encryption.json')
        private_key = test_utils.get_private_key()
        decrypter = Decrypter(private_key)
        encrypted_key = event['SessionEncKey']
        encrypted_key = encrypted_key.replace(asym_prefix, "")
        decrypted_key = decrypter.decrypt(encrypted_key)
        decrypted_data = test_utils.decrypt_json(event, decrypted_key, sym_prefix)
        self.assertEqual(decrypted_data, expected_resp)

    def test_event_lex_timeout_message(self):
        """Testing lex timeout message scenario"""
        event, expected_resp = self.load_req_resp('event_lex_timeout.json')
        this_handler = self.set_handler_with_encryption(event)
        actual_resp =self.get_response(this_handler, test_handler=True)
        self.assertEqual(expected_resp, actual_resp)


if __name__ == "__main__":
    unittest.main()
