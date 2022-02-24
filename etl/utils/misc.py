import httpx
DEFAULT_TIMEOUT = httpx.Timeout(timeout=10)


def httpx_request(url, header):
    url=url
    header = header
    with httpx.Client(headers=header) as client:
        r = client.get(url)
        resp_json = r.json()
        return resp_json