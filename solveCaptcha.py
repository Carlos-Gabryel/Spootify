import sys
import os
from twocaptcha import TwoCaptcha

def solve_captcha(sitekey, url):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    api_key = os.getenv('APIKEY_2CAPTCHA', '9c11761db13252d7b40713e0a1beb48a')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url,
            enterprise=1
            )

    except Exception as e:
        print(e)

    else:
        return result