import requests


class ReCaptcha:
    def __init__(self):
        self.site_key = "6LeW2wsUAAAAAIHedLq8cxaCGjuNiaPxAqU36NIS"
        self._secret_key = "6LeW2wsUAAAAAGrU5Vth1u-UCgYBxIMFi5ettBYV"
        self._endpoint = "https://www.google.com/recaptcha/api/siteverify"

    def verify(self, response):
        response = requests.post(self._endpoint, data={'secret' : self._secret_key, 'response' : response})
        result = response.json()

        return result["success"]
