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

    def get_address(self, address, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Addresses/paths/~1addresses~1{address}/get

        :param address: required
        :type address: str
        :return: Blockfrost API response
        """
        path = 'addresses/' + address
        return self._get(path, params=kwargs)

    def get_address_details(self, address, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Addresses/paths/~1addresses~1{address}~1total/get

        :param address: required
        :type address: str
        :return: Blockfrost API response
        """
        path = 'addresses/' + address + '/total'
        return self._get(path, params=kwargs)

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

    def get_latest_block(self, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks

        :return: Blockfrost API response
        """
        path = 'blocks/latest'
        return self._get(path, params=kwargs)

    def get_latest_block_txs(self, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks

        :return: Blockfrost API response
        """
        path = 'blocks/latest/txs'
        return self._get(path, params=kwargs)

    def get_specific_block(self, hash_or_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks/paths/~1blocks~1{hash_or_number}/get

        :param hash_or_number: Block hash or number
        :type hash_or_number: str
        :return: Blockfrost API response
        """
        path = 'blocks/' + str(hash_or_number)
        return self._get(path, params=kwargs)

    def get_specific_block_in_slot(self, slot_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks/paths/~1blocks~1slot~1{slot_number}/get

        :param slot_number: slot number
        :type slot_number: int
        :return: Blockfrost API response
        """
        path = '/blocks/slot/' + str(slot_number)
        return self._get(path, params=kwargs)

    def get_specific_block_in_epoch_slot(self, epoch_number, slot_number_epoch, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks/paths/~1blocks~1epoch~1{epoch_number}~1slot~1{slot_number}/get

        :param epoch_number: epoch number
        :type epoch_number: int
        :param slot_number_epoch: slot number
        :type slot_number_epoch: int
        :return: Blockfrost API response
        """
        path = '/blocks/epoch/' + str(epoch_number) + '/slot/' + str(slot_number_epoch)
        return self._get(path, params=kwargs)

    def get_next_blocks(self, hash_or_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks/paths/~1blocks~1{hash_or_number}~1next/get

        :param hash_or_number:
        :type hash_or_number: str
        :return: Blockfrost API response
        """
        path = '/blocks/' + hash_or_number + '/next'
        return self._get(path, params=kwargs)

    def get_previous_blocks(self, hash_or_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks/paths/~1blocks~1{hash_or_number}~1previous/get

        :param hash_or_number: Block hash or number
        :type hash_or_number: str
        :return: Blockfrost API response
        """
        path = '/blocks/' + hash_or_number + '/previous'
        return self._get(path, params=kwargs)

    def get_block_txs(self, hash_or_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Blocks/paths/~1blocks~1{hash_or_number}~1txs/get

        :param hash_or_number: Block hash or number
        :type hash_or_number: str
        :return: Blockfrost API response
        """
        path = '/blocks/' + hash_or_number + '/txs'
        return self._get(path, params=kwargs)

    def get_latest_epoch(self, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs

        :return: Blockfrost API response
        """
        path = '/epochs/latest'
        return self._get(path, params=kwargs)

    def get_latest_epoch_protocol_params(self, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1latest~1parameters/get

        :return: Blockfrost API response
        """
        path = '/epochs/latest/parameters'
        return self._get(path, params=kwargs)

    def get_specific_epoch(self, epoch_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1{number}/get

        :param epoch_number: epoch number
        :type epoch_number: int
        :return: Blockfrost API response
        """
        path = '/epochs/' + str(epoch_number)
        return self._get(path, params=kwargs)

    def get_next_epochs(self, epoch_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1{number}~1next/get

        :param epoch_number: starting epoch number
        :type epoch_number: int
        :return: Blockfrost API response
        """
        path = '/epochs/' + str(epoch_number) + '/next'
        return self._get(path, params=kwargs)

    def get_previous_epochs(self, epoch_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1{number}~1previous/get

        :param epoch_number: starting epoch number
        :type epoch_number: int
        :return: Blockfrost API response
        """
        path = '/epochs/' + str(epoch_number) + '/previous'
        return self._get(path, params=kwargs)

    def get_active_stake_distribution(self, epoch_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1{number}~1stakes/get

        :param epoch_number: Epoch number for stake distribution

        :return: Blockfrost API response
        """
        path = '/epochs/' + str(epoch_number) + '/stakes'
        return self._get(path, params=kwargs)

    def get_stake_distribution_by_pool(self, epoch_number, pool_id, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1{number}~1stakes~1{pool_id}/get

        :param epoch_number: Epoch number for stake distribution
        :type epoch_number: int
        :param pool_id: pool id BECH32
        :type pool_id; str
        :return: Blockfrost API response
        """
        path = '/epochs/' + str(epoch_number) + '/stakes/' + pool_id
        return self._get(path, params=kwargs)

    def get_block_distribution(self, epoch_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1{number}~1blocks/get

        :param epoch_number: Epoch number for block distribution
        :type epoch_number: int
        :return: Blockfrost API response
        """
        path = '/epochs/' + str(epoch_number) + '/blocks'
        return self._get(path, params=kwargs)

    def get_block_distribution_by_pool(self, epoch_number, pool_id, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1{number}~1blocks~1{pool_id}/get

        :param epoch_number: Epoch number for block distribution
        :type epoch_number: int
        :param pool_id: pool id BECH32
        :type pool_id; str
        :return: Blockfrost API response
        """
        path = '/epochs/' + str(epoch_number) + '/blocks/' + pool_id
        return self._get(path, params=kwargs)

    def get_protocol_params_for_epoch(self, epoch_number, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Epochs/paths/~1epochs~1{number}~1blocks/get

        :param epoch_number: Epoch number for block distribution
        :type epoch_number: int
        :return: Blockfrost API response
        """
        path = '/epochs/' + str(epoch_number) + '/parameters'
        return self._get(path, params=kwargs)

    def get_blockchain_genesis(self, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Ledger/paths/~1genesis/get

        :return: Blockfrost API response
        """
        path = '/genesis'
        return self._get(path, params=kwargs)

    def get_transaction_metadata_labels(self, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Metadata

        :return: Blockfrost API response
        """
        path = '/metadata/txs/labels'
        return self._get(path, params=kwargs)

    def get_transaction_metadata_json(self, label, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Metadata/paths/~1metadata~1txs~1labels~1{label}/get

        :param label: Metadata label
        :type label: str
        :return: Blockfrost API response
        """
        path = '/metadata/txs/labels/' + label
        return self._get(path, params=kwargs)

    def get_transaction_metadata_cbor(self, label, **kwargs):
        """
        see:
        https://docs.blockfrost.io/#tag/Cardano-Metadata/paths/~1metadata~1txs~1labels~1{label}/get

        :param label: Metadata label
        :type label: str
        :return: Blockfrost API response
        """
        path = '/metadata/txs/labels/' + label + '/cbor'
        return self._get(path, params=kwargs)
