import requests
import json
import urllib.parse
from typing import Literal
# Local imports
from . import utils

class OKX:
    HEADER = {
        "OK-ACCESS-KEY": None,            # The APIKey as a String.
        "OK-ACCESS-SIGN": None,           # The Base64-encoded signature (see Signing Messages subsection for details).
        "OK-ACCESS-TIMESTAMP": None,       # The UTC timestamp of your request .e.g : 2020-12-08T09:08:57.715Z
        "OK-ACCESS-PASSPHRASE": None,     # The passphrase you specified when creating the APIKey.
    }
    BASE_URL="https://www.okx.com"
    
    
    def __init__(self, api_key, api_secret, passphrase) -> None:
        self.API_KEY = str(api_key)
        self.API_SECRET = str(api_secret)
        self.PASSPHRASE = str(passphrase)


    def _get_header(self, request='GET', endpoint='', body:dict=dict()):
        cur_time = utils.get_timestamp()
        header = dict()
        header['CONTENT-TYPE'] = 'application/json'
        header['OK-ACCESS-KEY'] = self.API_KEY
        header['OK-ACCESS-SIGN'] = utils.sign(cur_time, request, endpoint, body, self.API_SECRET)
        header['OK-ACCESS-TIMESTAMP'] = str(cur_time)
        header['OK-ACCESS-PASSPHRASE'] = self.PASSPHRASE
        return header
    

    def send_signed_request(self, http_method:Literal["GET", "POST", "DELETE", "PUT"], url_path:str, payload={}):
        url = OKX.BASE_URL + url_path
        headers = self._get_header(request=http_method, endpoint=url_path, body=payload)
        # response = requests.request(http_method, url=url, headers=headers, data=json.dumps(payload))
        if http_method == 'POST':
            response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        elif http_method == 'GET':
            response = requests.get(url=url, headers=headers)
        return json.loads(response.text)


    def get_account_balance(self, **kwargs):
        r"""Retrieve a list of assets (with non-zero balance), remaining balance, and available amount in the trading account.

        :param ccy: (optional) Single currency or multiple currencies (no more than 20) separated with comma, e.g. BTC or BTC,ETH.
        """
        params = utils.validate_kwargs(kwargs, [], ["ccy"])
        query_string = utils.urlencode(**params)
        return self.send_signed_request("GET", f"/api/v5/account/balance{query_string}")
    

    def place_order(self, **kwargs):
        r"""Place order

        :param instId: Instrument ID, e.g. BTC-USD-190927-5000-C
        :param tdMode: Trade mode, Margin mode `cross` `isolated`, Non-Margin mode `cash`
        :param ccy: (optional) Margin currency, Only applicable to `cross MARGIN` orders in `Single-currency margin`
        :param clOrdId: (optional) Client Order ID as assigned by the client. A combination of case-sensitive alphanumerics, all numbers, or all letters of up to 32 characters.
        :param tag: (optional) Order tag, A combination of case-sensitive alphanumerics, all numbers, or all letters of up to 16 characters.
        :param side: Order side, `buy` `sell`
        :param posSide: (conditional) Position side. The default is `net` in the `net` mode. It is required in the `long/short` mode, and can only be `long` or `short`. Only applicable to `FUTURES/SWAP`.
        :param ordType: Order type. `market`: Market order, `limit`: Limit order, `post_only`: Post-only order, `fok`: Fill-or-kill order, `ioc`: Immediate-or-cancel order, `optimal_limit_ioc`: Market order with immediate-or-cancel order (applicable only to Futures and Perpetual swap).
        :param sz: Quantity to buy or sell
        :param px: (conditional) Order price. Only applicable to `limit`,`post_only`,`fok`,`ioc` order.
        :param reduceOnly: (optional) Whether orders can only reduce in position size. Valid options: `true` or `false`. The default value is false. Only applicable to `MARGIN` orders, and `FUTURES/SWAP` orders in `net` mode. Only applicable to `Single-currency margin` and `Multi-currency margin`
        :param tgtCcy: (optional) Whether the target currency uses the quote or base currency. `base_ccy`: Base currency, `quote_ccy`: Quote currency. Only applicable to SPOT Market Orders. Default is `quote_ccy` for buy, `base_ccy` for sell.
        :param banAmend Boolean: Whether to disallow the system from amending the size of the SPOT Market Order. Valid options: `true` or `false`. The default value is `false`. If `true`, system will not amend and reject the market order if user does not have sufficient funds. Only applicable to SPOT Market Orders
        :param tpTriggerPx String: (optional) Take-profit trigger price. If you fill in this parameter, you should fill in the take-profit order price as well.
        :param tpOrdPx String: (optional) Take-profit order price. If you fill in this parameter, you should fill in the take-profit trigger price as well. If the price is -1, take-profit will be executed at the market price.
        :param slTriggerPx String: (optional) Stop-loss trigger price. If you fill in this parameter, you should fill in the stop-loss order price.
        :param slOrdPx String: (optional) Stop-loss order price. If you fill in this parameter, you should fill in the stop-loss trigger price. If the price is -1, stop-loss will be executed at the market price.
        :param tpTriggerPxType String: (optional) Take-profit trigger price type. `last`: last price, `index`: index price, `mark`: mark price. The Default is `last`
        :param slTriggerPxType String: (optional) Stop-loss trigger price type. `last`: last price, `index`: index price, `mark`: mark price. The Default is `last`
        :param quickMgnType String: (optional) Quick Margin type. Only applicable to Quick Margin Mode of isolated margin `manual`, `auto_borrow`, `auto_repay`. The default value is `manual`


        You can place an order only if you have sufficient funds.
        For leading contracts, this endpoint supports placement, but can't close positions.

        Rate Limit: 60 requests per 2 seconds
        Rate Limit of leading contracts for Copy Trading: 1 requests per 2 seconds
        Rate limit rule (except Options): UserID + Instrument ID
        Rate limit rule (Options only): UserID + Instrument Family
        """
        kwargs = utils.validate_kwargs(kwargs, ["instId", "tdMode", "side", "ordType", "sz"], ["ccy", "clOrdId", "tag", "reduceOnly", "tgtCcy", "banAmend", "tpTriggerPx", "tpOrdPx", "slTriggerPx", "slOrdPx", "tpTriggerPxType", "slTriggerPxType", "quickMgnType"] + ["posSide", "px"])
        return self.send_signed_request("POST", "/api/v5/trade/order", payload=kwargs)
    

    def cancel_order(self, **kwargs):
        r"""
        Cancel order

        :param instId String: Instrument ID, e.g. `BTC-USD-190927`
        :param ordId String: (conditional) Order ID. Either `ordId` or `clOrdId` is required. If both are passed, ordId will be used.
        :param clOrdId String: (conditional) Client Order ID as assigned by the client
        """
        kwargs = utils.validate_kwargs(kwargs, ["instId"], ["ordId", "clOrdId"])
        return self.send_signed_request("POST", "/api/v5/trade/cancel-order", payload=kwargs)


    def get_order_list(self, **kwargs):
        r"""
        Get order List
        Retrieve all incomplete orders under the current account.

        :param instType String: (optional) Instrument type. `SPOT` `MARGIN` `SWAP` `FUTURES` `OPTION`
        :param uly String: (optional) Underlying
        :param instFamily: (optional) Instrument family. Applicable to `FUTURES/SWAP/OPTION`
        :param instId: (optional) Instrument ID, e.g. `BTC-USD-200927`
        :param ordType: (optional) Order type. `market`: Market order, `limit`: Limit order, `post_only`: Post-only order, `fok`: Fill-or-kill order, `ioc`: Immediate-or-cancel order, `optimal_limit_ioc`: Market order with immediate-or-cancel order
        :param state: (optional) State. `live` `partially_filled`
        :param after String: (optional) Pagination of data to return records earlier than the requested `ordId`
        :param before String: (optional) Pagination of data to return records newer than the requested `ordId`
        :param limit String: (optional) Number of results per request. The maximum is `100`; The default is `100`
        """
        kwargs = utils.validate_kwargs(kwargs, [], ["instType", "uly", "instFamily", "instId", "ordType", "state", "after", "before", "limit"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/trade/orders-pending{query_string}")
    

    def get_currencies(self, **kwargs):
        """
        Retrieve a list of all currencies.
        
        :param ccy String: (optional) Single currency or multiple currencies (no more than 20) separated with comma, e.g. `BTC` or `BTC,ETH`.
        """
        kwargs = utils.validate_kwargs(kwargs, [], ["ccy"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/asset/currencies{query_string}")
    

    def get_balance(self, **kwargs):
        """
        Retrieve the balances of all the assets and the amount that is available or on hold.

        :param ccy String: Single currency or multiple currencies (no more than 20) separated with comma, e.g. `BTC` or `BTC,ETH`.
        """
        kwargs = utils.validate_kwargs(kwargs, [], ["ccy"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/asset/balances{query_string}")


    def get_account_asset_valuation(self, **kwargs):
        """
        View account asset valuation

        :param ccy String: Asset valuation calculation unit. BTC, USDT, USD, CNY, JP, KRW, RUB, EUR, VND, IDR, INR, PHP, THB, TRY, AUD, SGD, ARS, SAR, AED, IQD. The default is the valuation in BTC.
        """
        kwargs = utils.validate_kwargs(kwargs, [], ["ccy"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/asset/asset-valuation{query_string}")


    def transfer_funds(self, **kwargs):
        """
        Funds transfer

        :param ccy String: Currency, e.g. `USDT`
        :param amt String: Amount to be transferred
        :param from String: The remitting account. `6`: Funding account, `18`: Trading account
        :param to String: The beneficiary account. `6`: Funding account, `18`: Trading account
        :param subAcct String: (conditional) Name of the sub-account. When `type` is 1, 2 or 4, sub-account is required.
        :param type String: (optional) Transfer type. `0`: transfer within account, `1`: master account to sub-account (Only applicable to APIKey from master account), `2`: sub-account to master account (Only applicable to APIKey from master account), `3`: sub-account to master account (Only applicable to APIKey from sub-account), `4`: sub-account to sub-account (Only applicable to APIKey from sub-account, and target account needs to be another sub-account which belongs to same master account), The default is `0`.
        :param loanTrans Boolean: (optional) Whether or not borrowed coins can be transferred out under `Multi-currency margin` and `Portfolio margin`. the default is `false`
        :param omitPosRisk String: (optional) Ignore position risk. Default is `false`. Applicable to `Portfolio margin`
        """
        kwargs = utils.validate_kwargs(kwargs, ["ccy", "amt", "from", "to"], ["type", "loanTrans", "omitPosRisk"] + ["subAcct"])
        return self.send_signed_request("POST", f"/api/v5/asset/transfer", payload=kwargs)
    

    def get_funds_transfer_state(self, **kwargs):
        """
        Retrieve the transfer state data of the last 2 weeks.

        :param transId String: (conditional) Transfer ID. Either transId or clientId is required. If both are passed, transId will be used.
        :param clientId String: (conditional) Client-supplied ID. A combination of case-sensitive alphanumerics, all numbers, or all letters of up to 32 characters.
        :param type String: (optional) Transfer type. `0`: transfer within account, `1`: master account to sub-account (Only applicable to API Key from master account), `2`: sub-account to master account (Only applicable to API Key from master account), `3`: sub-account to master account (Only applicable to APIKey from sub-account), `4`: sub-account to sub-account (Only applicable to APIKey from sub-account, and target account needs to be another sub-account which belongs to same master account). The default is `0`
        """
        params = utils.validate_kwargs(kwargs, [], ["transId", "clientId", "type"])
        query_string = utils.urlencode(**params)
        return self.send_signed_request("GET", f"/api/v5/asset/transfer-state{query_string}")


    def get_deposit_address(self, **kwargs):
        """
        Retrieve the deposit addresses of currencies, including previously-used addresses.

        :param ccy String: 	Currency, e.g. `BTC`
        """
        params = utils.validate_kwargs(kwargs, ["ccy"])
        query_string = utils.urlencode(**params)
        return self.send_signed_request("GET", f"/api/v5/asset/deposit-address{query_string}")


    def get_instruments(
            self, 
            instType:Literal["SPOT", "MARGIN", "SWAP", "FUTURES", "OPTION"]="SPOT",
            uly=None,
            instFamily=None,
            instId=None,
        ):
        """
        :param instType: Instrument type. `SPOT` `MARGIN` `SWAP` `FUTURES` `OPTION`
        :param uly: (conditional) Underlying. Only applicable to `FUTURES/SWAP/OPTION`. If instType is `OPTION`, either `uly` or `instFamily` is required.
        :param instFamily: (conditional) Instrument family. Only applicable to `FUTURES/SWAP/OPTION`. If instType is `OPTION`, either `uly` or `instFamily` is required.
        :param instId: (optional) Instrument ID
        """
        params = {
            "instType": instType,
        }
        if uly: params["uly"] = uly
        if instFamily: params["instFamily"] = instFamily
        elif instId: params["instId"] = instId
        query_string = utils.urlencode(**params)
        return self.send_signed_request("GET", f"/api/v5/public/instruments{query_string}")
    
    
    def get_subaccount_list(self, **kwargs):
        """
        :param enable: (optional) Sub-account status, `true`: Normal ; `false`: Frozen
        :param subAcct: (optional) Sub-account name
        :param after: (optional) If you query the data prior to the requested creation time ID, the value will be a Unix timestamp in millisecond format.
        :param before: (optional) If you query the data after the requested creation time ID, the value will be a Unix timestamp in millisecond format.
        :param limit: (optional) Number of results per request. The maximum is 100. The default is 100.
        """
        params = utils.validate_kwargs(kwargs, [], ['enable', 'subAcct', 'after', 'before', 'limit',])
        query_string = utils.urlencode(**params)
        return self.send_signed_request("GET", f"/api/v5/users/subaccount/list{query_string}")
    

# Broker Client
class OKXBroker(OKX):
    def __init__(self, api_key, api_secret, passphrase) -> None:
        super().__init__(api_key, api_secret, passphrase)


    def get_broker_account_info(self):
        """
        Retrieve broker account information
        """
        return self.send_signed_request("GET", "/api/v5/broker/nd/info")
    
    
    def create_subaccount(self, **kwargs):
        """
        Create a sub-account from the broker master account.
        :param subAcct String: Sub-account name. 6-20 letters (case sensitive) or numbers, which can be pure letters and not pure numbers.
        :param label String: (optional) Sub-account notes. No more than 50 letters (case sensitive) or numbers, which can be pure letters or pure numbers.
        """
        kwargs = utils.validate_kwargs(kwargs, ["subAcct"], ["label"])
        return self.send_signed_request("POST", "/api/v5/broker/nd/create-subaccount", payload=kwargs)
    

    def delete_subaccount(self, **kwargs):
        """
        Before the sub-account can be deleted, all funds must be transferred from this sub-account.
        :param subAcct String: 	Sub-account name
        """
        kwargs = utils.validate_kwargs(kwargs, ["subAcct"])
        return self.send_signed_request("POST", "/api/v5/broker/nd/delete-subaccount", payload=kwargs)


    def get_subaccount_list(self, **kwargs):
        """
        Get details of the sub-account list
        :param subAcct String: (optional) Sub-account name
        :param page String: (optional) Page for pagination
        :page limit String: (optional) Number of results per request. The maximum is `100`; the default is `100`
        """
        kwargs = utils.validate_kwargs(kwargs, [], ["subAcct", "page", "limit"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/broker/nd/subaccount-info{query_string}")
    

    def create_api_key_for_subaccount(self, **kwargs):
        """
        Create an APIKey for a sub-account.
        Applies to master accounts only. Only API keys with `Trade` privilege can call this endpoint.
        :param subAcct String: Sub-account name, supports 6 to 20 characters that include numbers and letters (case sensitive, space character is not supported).
        :param label String: 	API Key note. No more than 50 letters (case sensitive) or numbers, which can be pure letters or pure numbers.
        :param passphrase String: API Key password, supports 8 to 32 alphanumeric characters containing at least 1 number, 1 uppercase letter, 1 lowercase letter and 1 special character.
        :param ip String: (conditional) Link IP addresses, separate with commas if more than one. Support up to 20 addresses. If sub-account API Key has trade permission, linking IP addresses is required.
        :param perm String: (optional) API Key permissions. `read_only`: Read only, `trade`: Trade, `withdraw`: Withdraw, `read_only` by default
        """
        utils.require_kwargs(["subAcct", "label", "passphrase"], **kwargs)
        return self.send_signed_request("POST", "/api/v5/broker/nd/subaccount/apikey", payload=kwargs)
    

    def get_api_key_of_subaccount(self, **kwargs):
        """
        Query the APIKey of a sub-account
        :param subAcct String: Sub-account name
        :param apiKey String: (optional) API public key
        """
        kwargs = utils.validate_kwargs(kwargs, ["subAcct"], ["apiKey"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/broker/nd/subaccount/apikey{query_string}")


    def reset_api_key_of_subaccount(self, **kwargs):
        """
        Reset the APIKey of a sub-account
        :param subAcct String: Sub-account name
        :param apiKey String: API public key
        :param label String: (optional) API Key note. No more than 50 letters (case sensitive) or numbers, which can be pure letters or pure numbers. The field will be reset if set.
        :param perm String: (optional) API Key permissions. `read_only`: Read only, `trade`: Trade, `withdraw`: Withdraw. Separate with commas if more than one. The field will be reset if set.
        :param ip String: (optional) Link IP addresses, separate with commas if more than one. Support up to 20 IP addresses. The field will be reset if set. If sub-account APIKey has trade permission, linking IP addresses is required.
        """
        utils.require_kwargs(["subAcct", "apiKey"], **kwargs)
        return self.send_signed_request("POST", "/api/v5/broker/nd/subaccount/modify-apikey", payload=kwargs)
    
    
    def delete_api_key_of_subaccount(self, **kwargs):
        """
        Delete the APIKey of sub-accounts
        :param subAcct String: 	Sub-account name
        :param apiKey String: 	API public key
        """
        utils.require_kwargs(["subAcct", "apiKey"], **kwargs)
        return self.send_signed_request("POST", "/api/v5/broker/nd/subaccount/delete-apikey", payload=kwargs)
    
    
    def set_subaccount_level(self, **kwargs):
        """
        Set the account level of the sub-account
        :param subAcct String: Sub-account name
        :param acctLv String: Account level. `1`: Simple, `2`: Single-currency margin, `3`: Multi-currency margin, `4`: Portfolio margin
        """
        utils.require_kwargs(["subAcct", "acctLv"], **kwargs)
        return self.send_signed_request("POST", "/api/v5/broker/nd/set-subaccount-level", payload=kwargs)


    def set_trading_fee_for_subaccount(self, **kwargs):
        """
        Set trading fee rate for the sub-account
        :param instType String: (optional) Instrument type. `SPOT` `MARGIN` `SWAP` `FUTURES` `OPTION`  
        :param mgnType String: (optional) Margin type. `1`: USDT-margined, `2`: crypto-margined. Applicate to `FUTURES/SWAP`
        :param chgType String: (optional) Type of fee rate. `absolute`: Absolute change of the fee rate, `percentage`: Percentage change of the fee rate
        :param chgTaker String: (conditional) Taker fee rate for changing. For `absolute`: The unit is bp (1bp = 0.01%). Range belongs to [0 bp, 1,000bp], same as [0.00%, 10%]. Precision is 0.1 bp. For `percentage`: The unit is percent(%). Range belongs to [0%, 10000%]. Precision is 1%
        :param chgMaker String: (conditoinal) Maker fee rate for changing. For `absolute`: The unit is bp (1bp = 0.01%). Range belongs to [0 bp, 1,000bp], same as [0.00%, 10%]. Precision is 0.1 bp. For `percentage`: The unit is percent(%). Range belongs to [0%, 10000%]. Precision is 1%. Either chgTaker or chgMaker is required.
        """
        kwargs = utils.validate_kwargs(kwargs, [], ["instType"])
        return self.send_signed_request("POST", "POST /api/v5/broker/nd/set-subaccount-fee-rate", payload=kwargs)
    

    def create_deposit_address_for_subaccount(self, **kwargs):
        """
        Create the deposit address for the sub-account from the broker master account Up to 20 deposit addresses for each currency.
        :param subAcct String: Sub-account name
        :param ccy String: Currency, e.g. USDT
        :param chain String: (optional) Chain name, e.g. `USDT-ERC20`, `USDT-TRC20`, `USDT-Omni`. If the parameter is not filled in, the default will be the main chain.
        :param addrType String: (optional) Deposit address type. `1`: Regular addres, `2`: SegWit address. Only applicable to BTC and LTC
        :param to String: (optional) The beneficiary account. `6`: Funding `18`: Trading account. Default is `6`
        """
        kwargs = utils.validate_kwargs(kwargs, ["subAcct", "ccy"], ["chain", "addrType", "to"])
        return self.send_signed_request("POST", "/api/v5/asset/broker/nd/subaccount-deposit-address", payload=kwargs)
    

    def modify_deposit_address_for_subaccount(self, **kwargs):
        """
        Modify deposit address for sub-account.
        :param subAcct String: Sub-account name
        :param ccy String: 	Currency, e.g. USDT
        :param chain String: (optional) Chain name, e.g. `USDT-ERC20`, `USDT-TRC20`, `USDT-Omni`. If the parameter is not filled in, the default will be the main chain.
        :param addr String: Deposit address. Some digital currency addresses are formatted as 'address+tag', e.g. 'ARDOR-7JF3-8F2E-QUWZ-CAN7F:123456'
        :param to String: The beneficiary account. `6`: Funding, `18`: Trading account
        """
        kwargs = utils.validate_kwargs(kwargs, ["subAcct", "ccy", "addr", "to"], ["chain"])
        return self.send_signed_request("POST", "/api/v5/asset/broker/nd/modify-subaccount-deposit-address", payload=kwargs)
    

    def get_subaccount_deposit_address(self, **kwargs):
        """
        Retrieve the deposit addresses of the sub-account.
        :param subAcct String: 	Sub-account name
        :param ccy String: 	Currency, e.g. BTC
        """
        kwargs = utils.validate_kwargs(kwargs, ["subAcct", "ccy"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/asset/broker/nd/subaccount-deposit-address{query_string}")
    

    def get_subaccount_deposit_history(self, **kwargs):
        """
        Retrieve the deposit history of the sub-account.
        :param subAcct String: (optional) Sub-account name
        :param ccy String: (optional) Currency, e.g. `BTC`
        :param txId String: (optional) Hash record of the deposit
        :param type String: (optional) Deposit Type. `3`: internal transfer, `4`: deposit from chain
        :param state String: (optional) Status of deposit. `0`: waiting for confirmation, `1`: deposit credited, `2`: deposit successful, `8`: Pending due to temporary deposit suspension on this crypto currency, `11`: match the address blacklist, `12`: account or deposit is frozen, `13`: sub-account deposit interception
        :param after String: (optional) Pagination of data to return records earlier than the requested ts, Unix timestamp format in milliseconds, e.g. `1597026383085`
        :param before String: (optional) Pagination of data to return records newer than the requested ts, Unix timestamp format in milliseconds, e.g. `1597026383085`
        :param limit String: (optional) Number of results per request. The maximum is `100`; The default is `100`
        """
        kwargs = utils.validate_kwargs(kwargs, [], ["subAcct", "ccy", "txId", "type", "state", "after", "before", "limit"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/asset/broker/nd/subaccount-deposit-history{query_string}")
    

    def get_subaccount_withdrawal_history(self, **kwargs):
        """
        Retrieve the withdrawal history of the sub-account.
        :param subAcct String: (optional) Sub-account name
        :param ccy String: (optional) Currency, e.g. `BTC`
        :param wdId String: (optional) Withdrawal ID
        :param clientId String: (optional) Client-supplied ID. A combination of case-sensitive alphanumerics, all numbers, or all letters of up to 32 characters.
        :param txId String: (optional) Hash record of the deposit
        :param type String: (optional) Withdrawal type. `3`: internal transfer, `4`: withdrawal to chain
        :param state String: (optional) Status of withdrawal. `-3`: canceling, `-2`: canceled, `-1`: failed, `0`: waiting withdrawal, `1`: withdrawing, `2`: withdraw success, `7`: approved, `10`: waiting transfer, `4`, `5`, `6`, `8`, `9`, `12`: waiting mannual review
        :param after String: (optional) Pagination of data to return records earlier than the requested ts, Unix timestamp format in milliseconds, e.g. `1654041600000`
        :param before String: (optional) Pagination of data to return records newer than the requested ts, Unix timestamp format in milliseconds, e.g. `1656633600000`
        :param limit String: (optional) Number of results per request. The maximum is `100`; The default is `100`
        """
        kwargs = utils.validate_kwargs(kwargs, [], ["subAcct", "ccy", "wdId", "clientId", "txId", "type", "state", "after", "before", "limit"])
        query_string = utils.urlencode(**kwargs)
        return self.send_signed_request("GET", f"/api/v5/asset/broker/nd/subaccount-withdrawal-history{query_string}")

