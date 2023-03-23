import json
from datetime import datetime, timedelta, timezone

from jwt import (JWT, jwk_from_dict, jwk_from_pem,)
from jwt.utils import get_int_from_datetime


instance = JWT()

message = {
    'iss': 'https://example.com/',
    'sub': 'yosida95',
    'iat': get_int_from_datetime(datetime.now(timezone.utc)),
    'exp': get_int_from_datetime(
        datetime.now(timezone.utc) + timedelta(hours=1)),
}

"""Encode the message to JWT(JWS.)
    """
#load a RSA key from a JWK dict.
signing_key = jwk_from_dict({
    'kty': 'RSA',
    'n':'0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4QyQ5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6WeZu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEgU8awapJzKnqDKgw',
    "d":"X4cTteJY_gn4FYPsXB8rdXix5vwsg1FLN5E3EaG6RJoVH-HLLKD9M7dx5oo7GURknchnrRweUkC7hT5fJLM0WbFAKNLWY2vv7B6NqXSzUvxT0_YSfqijwp3RTzlBaCxWp4doFk5N2o8Gy_nHNKroADIkJ46pRUohsXywbReAdYaMwFs9tv8d_cPVY3i07a3t8MN6TNwm0dSawm9v47UiCl3Sk5ZiG7xojPLu4sbg1U2jx4IBTNBznbJSzFHK66jT8bgkuqsk0GjskDJk19Z4qwjwbsnn4j2WBii3RL-Us2lGVkY8fkFzme1z0HbIkfz0Y6mqnOYtqc0X4jfcKoAC8Q",
    'e': 'AQAB'})

compact_jws = instance.encode(message, signing_key, alg='RS256')


"""Decode the JWT with verifying the signature.
    """
#load a public key from PEM file corresponding to the signing private key.
with open(r'sample_project\user\v1\rsa_public_key.json','r') as fh:
    verifying_key = jwk_from_dict(json.load(fh))
    
message_recieved = instance.decode(compact_jws, verifying_key, do_time_check=True)
print(message_recieved)
"""
Successfuly retrieved the `message` from the `compact_jws`
"""
assert message == message_recieved
