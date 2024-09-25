from dotenv import load_dotenv
import os
load_dotenv()
import requests

def sendSMS(otp,mobile):
        url = os.getenv("SMS_API")
        senderid = os.getenv("SENDER_ID")
        apikey = os.getenv("SMS_APIKEY")
        clientid = os.getenv("SMS_CLIENT_ID")
        payload = {
            "SenderId": senderid,
            "Message": f"{otp} is the OTP to register with us. This OTP is valid for 5 minutes. Please do not share it with anyone. Quantum IT Solution",
            "MobileNumbers": mobile,
            "ApiKey": apikey,
            "ClientId": clientid
        }
        # print("url : ",url)
        # print("payload : ",payload)
        try:
            response = requests.post(f"{url}/api/v2/SendSMS", json=payload)
            # response.raise_for_status()  # Raise an exception for HTTP errors
            # print("response ==> ",response)
            data = response.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            return str(http_err)
        
        except requests.exceptions.RequestException as err:
            return str(err)
