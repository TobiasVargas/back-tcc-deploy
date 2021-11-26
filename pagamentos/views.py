from django.shortcuts import render
import mercadopago
from backend.settings import ACCESS_TOKEN_MELI, PUBLIC_KEY_MELI, NOTIFY_URL, REDIRECT_URI_MERCADO_PAGO, INIT_POINT


def get_btn_pagamento(preco,
                      payer_name,
                      payer_surname,
                      payer_email,
                      payer_address_street_name,
                      payer_address_street_number,
                      payer_address_zip_code,
                      external_reference):
    mp = mercadopago.MP(ACCESS_TOKEN_MELI)
    preference = {
        "items": [
            {
                "title": "TEST.WIKI - Adição de Saldo #" + str(external_reference),
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": preco,
            }
        ],
        "payer": {
            "name": payer_name,
            "surname": payer_surname,
            "email": payer_email,
            "address": {
                "street_name": payer_address_street_name,
                "street_number": payer_address_street_number,
                "zip_code": payer_address_zip_code
            }
        },
        "back_urls": {
            "success": REDIRECT_URI_MERCADO_PAGO,
            "failure": REDIRECT_URI_MERCADO_PAGO,
            "pending": REDIRECT_URI_MERCADO_PAGO
        },
        "auto_return": "all",
        "notification_url": NOTIFY_URL,
        "external_reference": external_reference
    }
    preference_result = mp.create_preference(preference)

    return preference_result['response'][INIT_POINT]
