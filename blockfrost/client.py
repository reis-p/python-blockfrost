"""
Blockfrost API DataHandler for the dadascience project
"""

import requests
from .exceptions import BlockfrostAPIException


class Client:
    API_URL_MAINNET = 'https://cardano-mainnet.blockfrost.io/api'
    API_URL_TESTNET = 'https://cardano-testnet.blockfrost.io/api'
    API_VERSION = 'v0'

    URL_ADDRESS = 'addresses/{}'

    def __init__(self, api_key, testnet=False):

        self.api_key = api_key
        self.api_url_mainnet = self.API_URL_MAINNET
        self.api_url_testnet = self.API_URL_TESTNET
        self.response = None
        self.testnet = testnet
        self.api_version = self.API_VERSION

        self.session = self._init_session()

    def _init_session(self):

        header = self._get_headers()
        session = requests.session()
        session.headers.update(header)

        return session

    def _get_headers(self):
        headers = {
            'Accept': 'application/json',
        }
        if self.api_key:
            headers['project_id'] = self.api_key
        else:
            raise ValueError('No API Key defined')

        return headers

    def _request(self, method, uri):
        self.response = getattr(self.session, method)(uri)
        return self._handle_response(self.response)

    @staticmethod
    def _handle_response(response):

        if not response.status_code == 200:
            raise BlockfrostAPIException(response, response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            raise ValueError

    def _get(self, path):
        return self._request_api('get', path)

    def _request_api(self, method, path):
        uri = self._create_uri(path)
        return self._request(method, uri)

    def _create_uri(self, path):
        url = self.api_url_mainnet
        if self.testnet:
            url = self.api_url_testnet
        v = self.api_version
        return url + '/' + v + '/' + path

    @staticmethod
    def _get_payload_from_params(params):
        payload = ''
        for item in params.items():
            if item[0] != 'details':
                payload = item[1]
        if params['details']:
            payload = payload + '/' + params['details']
        return payload

    def get_address(self, address):
        """
        :param address: required
        :type address: str
        :return: Blockfrost API response
        """
        path = 'addresses/' + address
        return self._get(path)

    def get_address_details(self, address):
        """
        :param address: required
        :type address: str
        :return: Blockfrost API response
        """
        path = 'addresses/' + address + '/total'
        return self._get(path)
