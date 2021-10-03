import simplejson as json

DEFAULT_HEADERS: dict = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
    "Content-Type": "application/json",
}


class HttpResponse(dict):
    def __init__(
        self,
        status_code,
        body: dict or str,
        headers=DEFAULT_HEADERS,
    ) -> dict:
        super().__init__()

        if isinstance(body, dict):
            response: str = json.dumps(body)
        elif isinstance(body, str):
            response: str = body
        else:
            raise Exception

        self.update(
            {
                "statusCode": str(int(status_code)),
                "headers": headers,
                "body": response,
            }
        )
