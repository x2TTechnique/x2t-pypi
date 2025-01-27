import hashlib
import hmac
import json
from requests import post, put, patch, delete, get, Response
from typing import Callable, Dict
from datetime import datetime
from urllib.parse import urlencode


def request_common(
    base_url: str,
    endpoint: str,
    method: Callable,
    params: Dict[str, str] = None,
    headers: Dict[str, str] = None,
    body: Dict = None,
) -> Response:
    if method not in {get, post, put, patch, delete}:
        raise ValueError(
            "Invalid method. Method must be one of: post, put, patch, delete.")
    params = params or {}
    if "timestamp" not in params:
        params["timestamp"] = str(int(datetime.timestamp(datetime.now())))
    query_string = urlencode(params)
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}?{query_string}"
    return method(url=url, headers=headers, json=body)


def sign(endpoint: str, params: dict, app_secret: str, body=None) -> str:
    """Generates a signature for TikTok Open API requests."""
    keys = sorted(key for key in params if key not in ["sign", "access_token"])
    input_data = "".join(key + params[key] for key in keys)
    if isinstance(body, dict):
        body_encoded = json.dumps(body, separators=(',', ':'))
        input_data += body_encoded

    input_data = app_secret + endpoint + input_data + app_secret
    return hmac.new(app_secret.encode(), input_data.encode(), hashlib.sha256).hexdigest()


def get_common_parameters(object, content_type="application/json") -> tuple[Dict[str, str], Dict[str, str]]:
    """Generates common headers and query parameters."""
    timestamp = str(int(datetime.timestamp(datetime.now())))
    headers = {
        "x-tts-access-token": object.access_token,
        "Content-Type": content_type
    }
    queries = {
        "app_key": object.service_id.app_key,
        "timestamp": timestamp
    }
    return headers, queries
