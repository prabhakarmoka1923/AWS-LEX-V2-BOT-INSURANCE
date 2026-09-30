"""Module to handle the Proxy response for API calls"""

from . import duplicate_tax_form as dup_tax_form
from . import intent_utils


def handle_proxy_req_response(self):
    """Handle Proxy response for one source api call"""
    res_type = intent_utils.get_interpreted_slots(self.slots, 'type')
    if res_type == "client":
        dup_tax_form.handle_client_search_response(self)
    elif res_type == "doc search":
        dup_tax_form.handle_doc_search_response(self)
    elif res_type == "mail tax":
        dup_tax_form.handle_reprint_forms_response(self)

    else:
        sessn_id = self.event["sessionId"]
        intent_utils.log_error(sessn_id, "error while executing request attributes from proxy",
                               res_type)
        msg = self.config["messages"]["technical_issue"]
        intent_utils.add_message(self, msg)
        intent_utils.add_message(self, intent_utils.payload_suggestions(
        self.config['main_menu'],
        self.config), "CustomPayload")

    self.intent_type = "Close"
    self.state = "Fulfilled"
