"""Module to get the suggestions"""

from . import intent_utils


def process_more_suggestions(self):
    """Process more contexts"""
    if self.session_attributes.get('sagemaker_pred'):
        msg = self.config["messages"]["no_suggestions_to_show"]
        intent_utils.add_message(self, msg)
        intent_utils.add_message(self, intent_utils.payload_suggestions(
            self.config['main_menu_different_topic'],
            self.config), "CustomPayload")
    else:
        contexts = [cxt for cxt in self.session.get('activeContexts', [{}])
                    if cxt.get("name", "") == "more_suggestions"]
        if not contexts:
            return

        try:
            opt_string = contexts[0]["contextAttributes"]["more_suggestions"]
            opts = opt_string.split(",")
            opts.append("I'm ready to move on")
        except KeyError:
            opts = self.config["show_more_options"]  # array from config

        msg = self.config["messages"]["show_more_options"]
        payload = intent_utils.payload_suggestions(opts, self.config)
        intent_utils.add_message(self, msg)
        intent_utils.add_message(self, payload, "CustomPayload")
