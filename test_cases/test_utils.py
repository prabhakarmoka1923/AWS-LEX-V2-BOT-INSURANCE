"""Module having utils function for TestAnnClientBot"""

import copy
import jsonpath_ng
from src.prulogger.Encrypter import SymmetricEncrypter


def get_private_key():
    """Getting private key
    Note: Below key is the developer's created privated key for testing
    """
    private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDzeV5HB5diKyXL
mPHX03NpYN0WkNcnNDqddtvOUZOhPWTMEY1MtYD2DKgC45ZFxkCXv5YUdE2isthQ
Zsdhv+ICdiTlegdau1LQ1GaoSn0sYRe/SoQHPbkuXe6qlEcFDI7R+i7XhbpkAjCF
g7bipN3t9MQ0dmHt0SHlmaK3wlfmG13NHQ37wWU7rAnBGc6tEEBE27OQFsiI1xYx
4Emi8T7+l/+zO1NfT/VUHSug8JZJ8SzBgeEN1aBXF24PE9ALHC7b1XuR5iBM0Q+f
Nm1X/n1X6CzLx1dv49IWPvfgL0uJF3WRQ85E9asdIkc2/5+RUQbQmqPPhfEtLjhX
x3bC8n8JAgMBAAECggEABLDyONaj21OfAQ8Dm+e6Wc2wvNpSFvKJ7ZZIcm9+c3Ui
H893xEJcB4GjbBjUAKiq/nGF1AOQqmGdSuFMFq1Sjr8Vg2loQl6JIDZzeusigcwm
H7yxEg2lp4fOTTGZs7Zz+wZByEvOlVY4dp4c1D2efBMDA8rDJMiqiUi+SqGfPXMA
aolUbOC3k3PYqBDCiLMfqbrJMy3mhg/5BwMEP0Cl/GreOKBXnfl25qOlNuwx4cMT
rPYfZVM/zcytQoVjh79RQZGqM6PfVKUojpjiHL0pTDmZqhOE68lqoqz17se1YTmz
rLc2O4hXvJ5IcgMt86VlYwpI0yXCBmyC2IRx3ae9AQKBgQD05BfJThz6v901UOjZ
uZ9eu/6hpvet9bdGhccIKDJBDuWOJMgKzSWHoY+pcZPwTBdFLJS8t5Ju3U/wx7ZI
thW8AJ5Ze1gvVE/8cAODQ3PMCIrSgODwP/cPEaqorwiCL+Bh+TZtX2VWdQqaV3ra
Tqc/B3yWbzJg569oKQJjE3+3iQKBgQD+hNIwAhocf6zzk1Te9nMwh01/zGofzXYO
N9+gm48mREQUGRsynJcETnHDjWW1qVH8QK5s3/1TbGcg/tvFCVXrQGUMO4m9kxb0
UTgkmCkryISNmUT6aPnniqrKZ4F6Cv6iyk1Z2lj7G4tfKrT6NXc+JLezLJzq6BRG
A9VEuesrgQKBgAX2uA2S9Wm12nE98y26M4NfGKhfJJD79uakw2ATeoXTEwwPIUAC
FvPin1kFBxFHCRoKJ+Ugo1RH13aJporGxGi7qx+KvW8JopkHMU61CdDiNF9D/DZd
mGqph3psKMzi1ZgNNaIcPJ+KYiO4FanTWIdUa1hOhO+PNNpYhVJcWzPhAoGAfhmk
YbDI6xG+yLdYN1d3XrXKieTnN3Z+ZTD9lP89f0IXULXXqc23bKTI7JAjskt/mTEa
ukqHokt1FP3wOMEVVocDCXp+FfTITKfo3wicbVrdgaJMcJyOJE+pqrp5hdPosRL2
G+x4ZYESHkZ0f/r5Z0qd0SHrZN8zHDVN9sz+XQECgYEAotIeGQSU4SG2YA15n/PD
JGTnU2fUmxO4+IbpaKOtWppgd4F6yOj94ftjt70jVXVbzCyYxIQ5nL7SJKbLbfCn
GSGEP06nNlTubtE7cKLFMmRJf4vZFCSskqTyqgpITQtT05VLF8FO7NY23gyVhS9G
nuGeFcfld28G1bHkDrrq96I=
-----END RSA PRIVATE KEY-----"""
    return private_key

def decrypt_json(data, decryption_key, sym_prefix=''):
    """Function to decrypt the payload"""
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
    input_data = copy.deepcopy(data)
    if sensitive_fields and isinstance(data, dict):


        for i in sensitive_fields:
            # get the values from payload matching the sensitive field rules
            match = jsonpath_ng.parse(i).find(input_data)
            # if there's more than one match iterate and update
            for match_value in match:
                value = match_value.value
                decrypter = SymmetricEncrypter(decryption_key)
                decrypted_value = decrypt_payload(value, decrypter, decryption_key, sym_prefix)
                # update the value matching with sensitive fields
                # replacing raw value with encrypted value
                match_value.full_path.update(input_data, decrypted_value)
    return input_data

def create_decrypt_data(key, value, decrypter, sym_prefix):
    """
    Wrapper function to do selective decryption
    """
    temp_dct = {}
    temp_val = value
    if isinstance(temp_val, str) and temp_val.startswith(sym_prefix):
        temp_val = decrypter.decrypt(value[len(sym_prefix):])
    temp_dct[key] = temp_val
    return temp_dct

def decrypt_payload(data, decrypter, sessn_dec_key, sym_prefix):
    """Wrapper function to decrypt basis on type of payload"""
    final_dec_val = data
    if not data:
        return data
    if isinstance(data, list):
        for item in data:
            decrypt_payload(item, decrypter, sessn_dec_key, sym_prefix)
    elif isinstance(data, dict):
        for item_key, value in data.items():
            if isinstance(value, dict):
                decrypt_payload(value, decrypter, sessn_dec_key, sym_prefix)
            elif isinstance(value, list):
                for item in value:
                    decrypt_payload(item, decrypter, sessn_dec_key, sym_prefix)
            else:
                decrypter = SymmetricEncrypter(sessn_dec_key)
                temp_dct = create_decrypt_data(item_key, value, decrypter, sym_prefix)
                data.update(temp_dct)
        final_dec_val = data
    elif isinstance(data, str) and data.startswith(sym_prefix):
        final_dec_val = decrypter.decrypt(data[len(sym_prefix):])
    return final_dec_val
