import datetime
import hmac
import base64
import json
import urllib.parse

# Signature
"""
The OK-ACCESS-SIGN header is generated as follows:

• Create a prehash string of timestamp + method + requestPath + body (where + represents String concatenation).
• Prepare the SecretKey.
• Sign the prehash string with the SecretKey using the HMAC SHA256.
• Encode the signature in the Base64 format.

Example: sign=CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(timestamp + 'GET' + '/api/v5/account/balance?ccy=BTC', SecretKey))

The timestamp value is the same as the OK-ACCESS-TIMESTAMP header with millisecond ISO format, e.g. 2020-12-08T09:08:57.715Z.

The request method should be in UPPERCASE: e.g. GET and POST.

The requestPath is the path of requesting an endpoint.

Example: /api/v5/account/balance

The body refers to the String of the request body. It can be omitted if there is no request body (frequently the case for GET requests).

Example: {"instId":"BTC-USDT","lever":"5","mgnMode":"isolated"}

The SecretKey is generated when you create an APIKey.

Example: 22582BD0CFF14C41EDBF1AB98506286D
"""
def get_timestamp(sep='T', timespec='milliseconds'):
    return datetime.datetime.utcnow().isoformat(sep=sep, timespec=timespec) + "Z"


def sign(timestamp, method, request_path:str, body, secret_key:str):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    else:
        body = json.dumps(body)
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)
    

def require_kwargs(required_keys:list, **kwargs):
    for key in required_keys:
        if key not in kwargs:
            raise ValueError(f"Required key '{key}' not found in kwargs")


def validate_kwargs(kwargs: dict, required_keys: list, optional_keys: list = []) -> dict:
    # Validate required keys
    for key in required_keys:
        if key not in kwargs:
            raise ValueError(f"Required key '{key}' not found in kwargs")

    # Remove keys that are not in either required or optional keys
    valid_keys = required_keys + optional_keys
    for key in list(kwargs.keys()):
        if key not in valid_keys or kwargs[key] is None:
            kwargs.pop(key)

    return kwargs


def urlencode(**kwargs):
    return ("?" + urllib.parse.urlencode(query=kwargs, doseq=False)) if list(kwargs.items()) else ""


def get_public_ip_address():
    import requests
    # Send a request to an external service to get the public IP address
    response = requests.get('https://api.ipify.org')

    # Extract the IP address from the response
    ip_address = response.text

    return ip_address


