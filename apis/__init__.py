from flask_restplus import Api

from .crypto import api as crypto_api


api = Api(
    version="1.0",
    title="Crypto API",
    description="An API to manage crypto-currencies",
)

api.add_namespace(crypto_api, "/crypto")
