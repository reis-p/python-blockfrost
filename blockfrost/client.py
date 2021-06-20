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

    def _request(self, method, uri, **kwargs):
        self.response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(self.response)

    @staticmethod
    def _handle_response(response):

        if not response.status_code == 200:
            raise BlockfrostAPIException(response, response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            raise ValueError

    def _get(self, path, **kwargs):
        return self._request_api('get', path, **kwargs)

    def _request_api(self, method, path, **kwargs):
        uri = self._create_uri(path)
        return self._request(method, uri, **kwargs)

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

    # User Side

    def get_address(self, address):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Addresses/paths/~1addresses~1{address}/get

        :param address: required
        :type address: str
        :return: Blockfrost API response
        """
        path = 'addresses/' + address
        return self._get(path)

    def get_address_details(self, address):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Addresses/paths/~1addresses~1{address}~1total/get

        :param address: required
        :type address: str
        :return: Blockfrost API response
        """
        path = 'addresses/' + address + '/total'
        return self._get(path)

    def get_address_utxos(self, address, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Addresses/paths/~1addresses~1{address}~1utxos/get

        :param address: required
        :type address: str
        :return: Blockfrost API response
        """
        path = 'addresses/' + address + '/utxos'
        return self._get(path, params=kwargs)

    def get_address_transactions(self, address, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Addresses/paths/~1addresses~1{address}~1transactions/get

        :param address: required
        :type address: str
        :return: Blockfrost API response
        """
        path = 'addresses/' + address + '/transactions'
        return self._get(path, params=kwargs)

    def get_latest_block(self):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks

        :return: Blockfrost API response
        """
        path = 'blocks/latest'
        return self._get(path)

    def get_latest_block_txs(self, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks

        :return: Blockfrost API response
        """
        path = 'blocks/latest/txs'
        return self._get(path, params=kwargs)

    def get_specific_block(self, hash_or_number):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks/paths/~1blocks~1{hash_or_number}/get

        :param hash_or_number: Block hash or number
        :type hash_or_number: str
        :return: Blockfrost API response
        """
        path = 'blocks/' + hash_or_number
        return self._get(path)
