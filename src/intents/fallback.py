"""Module handling fallback intent"""

import os
from . import (
    faq_intents,
    intent_utils,
    suggestions,
    handle_feedback
)


def process_fallback(self):
    """Process when the intent is fallback intent"""
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    self.intent_type = "ElicitIntent"
    self.state = "InProgress"
    session_attributes = self.session.get("sessionAttributes", {})
    attr = self.session_attributes
    fallback = session_attributes.get("fallbackCount", "")

    event = self.event
    # getting the 2nd top predicted intent
    # scenario: on providing the descriptive feedback to the bot, in few situations
    # even though the context is active, we have seen that the fallback intent
    # is getting triggered which is Lex issue, below is the code to handle this
    second_top_intent = event["interpretations"][1]["intent"]["name"]
    feedback_context_name = "store-feedback-desc"
    if (intent_utils.context_present(self, feedback_context_name) and
        second_top_intent == "StoreFeedbackDesc"):
        handle_feedback.store_feedback_desc(self)

    elif "Lex_Intent_Name" not in session_attributes:
        msg = self.config["messages"]["fallback_timeout_special_case"]
        intent_utils.add_message(self, msg)
        intent_utils.add_message(self,
                            intent_utils.payload_suggestions(self.config['welcome_suggestions'],
                            self.config), "CustomPayload")
        intent_utils.context_add(self, "more_suggestions")
    else:
        if not attr.get('sagemaker_pred', {}):
            utterance_history = self.session.get(
                "sessionAttributes", {}).get('Utterance_History', '')
            sagemaker_pred = intent_utils.get_sagemaker_suggestions(
                                                utterance_history,
                                                self.event['inputTranscript'],
                                                self.event["sessionId"],
                                                os.environ["SAGE_MAKER_BASEURL"]
                                                )
            if sagemaker_pred:
                attr["sagemaker_called"] = True
                intent_utils.log_info(self.event["sessionId"], sagemaker_pred[:5])
                sagemaker_first_pred = sagemaker_pred[0]

                if (sagemaker_first_pred['confidence'] >
                        self.config['sagemaker_endpoint']['confidence_threshold']):
                    attr.pop("sagemaker_called", None)
                    attr["sagemaker_pred"] = True
                    attr["DS_Model_Intent_Name"] = sagemaker_first_pred['intent']
                    attr["DS_Model_Intent_Score"] = \
                        sagemaker_first_pred['confidence']
                    if sagemaker_first_pred['intent'] == "MoreSuggestions":
                        suggestions.process_more_suggestions(self)
                    else:
                        faq_intents.process_faq_intent(self, sagemaker_first_pred['intent'])
                    return

        if not session_attributes:
            attr["fallbackCount"] = 2
            # Example: If Utterance is above 100 characters and Below 40%
            # Confidence, bot asks user to shorten response or call the CC
            fallback_msg = self.config["prompts_for_retries"][0]
            if len(self.event["inputTranscript"]) > 100:
                fallback_msg = self.config["prompts_for_retries"][1]
            intent_utils.add_message(self, fallback_msg)
        elif fallback in ["2", "3"]:
            intent_utils.add_message(self, self.config["prompts_for_retries"][2])
            intent_utils.add_message(self, intent_utils.payload_suggestions(
                ["Main Menu"], self.config), "CustomPayload")
            attr["fallbackCount"] = 3
        else:
            attr["fallbackCount"] = 2
            fallback_msg = self.config["prompts_for_retries"][0]
            if len(self.event["inputTranscript"]) > 100:
                fallback_msg = self.config["prompts_for_retries"][1]
            intent_utils.add_message(self, fallback_msg)

        for context in self.session['activeContexts']:
            if context["timeToLive"]["turnsToLive"] > 0:
                self.contexts.append(context)
