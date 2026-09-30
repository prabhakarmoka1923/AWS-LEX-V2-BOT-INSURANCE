"""Module to handle kendra implementation"""

from . import intent_utils


def process_kendra(self):
    """Process when the intent is Kendra intent"""
    req_attribute = self.event["requestAttributes"]
    answer = req_attribute[self.config["params"]["kendra_ans_1"]]
    intent_utils.add_message(self, answer)
    kendra_resp = self.event["sessionState"]["intent"]["kendraResponse"]
    result_item = kendra_resp["resultItems"][0]
    self.answer_attributes = result_item["documentAttributes"]
    kendra_attr = self.answer_attributes
    if len(kendra_attr) == 1 and kendra_attr[0]["key"] == "intent_name":
        val = kendra_attr[0]["value"]["stringValue"]
        if val.find("Casual_Talk") == -1:
            intent_utils.add_message(self, intent_utils.payload_suggestions(
                self.config['self_service_suggestions'],
                self.config), "CustomPayload")
            intent_utils.context_add(self, "question_answered_yes")
            intent_utils.context_add(self, "question_answered_no")

    for document_attribute in kendra_attr:
        parse_kendra_attributes(self, document_attribute)


def parse_kendra_attributes(self, payload):
    """
    Process Kendra result document attributes

    Args:
        payload: response from kendra
    """
    messages = self.config["messages"]

    def add_message():
        menu_help_msg = "Great. I'm here to help whenever you need me.\n\n" \
                        + messages["menu_options"]
        intent_utils.add_message(self, menu_help_msg)
        intent_utils.add_message(self, intent_utils.payload_suggestions(['Go back to Main Menu'],
                                                          self.config), "CustomPayload")

        reg_help_msg = messages["register_digital_service"]
        intent_utils.add_message(self, intent_utils.payload_build("text", self.config,
                                            intent_utils.simple_parse_custom_markdown(self,
                                                                                      reg_help_msg)
                                            ), "CustomPayload")
        opt = self.config['self_service_options']
        intent_utils.add_message(self, intent_utils.payload_suggestions(opt, self.config),
                          "CustomPayload")
        self_help_msg = messages['your_feedback_is_valued_self_help']
        intent_utils.add_message(self, intent_utils.payload_build("text", self.config,
                                            intent_utils.simple_parse_custom_markdown(self,
                                                                                      self_help_msg)
                                            ), "CustomPayload")

    key = payload["key"]
    if key == "suggestions":
        parse_kendra_process_suggestions(self, payload)
    elif key in ["question_answered", "more_information"]:
        parse_kendra_question_answered(self, payload)
    elif key == "intent_name":
        value = payload["value"]["stringValue"]
        feedback_intents = ["FAQOtherFeedbackIntent",
                            "FAQOtherScenariosThanksIntent",
                            "QuestionAnswered-Yes"]
        if value in feedback_intents:
            session_attributes = self.session.get("sessionAttributes", {})
            stored_rating = session_attributes.get("feedback_rating", "")
            self.messages = []
            if stored_rating == "0":
                add_message()
            elif stored_rating in ["1", "2", "3", "4", "5"]:
                add_message()
            else:
                intent_utils.add_message(self, intent_utils.payload_build("feedback", self.config,
                                                            messages["please_rate_experience_msg"]),
                                  "CustomPayload")
                intent_utils.context_add(self, "store-feedback")
        elif value == "FAQOtherMenuIntent":
            intent_utils.context_add(self, "more_suggestions")


def parse_kendra_process_suggestions(self, payload):
    """Process suggestions for payload when key is suggestions"""
    value = payload["value"]["stringListValue"]
    intent_utils.add_message(self, intent_utils.payload_suggestions(value, self.config),
                      "CustomPayload")


def parse_kendra_question_answered(self, payload):
    """Process suggestions when question is answered w. more info"""
    has_suggestions = any(item["key"] == "suggestions"
                          for item in self.answer_attributes)
    has_more_information = payload["value"]["stringValue"]
    more_suggestions_list = [item["value"]["stringValue"]
                             for item in self.answer_attributes
                             if item["key"] == "more_suggestions"]
    if more_suggestions_list:
        more_suggestions = more_suggestions_list[0]
        for item in self.answer_attributes:
            if item["key"] == "more_suggestions":
                more_suggestions = item["value"]["stringValue"]
        has_more_information += ",Show more options"
        content = {"more_suggestions": more_suggestions}
        intent_utils.context_add(self, "more_suggestions", content)
    else:
        has_more_information += ",I'm ready to move on"

    if has_suggestions:
        content = {"noSuggestions": has_more_information}
        intent_utils.context_add(self, "question_answered", content)
        return
    if has_more_information == "TRUE":
        self.messages = []
        intent_utils.add_message(self, intent_utils.payload_build("assistanceMessages",
                                                                  self.config),
                          "CustomPayload")
        intent_utils.context_add(self, "question_answered")
        intent_utils.context_add(self, "store-feedback")
    elif has_more_information == "Contact_Us":
        intent_utils.add_message(self, intent_utils.payload_build("question_answered", self.config),
                          "CustomPayload")
        intent_utils.context_add(self, "question_answered_yes")
        intent_utils.context_add(self, "question_answered_no")
        content = {"text": has_more_information}
        intent_utils.context_add(self, "question_answered_more_info", content)
    else:
        intent_utils.add_message(self, intent_utils.payload_build("question_answered", self.config),
                          "CustomPayload")
        intent_utils.context_add(self, "question_answered_yes")
        intent_utils.context_add(self, "question_answered_no")
        content = {"suggestions": has_more_information}
        intent_utils.context_add(self, "question_answered_more_info", content)
