from kavenegar import *
from jorvajor.local_setting import API_KEY


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': '',  # optional
            'receptor': phone_number,  # multiple mobile number, split by comma
            'message': f'your code {code}',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
