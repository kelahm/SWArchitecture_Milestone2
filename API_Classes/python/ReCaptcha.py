import requests


class ReCaptcha:
    def __init__(self):
        self.site_key = "6LeW2wsUAAAAAIHedLq8cxaCGjuNiaPxAqU36NIS"
        self._secret_key = "6LeW2wsUAAAAAGrU5Vth1u-UCgYBxIMFi5ettBYV"
        self._endpoint = "https://www.google.com/recaptcha/api/siteverify/"

    def verify(self, response):
        secret = "secret=" + self._secret_key
        response = "response=" + response

        query = self._endpoint + "?" + secret + "&" + response

        response = requests.get(query)
        result = response.json()

        return result["success"]
