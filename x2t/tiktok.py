from typing import Any, Dict, Tuple
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
    """
    Sends an HTTP request with common parameters handling.

    This function constructs a URL with query parameters, ensures a 
    timestamp is included, and sends a request using the specified HTTP method.

    Args:
        base_url (str): The base URL of the API.
        endpoint (str): The API endpoint to request.
        method (Callable): The HTTP method function (e.g., requests.get, requests.post).
        params (Dict[str, str], optional): Query parameters to include in the request. Defaults to None.
        headers (Dict[str, str], optional): Headers to include in the request. Defaults to None.
        body (Dict, optional): JSON body for POST, PUT, or PATCH requests. Defaults to None.

    Returns:
        Response: The response object from the HTTP request.

    Raises:
        ValueError: If an invalid HTTP method is provided.

    Example:
        >>> response = request_common(
        ...     base_url="https://api.example.com",
        ...     endpoint="/data",
        ...     method=post,
        ...     params={"key": "value"},
        ...     headers={"Authorization": "Bearer token"},
        ...     body={"data": "test"}
        ... )
        >>> print(response.status_code)
        200
    """
    if method not in {get, post, put, patch, delete}:
        raise ValueError(
            "Invalid method. Method must be one of: post, put, patch, delete.")
    params: dict[str, Any] = params or {}
    if "timestamp" not in params:
        params["timestamp"] = str(int(datetime.timestamp(datetime.now())))
    query_string: str = urlencode(params)
    url: str = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}?{query_string}"
    return method(url=url, headers=headers, json=body)


def sign(endpoint: str, params: dict, app_secret: str, body=None) -> str:
    """
    Generates a signature for TikTok Open API requests.

    This function creates an HMAC-SHA256 signature by concatenating the 
    app secret, API endpoint, sorted query parameters, and request body 
    (if provided). It ensures that the request is securely signed before 
    being sent to TikTok's API.

    Args:
        endpoint (str): The API endpoint being requested.
        params (dict): The query parameters for the request, excluding "sign" and "access_token".
        app_secret (str): The application's secret key used for signing the request.
        body (dict, optional): The request body, which will be JSON-encoded if provided. Defaults to None.

    Returns:
        str: The generated HMAC-SHA256 signature as a hexadecimal string.

    Example:
        >>> sign(
        ...     endpoint="/open_api/v1/resource",
        ...     params={"param1": "value1", "param2": "value2"},
        ...     app_secret="mysecret",
        ...     body={"key": "value"}
        ... )
        'a3b1c2d4e5f67890abcd1234567890abcdef1234567890abcdef1234567890'

    Notes:
        - The `params` dictionary is sorted before signing.
        - The request body is JSON-encoded before being included in the signature.
    """
    keys: list[str] = sorted(key for key in params if key not in ["sign", "access_token"])
    input_data: str = "".join(key + str(params[key]) for key in keys)

    if isinstance(body, dict):
        body_encoded: str = json.dumps(body)
        input_data += body_encoded

    input_data: str = app_secret + endpoint + input_data + app_secret
    return hmac.new(app_secret.encode(), input_data.encode(), hashlib.sha256).hexdigest()


def get_common_parameters(object, content_type: str = "application/json") -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Generates common headers and query parameters for an API request.

    Args:
        object: An object containing authentication and service details.
        content_type (str, optional): The content type for the request headers.
                                      Defaults to "application/json".

    Returns:
        Tuple[Dict[str, str], Dict[str, str]]: 
            - A dictionary of headers including the access token and content type.
            - A dictionary of query parameters including the app key and timestamp.

    Example:
        >>> obj = SomeAuthObject(access_token="abc123", service_id=Service(app_key="xyz789"))
        >>> headers, queries = get_common_parameters(obj)
        >>> print(headers)
        {'x-tts-access-token': 'abc123', 'Content-Type': 'application/json'}
        >>> print(queries)
        {'app_key': 'xyz789', 'timestamp': '1700000000'}
    """
    timestamp = str(int(datetime.timestamp(datetime.now())))
    headers: dict[str:Any] = {
        "x-tts-access-token": object.access_token,
        "Content-Type": content_type
    }
    queries: dict[str:Any] = {
        "app_key": object.service_id.app_key,
        "timestamp": timestamp
    }
    return headers, queries
