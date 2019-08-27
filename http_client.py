import configparser
import hashlib
import hmac
import json

import aiohttp
import asyncio
import requests
from aiohttp import ClientSession

from enums import *


class HttpClient(object):
    def __init__(self, config_path):
        self.public_config = configparser.ConfigParser()
        self.public_config.read(config_path)
        self.public_url = self.public_config['DEFAULT']['URL']
        self.ws_url = self.public_config['DEFAULT']['WS']

    def send(url, command, http_method, token=""):
        if token == "":
            headers = {"content-type": "application/json"}
        else:
            headers = {"content-type": "application/json", "authorization-vbtc": token}
        if http_method == HttpMethod.GET:
            response = requests.get(url, headers=headers)
        elif http_method == HttpMethod.POST:
            response = requests.post(url, json.dumps(command), headers=headers)
        elif http_method == HttpMethod.PUT:
            response = requests.put(url, json.dumps(command), headers=headers)
        else:
            raise AssertionError("Undefined HTTP method")
        if response.status_code != 200:
            print("Request error: ", response.reason)
            raise AssertionError("Request error: " + response.reason)
        try:
            data = response.json()        
        except:
            data = {}
        try:
            error = 'error' in data
        except:
            error = False
        if error:
            error = data['error']
            print("Response error: ({0}) {1}".format(error['messageCode'], error['message']))
            raise AssertionError("Response error :" + error['message'])
        return response

    def send_public_api(self, url, command, http_method, client=None, apikey=None):
        url = self.public_url + url
        headers = None
        if None not in(client, apikey):
            client_id = self.public_config[client][apikey]
            signature, message = self._sign_message(command, client, apikey)
            headers = {'X-BitQi-ClientId': client_id, 'X-BitQi-Signature': signature}

        if http_method == HttpMethod.POST:
            response = requests.post(url+message, headers=headers)
        elif http_method == HttpMethod.GET:
            response = requests.get(url, params=command)

        if response.status_code != 200:
            print("Request error: ", response.reason)
            print(response.text)
            raise AssertionError(response.content)

        if 'error' in response.json():
            raise AssertionError(response.json())

        return response

    async def send_async_public_api(self, url, params, method, client, apikey, session=None):
        timeout = 1200
        url = self.public_url + url
        headers = None
        if None not in (client, apikey):
            client_id = self.public_config[client][apikey]
            signature, message = self._sign_message(params, client, apikey)
            headers = {'X-BitQi-ClientId': client_id, 'X-BitQi-Signature': signature}
        if method == HttpMethod.POST:
            async with session.post(url+message, headers=headers, timeout=timeout) as response:
                return await response.json()

        elif method == HttpMethod.GET:
            async with session.get(url, headers=headers, timeout=timeout) as response:
                return await response.json()

    async def run_requests(self, params: list):
        """
        :param params: list of lists, each list is one public api request parameters
        :return: list of the json responses
        """
        tasks = []
        async with ClientSession(trust_env=True) as session:
            for param in params:
                task = asyncio.ensure_future(self.send_async_public_api(*param, session=session))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            return await responses

    def _sign_message(self, initial, client, apikey):
        message = '?'
        for key, value in initial.items():
            if value != "":
                message = message + str(key) + '=' + str(value) + '&'
        message = message[:len(message) - 1]
        if 'data' in apikey:
            key_type = 'Secret_data'
        else:
            key_type = 'Secret'
        secret = bytes(self.public_config[client][key_type], 'utf-8')
        content = bytes(message[1:], 'utf-8')
        hash = hmac.new(secret, content, hashlib.sha256)
        signature = hash.hexdigest()
        return signature, message

    async def ws_conn(self, market_id, client_id):
        timeout = 30
        sign = '{client:"' + client_id + '"}'
        market = '{marketId:' + str(market_id) + '}'
        session = aiohttp.ClientSession()
        try:
            ws = await asyncio.wait_for(session.ws_connect(self.ws_url, autoping=True), timeout=timeout)
        except asyncio.TimeoutError:
            raise WSConnectionError
        await ws.send_str(sign)
        await ws.send_str(market)
        session.detach()
        return ws

    async def get_ws_msg(self, ws):
        messages = []
        timeout = 3
        res = None
        while True:
            try:
                res = await asyncio.wait_for(ws.receive(), timeout=timeout)
            except asyncio.TimeoutError:
                break
            print(res.data)
            messages.append(json.loads(res.data))
        return messages

class WSConnectionError(Exception):
    pass
