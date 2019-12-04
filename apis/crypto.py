from flask_restplus import Namespace, Resource, abort
from parsers import crypto as crypto_parsers


from tasks.crypto import (
    get_currency_info, get_currency_price_eth, get_currency_price_usd
)

api = Namespace("crypto", description="Crypto operations")


@api.route("/status")
class Status(Resource):
    def get(self):
        """Pings the server to ensure it is working as expected"""
        return {'status': 'OK'}


@api.route("/info/<path:coin>")
class Info(Resource):
    @api.response(200, "Success")
    @api.response(400, "Invalid coin")
    @api.response(401, "API key missing.")
    def get(self, coin):
        """ Retrieves detailed information about a coin """
        message = get_currency_info.delay(currency=coin.upper())
        if message.get() in [400, 401]:
            abort(code=message.get(), error="ERROR", status=None)

        return message.get(), 200


@api.route("/price")
class Price(Resource):
    @api.expect(crypto_parsers.get_parser_price())
    @api.response(200, "Success")
    @api.response(400, "Invalid coin")
    @api.response(401, "API key missing.")
    def get(self):
        """ Retrieves actual price of a currency"""
        parser = crypto_parsers.get_parser_price()
        args = parser.parse_args()
        if args.currency == "ETH":
            message = get_currency_price_eth.apply_async(args=[args.coin], priority=9)
            if message.get() in [400, 401]:
                abort(code=message.get(), error="ERROR", status=None)

            return message.get(), 200
        else:
            message = get_currency_price_usd.apply_async(args=[args.coin], priority=9)
            if message.get() in [400, 401]:
                abort(code=message.get(), error="ERROR", status=None)

            return message.get(), 200


@api.route("/offer")
class Offer(Resource):
    def post(self):
        """ To be implemented """
