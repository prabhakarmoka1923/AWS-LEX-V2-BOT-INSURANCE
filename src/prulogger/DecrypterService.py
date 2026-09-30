"""Decryption logic to decrypt the encrypted msg"""

import json
import jsonpath_ng
from prulogger.Decrypter import Decrypter


def is_json(message):
    '''
        check if the given message is a json object
    '''
    try:
        json.loads(message)
        return True
    except ValueError:
        return False


# pylint: disable=too-few-public-methods
class DecrypterService:
    '''
        Decrypter service to decrypt the encrypted values
        from sensitive fields in the payload
    '''

    def __init__(self, private_key, fields_to_decrypt=
    ("$.inputTranscript",
     "$.sessionState.sessionAttributes",
     "$.sessionState.intent.slots")
                 ):
        self.private_key = private_key
        self.sensitive_fields = fields_to_decrypt

    def decrypt(self, data):
        '''
            decrypt the encrypted data using decrypter
        '''
        if self.sensitive_fields:
            decrypter = Decrypter(self.private_key)
            for i in self.sensitive_fields:
                jsonpath_expr = jsonpath_ng.parse(i)
                match = jsonpath_expr.find(data)
                for count, match_value in enumerate(match):
                    value = match_value.value.split("_", 1)[1]
                    decrypted_value = decrypter.decrypt(value)
                    if is_json(decrypted_value):
                        decrypted_value = json.loads(decrypted_value)
                    match[count].full_path.update(data, decrypted_value)
        return data
