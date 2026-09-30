"""Module contains all intent related util functions"""

import re
import csv
import logging
import json
import ast
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
from . import load_secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def read_faq_data():
    """Read FAQ data from data.csv"""
    with open("data.csv", 'r', encoding="utf-8") as data_file:
        reader = csv.DictReader(data_file)
        return {row['intent_name']: row for row in reader}


def payload_build(payload, config, content=None):
    """
    Incrementally build payload for feedback, menu, etc., based on

    Args:
        payload: Chunk of payload so far
        config: config for suggestions content
        content: additional content
    Returns:
        updated version of payload
    """
    data = {"website": {payload: ''}}
    if payload == "question_answered" and content is None:
        data["website"][payload] = config["show_more_info_suggestions"]
    else:
        data["website"][payload] = content if content else True
    return data


def payload_suggestions(suggestions, config):
    """
    Build payload based on suggestions

    Args:
        suggestions: available suggestions for an answer
        config: config object
    Returns:
        A structure appropriate for display of the suggestions
    """
    if "type" in suggestions[0]:
        return {"website": {"suggestions_links": suggestions}}
    if suggestions[0].lower() == "initial suggestions":
        suggestions = config["initial_suggestions"]
    return {"website": {"suggestions": suggestions}}


def log_error(session_id, message, err):
    """This function is to log with logging level as error"""
    log_err = {
        "message": message,
        "sessionId": session_id,
        "body": err
    }
    logger.error(log_err)


def log_info(session_id, message):
    """This function is to log with logging level as info"""
    log_msg = {
        "message": message,
        "sessionId": session_id
    }
    logger.info(log_msg)


def validate_dup_slot(event):
    """
    This function validate slot of process duplicate tax form
    """
    slots = event['sessionState']['intent']['slots']
    if not validate_contract_id(slots):
        return {
            'isValid': False,
            'violatedSlot': 'contractId'
        }

    if not validate_birthdate(slots, event):
        return {
            'isValid': False,
            'violatedSlot': 'dob'
        }
    if not slots['ssn'] or not get_interpreted_slots(slots, 'ssn'):
        return {
            'isValid': False,
            'violatedSlot': 'ssn'
        }

    return {'isValid': True}


def get_interpreted_slots(slots, slot_name):
    """This function is to retrieve interpreted slots"""
    slot_name = slots.get(slot_name)
    value = None
    if not slot_name:
        return value
    slot_name_val = slot_name.get('value')
    if slot_name_val and 'interpretedValue' in slot_name_val:
        value = slot_name_val['interpretedValue']
    return value


def validate_birthdate(slots, event):
    """
    This function validate birthdate slot of process duplicate tax form
    """
    if not slots['dob'] or not get_interpreted_slots(slots, 'dob'):
        return False
    ori_date_lst = slots['dob'].get('value').get('originalValue').split('/')
    original_month = original_date = original_year = 0
    if len(ori_date_lst) == 3:
        try:
            original_month = int(ori_date_lst[0])
            original_date = int(ori_date_lst[1])
            original_year = int(ori_date_lst[2])
            if 1 <= original_month <= 12 and 1 <= original_date <= 31 and \
                    original_year < datetime.today().year:
                return True
        except ValueError as value_error:
            log_error(event["sessionId"], "Invalid date format ", str(value_error))
    return False


def validate_contract_id(slots):
    """
    This function validate contract slot of process duplicate tax form
    """
    if not slots['contractId'] or not get_interpreted_slots(slots, 'contractId'):
        return False
    contract = get_interpreted_slots(slots, 'contractId')
    # defining the minimum number of digits needed in contract number
    minimum_digits = 3
    return 7 <= len(contract) <= 10 and digit_count(contract) >= minimum_digits

def digit_count(contract_id):
    """Function to extract digit count in <contract_id>"""
    digits_in_contract_id = [x for x in contract_id if x.isdigit()]
    return len(digits_in_contract_id)

def get_sagemaker_suggestions(session_text, input_text, session_id, url):
    """Send Utterance history and input text on fallback to sagemaker and get suggestions """
    get_key = load_secret.get_secret()

    input_samples = {
        "input_text": input_text,
        "session_text": ','.join(session_text.split(',')[:10]),  # Get only last 10 Utterances
        "session_id": session_id
    }
    try:
        response = requests.post(
            url=url,
            json=input_samples,
            auth=HTTPBasicAuth(get_key.get('onesource_api_key'),
                               get_key.get('onesource_api_sec')),
            timeout=60
        )
        parsed_response = json.loads(response.content.decode('utf-8'))
        if "predictions" in parsed_response:
            return parsed_response["predictions"]
        log_error(session_id, "Error occured while calling sage maker",
                  "no prediction returned by sage maker")
    except requests.exceptions.Timeout as exc:
        log_error(session_id, "Exception occured while calling sage maker", str(exc))
    except requests.exceptions.RequestException as exc:
        log_error(session_id, "Exception occured while calling sage maker", str(exc))

    return {}


def slot_prompt(self, prompt, counter_name, counter):
    """
    Process prompt on basis of counter

    Args:
        prompt: prompt name
        counter_name: counter name
        counter: integer value of counter name
    """
    if counter < 2:
        add_message(self, self.config[prompt][counter])
        add_message(self, payload_build("inputMasked", self.config,
                                        simple_parse_custom_markdown(self, "Mask after value")),
                    "CustomPayload")
        self.session['sessionAttributes'][counter_name] = counter + 1
    else:
        add_message(self, self.config["messages"]["second_fallback"])
        add_message(self, payload_suggestions(
            self.config['show_failure_suggestions'],
            self.config), "CustomPayload")
        attrbs = ['cn_prompt_counter', 'dob_prompt_counter', 'ssn_prompt_counter']
        reset_session_attrbs(self,
                             attrbs, 0)
        self.intent_type = "Close"
        self.state = "Fulfilled"


def reset_session_attrbs(self, params, value):
    """Reset data stored in session attributes"""
    for item in params:
        self.session['sessionAttributes'][item] = value


def get_request_attributes(self, key):
    """Return parsed data stored in request attributes"""
    req_attributes = self.event["requestAttributes"][key]
    req_attributes = ast.literal_eval(req_attributes)
    return req_attributes


def context_present(self, name):
    """
    Check if context with `name` is present

    Args:
        name: name of the attribute to check in activeContexts
    """
    return any(context['name'] == name
               for context in self.session['activeContexts'])


def set_context(name, context_attributes, turns_to_live=2, time_to_live=180):
    """
    Set intent context and life span (e.g., 2 turns, 180 sec)
    """
    return {
        "name": name, "contextAttributes": context_attributes,
        "timeToLive": {
            "timeToLiveInSeconds": 90 if not time_to_live else time_to_live,
            "turnsToLive": turns_to_live
        }
    }


def context_add(self, key, payload=None, turns=2, ttl=180):
    """
    Add payload based on context
    """
    payload = {} if not payload else payload
    self.contexts.append(set_context(key, payload, turns, ttl))


def add_message(self, content, content_type=None):
    """
    Append content to messages based on content type

    Args:
        content: content to add (can be text, list, etc.)
        content_type: CustomPayload|SSML (optional; default is "PlainText")
    """
    ctype, cont = "PlainText", "Unsupported Content"
    if not content_type or content_type == "PlainText":
        ctype = "PlainText"
        cont = simple_parse_custom_markdown(self, content)
    elif content_type == "CustomPayload":
        ctype, cont = content_type, json.dumps(content)
    elif content_type == "SSML":
        ctype, cont = content_type, content
    self.messages.append({"contentType": ctype, "content": cont})


def simple_parse_custom_markdown(self, raw_text):
    """
    Parse custom markdown like text from CSV and send back to client
    Args:
        raw_text: input raw text
    Returns:
        parsed text (e.g., *hello* becomes <b>hello</b>)
    """
    if self.pru_env is not None and self.pru_env == "Genesys":
        raw_text = re.sub('<hr(.*?)/>', r'\n', raw_text)
        return raw_text
    repl_pattern = r'<a href="\2" target="_blank" role="link" ' + \
                   r'aria-label="\1" tabindex=0>\1</a>'
    img_pattern = r'<img src="\2" alt="\1" style="padding-left:2rem;">'
    res = re.sub(r"\^([^\^]+?)\^", r"<li>\1</li>", raw_text)
    res = re.sub(r'\*(.*?)\*', r'<b>\1</b>', res)
    res = re.sub('_(.*?)_', r'<i>\1</i>', res)
    res = re.sub('\n', '<br>', res)
    res = re.sub(r'!\[(.*?)\]\((.*?)\)', img_pattern, res)
    res = re.sub(r'\[(.*?)]\((.*?)\)', repl_pattern, res)
    # Adding temporarily later will change at the UI side of chatbot
    res = re.sub('<hr(.*?)/>', r'<hr style="margin-top: 10px; margin-bottom: 10px;"/>', res)
    return res.strip()
