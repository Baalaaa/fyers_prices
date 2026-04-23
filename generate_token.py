import os

from fyers_apiv3 import fyersModel
from dotenv import load_dotenv

# --- Load .env Files ---
load_dotenv()


# --- Class FyersToken ---
class FyersToken:

    # --- Default Constructor ---
    def __init__(self):
        self.APP_ID = os.getenv("APP_ID")
        self.APP_SECRET = os.getenv("APP_SECRET")
        self.REDIRECT_URI = os.getenv("REDIRECT_URI")
        self.session = fyersModel.SessionModel(
            client_id=self.APP_ID,
            secret_key=self.APP_SECRET,
            redirect_uri=self.REDIRECT_URI,
            response_type='code',
            grant_type='authorization_code'
        )


    # --- Generate Url Func ---
    def generate_url(self):
        """Generate Login URL for Fyers API"""

        login_url = self.session.generate_authcode()
        print(login_url)



    # ---- Access Token Func ----
    def generate_access_token(self, auth_code: str):
        """Generate access token for Fyers API"""

        try:
            self.session.set_token(auth_code)

            # Generate Access Token
            response = self.session.generate_token()
            print(response)
            if response.get("s") != "ok":
                print("Error:", response)
                return

            access_token = response['access_token']
            print(f"Access Token Generated: {access_token} !")

            # Save it
            with open("access_token.txt", "w") as file:
                file.write(access_token)

        except Exception as e:
            print(e)

if __name__ == '__main__':

    # 1
    fy_obj = FyersToken()

    # 2
    fy_obj.generate_url()

    auth_code = input("Enter Authorization Code: ")
    #3
    fy_obj.generate_access_token(auth_code)