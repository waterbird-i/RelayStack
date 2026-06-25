SECRET_HEADERS = {"authorization", "cookie", "x-api-key"}


def redact_headers(headers):
    return {
        key: ("<redacted>" if key in SECRET_HEADERS else value)
        for key, value in headers.items()
    }


def redact_url(url):
    return url
