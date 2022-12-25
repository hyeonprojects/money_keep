import json
import os

from fastapi import HTTPException

SECRET_JSON_FILE = os.path.join("./",  "setting.json")

with open(SECRET_JSON_FILE, 'r') as secret_json:
    secret = json.load(secret_json)


def get_secret(setting, secret=secret):
    try:
        return secret[setting]
    except KeyError:
        error_msg = "Set the {} envirnment variable".format(setting)
        return HTTPException(status_code=404, message=error_msg)
