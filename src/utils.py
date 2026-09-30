"""Utils module for configuration related items"""

import pathlib
import json
from intents import (
    fallback,
    suggestions,
    api_handler,
    welcome,
    kendra, duplicate_tax_form,
    faq_intents,
    handle_feedback,
    intent_utils
)


class Handler:
    """Handler for lambda events"""

    # pylint: disable=too-many-instance-attributes
    # A lot of state is maintained here, so a few extra is OK

    def __init__(self, event, logencryption):
        """Initializer"""
        config_dir = pathlib.Path(__file__).parent.resolve()
        with open(config_dir.joinpath("config.json"),
                  'r',
                  encoding="utf-8") as configin:
            self.config = json.load(configin)
        self.intent_type = "Close"
        self.state = "Fulfilled"
        self.slot_to_elicit = None
        self.session_attributes = {}
        self.answer_attributes = None
        self.messages = []
        self.contexts = []
        self.event = event
        self.session = event['sessionState']
        self.current_intent = self.session['intent']['name']
        self.slots = self.session['intent']['slots']
        self.intent_diverted = False
        self.req_attributes = None
        self.pru_env = event.get('requestAttributes', {}).get('x_pru_env', None)
        self.logencryption = logencryption

    def process(self):
        """Process Lex intents"""
        # pylint: disable=too-many-branches
        intent = self.current_intent

        if intent == 'WelcomeIntent':
            welcome.welcome(self)
        elif intent.startswith('FAQ'):
            faq_intents.process_faq_intent(self, intent)
        elif intent == 'QuestionAnswered-Yes':
            faq_intents.process_faq_intent(self, intent)
        elif intent == 'StoreFeedbackDesc':
            handle_feedback.store_feedback_desc(self)
        elif intent == 'QuestionAnswered-MoreInfo':
            faq_intents.process_question_more_info(self)
        elif intent == 'QuestionAnswered-No':
            faq_intents.process_question_not_answered(self)
        elif intent == 'FeedbackIntent':
            handle_feedback.feedback(self)
        elif intent == 'StoreFeedback':
            handle_feedback.store_feedback(self)
        elif intent == 'FallbackIntent':
            fallback.process_fallback(self)
        elif intent == 'MoreSuggestions':
            suggestions.process_more_suggestions(self)
        elif intent == 'Kendra':
            kendra.process_kendra(self)
        elif intent == 'ProcessCustDupTaxFormIntent':
            duplicate_tax_form.process_dup_tax_form(self)
        elif intent == 'HandleProxyReqResponseIntent':
            api_handler.handle_proxy_req_response(self)
        else:
            intent_utils.log_error(self.event["sessionId"], "unsupported intent",
                                   f"Intent: {intent} not supported")
            intent_utils.add_message(self, self.config["messages"]["unsupported_intent"])
            intent_utils.add_message(self, intent_utils.payload_suggestions(
                self.config['main_menu'],
                self.config), "CustomPayload")

        return self.generate_response()

    def generate_response(self):
        """Generate response after all processing is done"""
        res = {
            "sessionState": {
                "activeContexts": self.contexts,
                "dialogAction": {
                    "slotToElicit": self.slot_to_elicit,
                    "type": self.intent_type,
                },
            },
            "messages": self.messages,
            "sessionId": self.event['sessionId']
        }

        self.session_attributes['Lex_Intent_Name'] = self.current_intent
        self.session_attributes['Lex_Intent_Score'] = \
            self.event['interpretations'][0].get("nluConfidence", 0)

        persistent_attr = ["feedback_rating", "feedback_comments"]
        existing_attributes = self.session.get('sessionAttributes', {})
        for key in persistent_attr:
            if not existing_attributes.get(key, {}):
                continue  # not there, so not needed
            if self.session_attributes.get(key, {}):
                continue  # no need to add here because it was added before
            self.session_attributes[key] = existing_attributes[key]

        history = self.event['inputTranscript'].replace(',', '') + ', ' \
                  + existing_attributes.get('Utterance_History', '')
        self.session_attributes['Utterance_History'] = ','.join(history.split(',')[:30])
        res["sessionState"]["sessionAttributes"] = self.session_attributes

        res['requestAttributes'] = self.req_attributes

        if self.intent_type not in ("Delegate", "ElicitIntent"):
            res["sessionState"]["intent"] = {
                "name": self.current_intent,
                "state": self.state,
                "slots": self.slots,
            }

        return res
