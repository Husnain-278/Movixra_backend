import requests
from django.conf import settings

def get_paypal_access_token():
    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"
    response = requests.post(
        url,
        auth=(
            settings.PAYPAL_CLIENT_ID,
            settings.PAYPAL_SECRET
        ),
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        data={
            "grant_type": "client_credentials"
        }
    )
    data = response.json()
    return data.get("access_token")


def create_paypal_order(booking):
    access_token = get_paypal_access_token()
    url = f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders"
    headers = { 
     "Content-Type": "application/json",
     "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units":[
            {
                "amount":{
                    "currency_code": "USD",
                    "value": str(booking.total_amount)
                }
            }
        ],
        "application_context":{
            "brand_name": "Movixra",
            "landing_page": "NO_PREFERENCE",
            "user_action": "PAY_NOW",
            "return_url": "http://localhost:3000/payment-success",
            "cancel_url": "http://localhost:3000/payment-cancel",
        }
    }
    
    response = requests.post(
        url,
        json=payload,
        headers=headers
    )
    data = response.json()
    return data