"""Prudential bot custom logger module"""

import logging
import copy
import secrets
import jsonpath_ng
from prulogger.Encrypter import (
    Encrypter, SymmetricEncrypter
)

valid_log_level = ["debug", "info", "warn", "error"]


def format_public_key(key: str):
    """
    method to format the public key passed
    """
    if key.count("\n") > 0:
        return key
    public_key_version = key[0:key.find("-----")]
    prefix = public_key_version + "-----BEGIN PUBLIC KEY-----"
    suffix = "-----END PUBLIC KEY-----"
    raw_data = key.replace(prefix, "").replace(suffix, "").replace(" ", "")
    chunksize = 65
    segments = [raw_data[i:i + chunksize] for i in range(0, len(raw_data), chunksize)]
    return prefix + "\n" + "\n".join(segments) + "\n" + suffix


def create_enc_data(key, value, encrypter, words_not_to_encrypt):
    """
    function to return the dict with encrypted
    value here will be either string, list or None
    """
    temp_dct = {}

    # Scenario : value is non empty string & not in skip_words
    if isinstance(value, str) and value not in words_not_to_encrypt and value:
        temp_dct[key] = encrypter.encrypt(value)

    # Scenario : value list non empty list
    elif isinstance(value, list) and value:
        temp_dct[key] = encrypter.encrypt(str(value))

    # Scenario : Value is None
    else:
        temp_dct[key] = value
    return temp_dct


def encrypt_val(inp, encrypter, sessn_enc_key, symmetric_encryption_flag):
    """function to encrypt not None value"""
    # e.g. slot values comes like this
    # {'shape': 'Scalar', 'value': {'originalValue': '12/12/1992',
    # 'resolvedValues': ['1992-12-12'], 'interpretedValue': '1992-12-12'}}
    # so encryption of 'Scalar' is not needed
    words_not_to_encrypt = ['Scalar', 'PlainText', 'CustomPayload']
    final_enc_val = ''
    if not inp:
        return inp
    if isinstance(inp, str):
        final_enc_val = encrypter.encrypt(inp)
    elif isinstance(inp, list):
        for pos, item in enumerate(inp):
            inp[pos] = encrypt_val(item, encrypter, sessn_enc_key, symmetric_encryption_flag)
        final_enc_val = inp
    elif isinstance(inp, dict):
        for item_key, value in inp.items():
            if isinstance(value, dict):
                encrypt_val(value, encrypter, sessn_enc_key, symmetric_encryption_flag)
            else:
                if symmetric_encryption_flag:
                    # encrypter needs to be initialized again
                    # else it throws exception AlreadyFinalized("Context was already finalized.")
                    encrypter = SymmetricEncrypter(sessn_enc_key)
                temp_dct = create_enc_data(item_key, value, encrypter, words_not_to_encrypt)
                inp.update(temp_dct)
        final_enc_val = inp
    return final_enc_val


def create_session_enc_key(symmetric_encryption_flag):
    """Function to create the session encryption key"""
    session_enc_key = None
    if symmetric_encryption_flag:
        session_enc_key = secrets.token_bytes(32)
    return session_enc_key


def encrypt_session_key(asymmetric_encrypter, key):
    """Function to encrypt the session key, this will use assyemtric encryption"""
    encrypted_session_key = asymmetric_encrypter.encrypt(key)
    return encrypted_session_key


class LoggerService:
    """This is the main logger class with obfuscation option"""

    # pylint: disable=too-many-arguments too-many-instance-attributes
    def __init__(self, public_key, session_id,
                 symmetric_encryption_flag,
                 verbose_level="info", fields_to_encrypt=
                 ("$.inputTranscript",
                  "$.sessionState.sessionAttributes",
                  "$.sessionState.intent.slots",
                  "$.interpretations..slots")):
        # self.encrypter = Encrypter(public_key)
        self.sensitive_fields = fields_to_encrypt
        self.logger = logging.getLogger()
        logging.basicConfig(format="")
        self.verbose_level = verbose_level
        self.determined_level = self.get_minimum_log_level()
        self.logger.setLevel(self.determined_level)
        self.public_key = format_public_key(public_key)
        self.default_meta = {
            "sessionId": session_id
        }
        self.symmetric_encryption_flag = symmetric_encryption_flag
        self.sessn_enc_key = create_session_enc_key(self.symmetric_encryption_flag)

    def get_minimum_log_level(self):
        """get minimum log level from levels passed"""
        determined_log_level = "info"
        standardized_log_level = self.verbose_level.replace(" ", "").lower().split(",")
        for i in valid_log_level:
            if i in standardized_log_level:
                determined_log_level = i
                break
        return determined_log_level.upper()

    # pylint: disable=too-many-locals
    def log(self, level, data):
        """logs the data into cloudwatch based on the level passed"""
        level_mapper = {
            "CRITICAL": 50,
            "ERROR": 40,
            "WARNING": 30,
            "INFO": 20,
            "DEBUG": 10
        }
        level_integer_value = level_mapper[level.upper()]
        if self.sensitive_fields and isinstance(data, dict):
            input_data = copy.deepcopy(data)

            public_key_version = self.public_key[0:self.public_key.find("-----")]
            public_key_data = self.public_key[self.public_key.find("-----"):]
            # initializing the assymetric encrypter for encrypting session encryption key
            asymmetric_encrypter = Encrypter(public_key_version, public_key_data)

            # configuration branching for asymmetric and hybrid Encryption approach
            if self.symmetric_encryption_flag:
                # encrypting the above used session encryption key <sessn_enc_key>
                encrypted_session_key = encrypt_session_key(asymmetric_encrypter,
                                                            self.sessn_enc_key)
                encrypted_key_val = {"SessionEncKey": encrypted_session_key}
                # adding the encrypted key in the prepared input_data
                input_data.update(encrypted_key_val)
            for i in self.sensitive_fields:
                # get the values from payload matching the sensitive field rules
                match = jsonpath_ng.parse(i).find(input_data)
                # if there's more than one match iterate and update
                for match_value in match:
                    value = match_value.value
                    if self.symmetric_encryption_flag:
                        # encrypter needs to be initialized every time encryption is done
                        # else it throws exception AlreadyFinalized(
                        # "Context was already finalized.")
                        encrypter = SymmetricEncrypter(self.sessn_enc_key)
                    else:
                        encrypter = asymmetric_encrypter
                    encrypted_value = encrypt_val(value, encrypter, self.sessn_enc_key,
                                                  self.symmetric_encryption_flag)
                    # update the value matching with sensitive fields
                    # replacing raw value with encrypted value
                    match_value.full_path.update(input_data, encrypted_value)
            input_data.update(self.default_meta)
            self.logger.log(level_integer_value, input_data)
            return None
        data_to_log = copy.deepcopy(self.default_meta)
        data_to_log.update({"message": data})
        self.logger.log(level_integer_value, data_to_log)
        return None
