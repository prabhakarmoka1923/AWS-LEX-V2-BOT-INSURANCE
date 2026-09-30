"""Module for the welcome prompt"""

from . import intent_utils


def welcome(self):
    """Handle initial intent request"""
    intent_utils.add_message(self, self.config["messages"]["welcome"])
    intent_utils.add_message(self, intent_utils.payload_suggestions(
        self.config['welcome_suggestions'],
        self.config), "CustomPayload")
    intent_utils.context_add(self, "more_suggestions")
