
import json


class BlockfrostAPIException(Exception):

    def __init__(self, response, status_code, text):
        self.code = 0
        try:
            json_res = json.loads(text)
        except ValueError:
            self.message = 'Invalid JSON error message from blockfrost: {}'.format(response.text)
        else:
            self.code = json_res['status_code']
            self.message = json_res['message']
        self.status_code = status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return 'APIError(code={}): {}'.format(self.code, self.message)