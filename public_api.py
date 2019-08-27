import configparser
import multiprocessing

import asyncio
from aiohttp import ContentTypeError


from enums import HttpMethod
from http_client import HttpClient








class PublicApi:
    def __init__(self, config_path):

        self.client = HttpClient(config_path)

    def create_withdrawal(self, client='USER1', apikey='Public', **params):
        response = self.client.send_public_api("/api/po/Account/CreateWithdrawal",
                                               params, HttpMethod.POST, client, apikey)
        return response.json()

    def create_code(self, amount, currency, recipient="", description="", client='USER1',
                    apikey='Public'):
        command = {'Amount': amount, 'Currency': currency, 'Recipient': recipient, 'Description': description}

        response = self.client.send_public_api("/api/po/Account/CreateCode",
                                    command, HttpMethod.POST, client, apikey)
        return response.json()

    def get_user_balances(self, data=0, client='USER1', apikey='Public'):
        command = {'data': data}
        response = self.client.send_public_api("/api/po/Account/GetUserBalances",
                                               command, HttpMethod.POST, client, apikey)
        return response.json()

    def redeem_code(self, id, client='USER1', apikey='Public'):
        command = {'Code': id}
        response = self.client.send_public_api("/api/po/Account/RedeemCode",
                                               command, HttpMethod.POST, client, apikey)
        return response.json()

    def create_order(self, client='USER1', apikey='Public', **params):
        response = self.client.send_public_api("/api/po/Trade/CreateOrder",
                                               params, HttpMethod.POST, client, apikey)
        return response.json()

    def get_order_book(self, **params):
        response = self.client.send_public_api("/api/po/MarketData/GetOrderBook", params, HttpMethod.GET)
        return response.json()

    def get_ticker(self, **params):
        response = self.client.send_public_api("/api/po/MarketData/GetTicker", params, HttpMethod.GET)
        return response.json()

    def get_prices(self):
        response = self.client.send_public_api("/api/po/MarketData/GetMarketPrices", None, HttpMethod.GET)
        return response.json()

    def cancel_order(self, id, client='USER1', apikey='Public'):
        params = {'OrderId': id}
        response = self.client.send_public_api("/api/po/Trade/CancelOrder", params, HttpMethod.POST, client, apikey)
        return response.json()

    def get_order_info(self, id, client='USER1', apikey='Public'):
        params = {'OrderId': id}
        response = self.client.send_public_api("/api/po/Trade/GetOrder", params, HttpMethod.POST, client, apikey)
        return response.json()

    def get_user_open_orders(self, client='USER1', apikey='Public', **params):
        response = self.client.send_public_api("/api/po/Account/OpenOrders", params, HttpMethod.POST, client, apikey)
        return response.json()

    def get_user_orders(self, client='USER1', apikey='Public', **params):
        response = self.client.send_public_api("/api/po/Account/GetUserOrders", params, HttpMethod.POST, client, apikey)
        return response.json()

    def create_test_order(self, client='USER1', apikey='Public', **params):
        response = self.client.send_public_api("/api/po/Trade/TestOrder", params, HttpMethod.POST, client, apikey)
        return response.json()

    def modify_order_price(self, client='USER1', apikey='Public', **params):
        response = \
            self.client.send_public_api("/api/po/Trade/ModifyOrderPrice", params, HttpMethod.POST, client, apikey)
        return response.json()

    def get_currencies(self):
        response = \
            self.client.send_public_api("/api/po/MarketData/CurrenciesInfo", None, HttpMethod.GET)
        return response.json()

    def get_currency(self, asset):
        params = {'title': asset}
        response = \
            self.client.send_public_api("/api/po/MarketData/CurrencyInfo", params, HttpMethod.GET)
        return response.json()

    def get_symbols(self):
        response = \
            self.client.send_public_api("/api/po/MarketData/GetSymbols", None, HttpMethod.GET)
        return response.json()

    def get_user_transactions(self, client='USER1', apikey='Public', **params):
        response = \
            self.client.send_public_api("/api/po/Account/GetUserTransactions", params, HttpMethod.POST, client, apikey)
        return response.json()

    def get_address_transaction_history(self, client='USER1', apikey='Public', **params):
        response = self.client.send_public_api("/api/po/Account/GetAddressTransactionHistory", params,
                                               HttpMethod.POST, client, apikey)
        return response.json()

    def get_user_trades(self, client='USER1', apikey='Public', **params):
        response = \
            self.client.send_public_api("/api/po/Account/GetUserTrades", params, HttpMethod.POST, client, apikey)
        return response.json()

    def get_user_address_list(self, client='USER1', apikey='Public', **params):
        response = \
            self.client.send_public_api("/api/po/Account/GetUserAddressListByCurrency", params,
                                        HttpMethod.POST, client, apikey)
        return response.json()

    def get_crypto_address(self, client='USER1', apikey='Public', **params):
        response = \
            self.client.send_public_api("/api/po/Account/GetCryptoAddress", params, HttpMethod.POST, client, apikey)
        return response.json()

    def get_order_book_value(self, **params):
        book_value = self.client.send_public_api("/api/po/MarketData/OrderBookValue", params, HttpMethod.GET)
        return book_value.json()

    def get_common_trades(self, **params):
        book_value = self.client.send_public_api("/api/po/MarketData/GetTrades", params, HttpMethod.GET)
        return book_value.json()




class WebSocketApi:

    def __init__(self):
        self.http_client = HttpClient()

    def custom_exception_handler(self, loop, context):
        loop.default_exception_handler(context)
        loop.stop()

    '''def connect_to_ws(self, market_id, user):
        public_config = configparser.ConfigParser()
        public_config.read(PUBLIC_CONFIG)
        apikey = public_config[user]['Public']
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(self.custom_exception_handler)
        future = loop.create_future()
        loop.create_task(self.http_client.connect_to_ws(future, market_id, apikey))
        websocket = loop.run_until_complete(future)
        return websocket'''

    def connect_to_ws(self, market_id, user, apikey='Public', public_config='./public_api.ini'):
        public_config = configparser.ConfigParser()
        public_config.read(public_config)
        client_id = public_config[user][apikey]
        loop = asyncio.get_event_loop()

        ws = loop.run_until_complete(self.http_client.ws_conn(market_id=market_id, client_id=client_id))
        return ws

    def get_ws_messages(self, websockets, return_dict=None):
        loop = asyncio.get_event_loop()
        if return_dict is None:
            return_dict = {}
        messages = []

        for websocket in websockets:
            msgs = loop.run_until_complete(self.http_client.get_ws_msg(websocket))
            messages.append(msgs)

        for m, i in zip(messages, range(1, len(messages) + 1)):
            user = 'USER' + str(i)
            return_dict[user] = m
        return return_dict

    def get_multiply_users_messages(self, websockets, return_dict):
        proc_list = []

        for websocket, i in zip(websockets, range(len(websockets))):
            user = 'USER' + str(i)
            proc = multiprocessing.Process(target=self.get_ws_messages, args=(websocket, return_dict, user))
            proc_list.append(proc)
            proc.start()
        return proc_list

    '''def get_ws_messages(self, websockets, return_dict=None, multiprocess=False):
        loop = asyncio.get_event_loop()
        if return_dict is None:
            manager = multiprocessing.Manager()
            return_dict = manager.dict()
        future_list = []

        for websocket in websockets:
            future = loop.create_future()
            loop.create_task(self.http_client.get_ws_messages(future, websocket))
            future_list.append(future)

        for future, i in zip(future_list, range(len(future_list))):
            user = 'USER' + str(i+1)
            loop.run_until_complete(future)
            return_dict[user] = future.result()
        if multiprocess is False:
            return return_dict'''


class AsyncPublicApi:

    def __init__(self):
        self.client = HttpClient()

    def _execute_request(self, params_list, rest_dict=None, client='USER1',
                     apikey='Public', ignore_errors=True, exception_queue=None, endpoint=None):
        request_param_list = []

        for params in params_list:
            request_param_list.append([endpoint, params, HttpMethod.POST, client, apikey])
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.client.run_requests(request_param_list))
        try:
            result = loop.run_until_complete(future)
        except ContentTypeError as e:
            if exception_queue is None:
                raise e
            else:
                exception_queue.put(e.message)
                raise e

        if ignore_errors is False:
            for order in result:
                if 'error' in order:
                    if exception_queue is None:
                        raise AssertionError(order)
                    else:
                        exception_queue.put(order)
        if rest_dict is None:
            return result
        else:
            rest_dict[client] = result

    def create_order(self, params_list, rest_dict=None, client='USER1',
                     apikey='Public', ignore_errors=True, exception_queue=None):

        """
        :param params_list: list of dictionaries, each dictionary is /Trade/CreateOrder parameters. For example:
        params_list = \
        [
        {'Market': 'ZEC/USD', 'OrderSide': 'Ask, 'OrderType': 'Limit', 'AccountType': 'Trade', 'Amount': 1, 'Price': 1},
        {'Market': 'ZEC/USD', 'OrderSide': 'Ask, 'OrderType': 'Limit', 'AccountType': 'Trade', 'Amount': 2, 'Price': 2}
        ]
        :param rest_dict: multiprocessing.Manager().dict() If defined, pass function result to multiprocess manager
        :param exception_queue: multiprocessing.SimpleQueue() Should be defined, if function is used in a child process
        """
        endpoint = '/api/po/Trade/CreateOrder'
        return self._execute_request(params_list, rest_dict, client, apikey, ignore_errors, exception_queue, endpoint)

    def create_withdrawal(self, params_list, rest_dict=None, client='USER1',
                          apikey='Public', ignore_errors=True, exception_queue=None):
        endpoint = '/api/po/Account/CreateWithdrawal'
        return self._execute_request(params_list, rest_dict, client, apikey, ignore_errors, exception_queue, endpoint)

    def create_code(self, params_list, rest_dict=None, client='USER1',
                          apikey='Public', ignore_errors=True, exception_queue=None):
        endpoint = '/api/po/Account/CreateCode'
        return self._execute_request(params_list, rest_dict, client, apikey, ignore_errors, exception_queue, endpoint)

    def cancel_order(self, id_list, client='USER1', apikey='Public', exception_queue=None):
        request_param_list = []
        for id in id_list:
            params = {'OrderId': id}
            request_param_list.append(['/api/po/Trade/CancelOrder', params, HttpMethod.POST, client, apikey])
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.client.run_requests(request_param_list))
        try:
            loop.run_until_complete(future)
        except ContentTypeError as e:
            if exception_queue is None:
                raise e
            else:
                exception_queue.put(e.message)
                raise e
