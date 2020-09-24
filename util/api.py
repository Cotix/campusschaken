from config import *
import json


def ok(data, status=200):
    if(isinstance(data, dict)):
        text = json.dumps(data)
    else:
        text = data.to_json()
    res = Response(text, status=status, mimetype="application/json")
    return res


def success():
    res = Response("{\"success\":true}", status=200, mimetype="application/json")
    return res


def error(reason, errno):
    res = Response("{\"error\":\"" + reason + "\"}", status=errno, mimetype="application/json")
    return res
