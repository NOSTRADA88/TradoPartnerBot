import datetime
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import httpx


__domain = 'https://test.tradoclub.ru/'


async def get_encoded_data():
    payload = {
        "time": datetime.datetime.now().timestamp()
    }

    with open('config_data/public_key.pem', 'rb') as key_file:
        __public_key = serialization.load_pem_public_key(
            key_file.read(),
        )

    __json_data = json.dumps(payload).encode('utf-8')

    __encrypted_data = __public_key.encrypt(
        __json_data,
        padding.PKCS1v15()
    )

    encoded_data = base64.b64encode(__encrypted_data)
    return encoded_data


async def get_token():
    encoded_data = await get_encoded_data()
    reqeust = httpx.post(
        url=f'{__domain}/mlm2/api/bot/get-token',
        data=encoded_data,
        headers={
            "Content-Type": "text/plain"
        }
    )
    return reqeust.json()['token']


async def get_user_id(phone_number):

    encoded_data = await get_encoded_data()

    reqeust = httpx.post(
        url=f'{__domain}/mlm2/api/bot/{await get_token()}/authorise/{phone_number}',
        data=encoded_data,
        headers={
            "Content-Type": "text/plain"
        }
    )
    return reqeust.json()['id'] if reqeust.json()['user_is_exist'] == 'true' else False


async def get_referrals(user_id):

    encoded_data = await get_encoded_data()

    reqeust = httpx.post(
        url=f'{__domain}/mlm2/api/bot/{await get_token()}/user/{user_id}/referral-links',
        data=encoded_data,
        headers={
            "Content-Type": "text/plain"
        }
    )
    return reqeust.json()


async def get_account_details(user_id):

    encoded_data = await get_encoded_data()

    reqeust = httpx.post(
        url=f'{__domain}/mlm2/api/bot/{await get_token()}/user/{user_id}/detailed_information',
        data=encoded_data,
        headers={
            "Content-Type": "text/plain"
        }
    )
    return reqeust.json()


async def get_clients(user_id):

    encoded_data = await get_encoded_data()

    reqeust = httpx.post(
        url=f'{__domain}/mlm2/api/bot/{await get_token()}/user/{user_id}/clients',
        data=encoded_data,
        headers={
            "Content-Type": "text/plain"
        }
    )
    return reqeust.json()
