import datetime
import logging

import requests
from celery.schedules import crontab

from alerts.mail import send_email
from crypto_celery import worker
from settings import (
    api as settings,
    alerts as alerts_settings
)


@worker.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/10'), verify_price.s())


@worker.task
def verify_price():
    today = datetime.datetime.today()

    actual_price = get_currency_price_usd("APPC")["price"]

    logging.info('[{}] Checking APPC price (USD)...'.format(today))
    if actual_price > alerts_settings.ALERT_THRESHOLD:
        logging.info("Sending email alert!")

        mail_subject = "ALERT - {}".format(today.strftime("%Y-%m-%d"))

        mail_body = 'APPC is higher than threshold: \n' + \
                    '- Actual value: {}'.format(actual_price) + "\n" + \
                    '- Threshold defined: {}'.format(alerts_settings.ALERT_THRESHOLD)

        send_email(mail_subject, mail_body,
                   alerts_settings.FROM_ADDR, alerts_settings.TO_ADDR,
                   alerts_settings.SMTP_HOST, alerts_settings.SMTP_PORT,
                   alerts_settings.SMTP_USER, alerts_settings.SMTP_PASS)
    else:
        logging.info("Keeping it cool :)")


@worker.task
def get_currency_info(currency: str):
    logging.info("Getting info for currency: '{}'".format(currency))
    data = {
        "symbol": currency
    }
    response = requests.get(settings.COINMARKETCAP_DOMAIN + "/v1/cryptocurrency/map",
                            headers=settings.COINMARKETCAP_HEADERS, params=data)

    if response.status_code != 200:
        return response.status_code

    return response.json()["data"][0]


@worker.task
def get_currency_price_eth(currency: str):
    logging.info("Getting price (ETH) for currency: '{}'".format(currency))
    data = {
        "symbol": currency + "ETH"
    }
    response = requests.get(settings.BINANCE_DOMAIN + "/api/v3/ticker/price", params=data)

    if response.status_code != 200:
        return response.status_code

    return response.json()


@worker.task
def get_currency_price_usd(currency: str):
    logging.info("Getting price (USD) for currency: '{}'".format(currency))
    data = {
        "symbol": currency
    }
    response = requests.get(
        settings.COINMARKETCAP_DOMAIN + "/v1/cryptocurrency/quotes/latest",
        headers=settings.COINMARKETCAP_HEADERS, params=data)

    if response.status_code != 200:
        return response.status_code

    return response.json()["data"][currency]["quote"]["USD"]
