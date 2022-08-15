from kavenegar import *
from jorvajor.local_setting import API_KEY
from ippanel import Client


# def send_otp_code(phone_number, code):
#     try:
#         api = KavenegarAPI(API_KEY)
#         params = {
#             'sender': '',  # optional
#             'receptor': phone_number,  # multiple mobile number, split by comma
#             'message': f'your code {code}',
#         }
#         response = api.sms_send(params)
#         print(response)
#     except APIException as e:
#         print(e)
#     except HTTPException as e:
#         print(e)

def send_otp_code(phone_number, code):
    # you api key that generated from panel
    api_key = API_KEY

    # create client instance
    sms = Client(api_key)
    bulk_id = sms.send(
        "+98500010400402399",  # originator
        [f"{phone_number}"],  # recipients
        f"{code}"  # message
    )

    response = bulk_id
    print(response)
