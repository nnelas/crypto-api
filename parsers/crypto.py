from flask_restplus import reqparse


def get_parser_price():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "coin",
        type=str.upper,
        required=True,
        help="Symbol of the coin to search"
    )
    parser.add_argument(
        "currency",
        type=str.upper,
        choices=["USD", "ETH"],
        default="ETH",
        help="Currency in which price is returned. Supported currencies: 'USD', 'ETH'"
    )
    return parser
