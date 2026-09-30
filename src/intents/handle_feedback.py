"""Module to handle the feedback"""

from . import intent_utils


def feedback(self):
    """Process when the intent is feedback i.e. when use wants to
        give feedback/rate the bot"""
    messages = self.config["messages"]
    intent_utils.add_message(self, intent_utils.payload_build("feedback", self.config,
                                                messages["please_rate_experience_msg"]),
                      "CustomPayload")
    intent_utils.context_add(self, "store-feedback")


def store_feedback_desc(self):
    """Process when the intent is store_feedback_desc and when customer
    giving feedback to the bot"""
    messages = self.config["messages"]

    def add_message():
        intent_utils.add_message(self, messages["your_feedback_is_valued"] + "\n\n" \
                          + messages["menu_options"])
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

    self.session_attributes["feedback_comments"] = self.event['inputTranscript']
    # print(f"Feedback-Description {self.event['inputTranscript']}")
    add_message()


def store_feedback(self):
    """Process when the intent is store_feedback"""
    messages = self.config["messages"]
    slots = self.slots

    def add_message():
        intent_utils.add_message(self, messages["your_feedback_is_valued"] + "\n\n" \
                          + messages["menu_options"])
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

    if not slots['FeedbackRating']:
        self.intent_type = "ElicitSlot"
        self.slot_to_elicit = "FeedbackRating"
        self.state = "InProgress"
        intent_utils.context_add(self, "store-feedback")
        intent_utils.add_message(self, messages["please_rate_experience"])
    elif not slots["FeedbackDescription"]:
        rating = intent_utils.get_interpreted_slots(slots, 'FeedbackRating')
        self.session_attributes["feedback_rating"] = rating
        # print(f"Feedback {rating}")
        add_message()
