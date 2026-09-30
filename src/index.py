"""Process intents/slots from Lex using Kendra or other entities and send response
back to Lex
"""

from prulogger import LoggerService
from intents import load_secret, intent_utils
from utils import Handler


VERBOSE_LEVEL = "info"
LOG_EVENT = True
LOG_ENCRYPTION = True
SYMMETRIC_ENCRYPTION = True

def get_logger_encrypted(event, symmetric_encryption_flag):
    """Gets an encrypted logger instance that uses asymmetric/symmetric encryption"""
    # pylint: disable=too-many-function-args
    get_key = load_secret.get_secret()

    # Log encryption
    public_key = get_key.get('cdo_logger_public_key')
    sensitive_fields = [
        "$.inputTranscript",

        "$.sessionState..slots.dob",  # Search for dob slot under sessionState
        "$.sessionState..slots.contractId",  # Search for contractid slot under sessionState
        "$.sessionState..slots.ssn",  # Search for ssn slot under sessionState

        "$.interpretations..slots",  # Search for slots under interpretations

        #  Search for contractid slot under proposedNextState
        "$.proposedNextState..slots.contractId",
        "$.proposedNextState..slots.dob",  # Search for dob slot under proposedNextState
        "$.proposedNextState..slots.ssn",  # Search for ssn slot under proposedNextState

        "$.transcriptions..transcription",
        # Search for contractid resolvedSlot under transcriptions
        "$.transcriptions..resolvedSlots.contractId",
        # Search for dob resolvedSlot under transcriptions
        "$.transcriptions..resolvedSlots.dob",
        # Search for ssn resolvedSlot under transcriptions
        "$.transcriptions..resolvedSlots.ssn",

        # Search for api request data under requestAttributes and contextAttributes
        "$.requestAttributes",
        "$..contextAttributes",
        "$.sessionState..sessionAttributes.Utterance_History"
    ]
    session_id = event['sessionId']
    logger_enc = LoggerService(public_key, session_id,
                               symmetric_encryption_flag,
                               VERBOSE_LEVEL, sensitive_fields)
    return logger_enc


def lambda_handler(event, context=None, callback=None):
    """Lambda handler"""
    # pylint: disable=unused-argument
    # pylint: disable=broad-except
    this_handler = Handler(event, LOG_ENCRYPTION)
    logger = intent_utils.logger
    logger_encrypted = get_logger_encrypted(event, SYMMETRIC_ENCRYPTION)
    try:
        log_req_res(event, logger, logger_encrypted, LOG_EVENT, LOG_ENCRYPTION)
        response = this_handler.process()
        log_req_res(response, logger, logger_encrypted, LOG_EVENT, LOG_ENCRYPTION)
    except Exception as exc:
        sessn_id = this_handler.event["sessionId"]
        intent_utils.log_error(sessn_id, "Exception in generating response", exc)
        msg = this_handler.config["messages"]["technical_issue"]
        intent_utils.add_message(this_handler, msg)
        intent_utils.add_message(this_handler, intent_utils.payload_suggestions(
                this_handler.config['main_menu'],
                this_handler.config), "CustomPayload")
        response = this_handler.generate_response()
    return response

def log_req_res(event, logger, logger_encrypted, log_event, log_encryption):
    """Log event based on logger configuration"""
    if log_event:
        if log_encryption:
            logger_encrypted.log("info", event)
        else:
            logger.info(event)
