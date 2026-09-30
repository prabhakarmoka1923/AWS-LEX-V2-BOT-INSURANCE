"""Duplicate tax form functionality"""

import ast
from . import intent_utils


def process_dup_tax_form(self):
    """
    Handle fulfillment of mail duplicate tax form
    Call customer search api and one source api
    """
    self.session['activeContexts'] = []

    self.session_attributes = self.session.get('sessionAttributes', {})
    cn_prompt_counter = int(self.session_attributes.get('cn_prompt_counter', 0))
    dob_prompt_counter = int(self.session_attributes.get('dob_prompt_counter', 0))
    ssn_prompt_counter = int(self.session_attributes.get('ssn_prompt_counter', 0))

    validation_result = intent_utils.validate_dup_slot(self.event)

    if self.event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:

            self.intent_type = "ElicitSlot"
            self.slot_to_elicit = validation_result['violatedSlot']
            self.state = "InProgress"
            self.contexts.extend(self.session['activeContexts'])

            if validation_result['violatedSlot'] == 'contractId':
                intent_utils.slot_prompt(self,
                                  "contract_number_prompts",
                                  "cn_prompt_counter",
                                  cn_prompt_counter)
            if validation_result['violatedSlot'] == 'dob':
                intent_utils.slot_prompt(self, "dob_prompts",
                                  "dob_prompt_counter",
                                  dob_prompt_counter)
            if validation_result['violatedSlot'] == 'ssn':
                intent_utils.slot_prompt(self, "ssn_prompts",
                                  "ssn_prompt_counter",
                                  ssn_prompt_counter)

        else:
            user_contract_id = \
                self.slots['contractId'].get('value').get('interpretedValue')
            user_dob = self.slots['dob'].get('value').get('interpretedValue')
            user_ssn = self.slots['ssn'].get('value').get('interpretedValue')

            # Requesting proxy to perform customer search api call
            data = {
                "policy_number": user_contract_id,
                "tax_payer_id": user_ssn,
                "birth_date": user_dob
            }
            self.req_attributes = {'clientValidation': str(data)}
            intent_utils.add_message(self, 'Handed over')
            intent_utils.context_add(self, "handle-proxy-response")
            attrbs = ['cn_prompt_counter', 'dob_prompt_counter', 'ssn_prompt_counter']
            intent_utils.reset_session_attrbs(self, attrbs, 0)
            self.intent_type = "Close"
            self.state = "Fulfilled"


def handle_reprint_forms_response(self):
    """Handle Reprint API response from proxy"""
    req_attributes = intent_utils.get_request_attributes(self, 'annuities.TaxDNPQ20Response')
    # Check for non empty request attribute and it should be a list
    if isinstance(req_attributes, list) and req_attributes:
        response, suggestions = generate_forms_final_response(self, req_attributes)
        intent_utils.add_message(self, response)
        intent_utils.add_message(self, intent_utils.payload_suggestions(
            suggestions, self.config), "CustomPayload")
        intent_utils.context_add(self, "question_answered_yes")
        intent_utils.context_add(self, "question_answered_no")
    elif not req_attributes:  # no tax forms available
        intent_utils.add_message(self, self.config["messages"]["no_tax_form"])
        intent_utils.add_message(self, intent_utils.payload_suggestions(
            self.config['show_failure_suggestions'],
            self.config), "CustomPayload")
    else:
        intent_utils.add_message(self, self.config["messages"]["api_failure"])
        intent_utils.add_message(self, intent_utils.payload_suggestions(
            self.config['main_menu'],
            self.config), "CustomPayload")


def handle_doc_search_response(self):
    """Handle Document search API response from proxy"""
    req_attributes = intent_utils.get_request_attributes(self, 'annuities.TaxDNPQ30Error')
    if req_attributes['responseCode'] == 204:
        intent_utils.add_message(self, self.config["messages"]["no_tax_form"])
        intent_utils.add_message(self, intent_utils.payload_suggestions(
            self.config['show_failure_suggestions'],
            self.config), "CustomPayload")
    else:
        intent_utils.add_message(self, self.config["messages"]["api_failure"])
        intent_utils.add_message(self, intent_utils.payload_suggestions(
            self.config['main_menu'],
            self.config), "CustomPayload")


def handle_client_search_response(self):
    """Handle Client search API response from proxy"""
    req_attributes = intent_utils.get_request_attributes(self, 'annuities.clientValidationError')
    response = ast.literal_eval(req_attributes['response'])
    if req_attributes['responseCode'] == 200 and response.get('responseCode', '') == '':
        if response and response.get('messages') is not None:
            intent_utils.add_message(self, self.config["messages"]["cust_not_found"])
            intent_utils.add_message(self, intent_utils.payload_suggestions(
                self.config['show_failure_suggestions'],
                self.config), "CustomPayload")
    else:
        intent_utils.add_message(self, self.config["messages"]["api_failure"])
        intent_utils.add_message(self, intent_utils.payload_suggestions(
            self.config['main_menu'],
            self.config), "CustomPayload")


def generate_forms_final_response(self, req_attributes):
    """Generate form success response on the basis of forms reprinted"""
    success_tax_forms = []
    failed_tax_forms = []
    form_lst_pass = ''
    form_lst_fail = ''

    for tax_form in req_attributes:
        for key, value in tax_form.items():
            form_mailed_lst = self.config["messages"]["form_mailed_lst"]
            year, form_type = key.split('-', 1)
            if value.lower() == "success":
                success_tax_forms.append(key)
                form_lst_pass = form_lst_pass + form_mailed_lst.format(form_type, year)
            else:
                failed_tax_forms.append(key)
                form_lst_fail = form_lst_fail + form_mailed_lst.format(form_type, year)

    if len(req_attributes) == len(success_tax_forms):
        # all forms reprinting success
        response = self.config["messages"]["all_taxform_success"]
        response = response.format(form_lst_pass)
        suggestions = self.config['show_success_suggestions']
    elif len(req_attributes) == len(failed_tax_forms):
        # all form reprinting failed
        response = self.config["messages"]["all_taxform_failed"]
        response = response.format(form_lst_fail)
        suggestions = self.config['show_failure_suggestions']
    elif len(req_attributes) == (len(success_tax_forms) + len(failed_tax_forms)):
        # Some forms reprinted, some failed
        response = self.config["messages"]["some_taxform_success_failed"]
        response = response.format(form_lst_pass, form_lst_fail)
        suggestions = self.config['show_success_suggestions']
    return response, suggestions
