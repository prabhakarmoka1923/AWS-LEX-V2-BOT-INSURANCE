"""Module to handle FQAs related functions"""

from . import intent_utils
from . import kendra
from . import fallback

FAQ_CSV_XREF = intent_utils.read_faq_data()


def process_faq_intent(self, intent):
    """Process FAQ intent ensuring that the ***_topic_slot is filled"""
    topic_slots = [key for key in self.slots.keys()
                   if key.endswith('_topic_slot')]
    main_slots = [key for key in topic_slots if self.slots[key]]
    all_filled = len(main_slots) == len(topic_slots)
    # intent = self.current_intent

    # Add context for Casual talk intents
    if intent.startswith('FAQCasualTalk'):
        intent_utils.context_add(self, "more_suggestions")
    if intent.startswith('FAQNOSLOT_') or not topic_slots:
        answer = FAQ_CSV_XREF.get(intent)
    elif not (all_filled or intent.startswith('FAQCasualTalk') or
              intent.startswith('FAQOther')):
        fallback.process_fallback(self)
        return
    elif intent.startswith('FAQSIMP_'):
        # Example: Go from FAQSIMP_TaxForms_Intent to FAQSIMP_TaxForms
        prefix = '_'.join(intent.split('_')[:2])
        value = intent_utils.get_interpreted_slots(self.slots, main_slots[0])
        answer = FAQ_CSV_XREF.get(f"{prefix}_{value}")
    else:
        answer = FAQ_CSV_XREF.get(intent)

    if answer:
        process_faq_from_csv(self, answer)
        # Example: If Utterance is above 100 characters and Between 40-60%
        # Confidence, bot asks user to shorten response or call the CC
        if self.event['interpretations'][0]['intent']['name'] \
                == intent:
            if len(self.event['inputTranscript']) > 100 and 0.40 \
                    <= self.event['interpretations'][0]['nluConfidence'] \
                    <= 0.60:
                intent_utils.add_message(self, self.config["prompts_for_retries"][3])
    else:
        fallback.process_fallback(self)


def process_question_more_info(self):
    """Process when the intent is question_answered_more_info"""
    for context in self.session['activeContexts']:
        if context["name"] == "question_answered_more_info":
            if context["contextAttributes"].get("suggestions", {}):
                txt = self.config["messages"]["alternative_options"]
                opts = context['contextAttributes']['suggestions'].split(
                    ",")
                intent_utils.add_message(self, txt)
                intent_utils.add_message(self, intent_utils.payload_suggestions(opts, self.config),
                                  "CustomPayload")
            elif context["contextAttributes"].get("text", {}):
                txt = self.config["messages"]["contact_us"]
                intent_utils.add_message(self, txt)
                intent_utils.add_message(self,
                                  intent_utils.payload_build("assistanceMessages", self.config),
                                  "CustomPayload")
                intent_utils.context_add(self, "question_answered")
                intent_utils.context_add(self, "store-feedback")
        elif context["name"] == "more_suggestions":
            opts = context['contextAttributes']['more_suggestions']
            content = {"more_suggestions": opts}
            intent_utils.context_add(self, "more_suggestions", content)


def process_question_not_answered(self):
    """Process when the intent is question_answered_no"""
    intent_utils.add_message(self, self.config["messages"]["please_give_feedback"])
    intent_utils.context_add(self, "store-feedback-desc")


def process_faq_from_csv(self, answer):
    """Process an answer for FAQ when it is from CSV"""
    intent_utils.add_message(self, answer["_answer"])

    keys = ['intent_name', 'question_answered', 'more_suggestions']
    secondary_keys = ['suggestions']

    if len([key for key in keys + secondary_keys if answer[key]]) == 1:
        if not self.current_intent.startswith("FAQCasualTalk"):
            intent_utils.add_message(self, intent_utils.payload_suggestions(
                self.config['self_service_suggestions'],
                self.config), "CustomPayload")
            intent_utils.context_add(self, "question_answered_yes")
            intent_utils.context_add(self, "question_answered_no")

    self.answer_attributes = [
        {"key": key, "value": {"stringValue": answer[key]}}
        for key in keys if answer[key]]

    for key in secondary_keys:
        if answer[key]:
            value = [val.strip() for val in answer[key].split(',')]
            self.answer_attributes.append(
                {"key": key, "value": {"stringListValue": value}})

    for payload in self.answer_attributes:
        kendra.parse_kendra_attributes(self, payload)
