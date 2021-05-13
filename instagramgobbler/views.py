from django.http import HttpResponse
import requests
from django.conf import settings
import json
from .models import InstaToken
from datetime import datetime
from datetime import timedelta


def generate_long_term_token(request):
    if request.method == "GET":
        code = request.GET.get("code")
        if not code:
            return HttpResponse(
                """<html><body>NO CODE TO GOBBLE SORRY
                    I CANT DO ANYTHING</body></html>"""
            )
        payload = {
            "client_id": settings.INSTAGRAM_CLIENT_ID,
            "client_secret": settings.INSTAGRAM_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": settings.INSTAGRAM_REDIRECT_URI,
            "code": code,
        }
        response = requests.post(settings.INSTAGRAM_ACCESS_TOKEN_URL, data=payload)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            short_lived_token = response_json["access_token"]
            user_id = response_json["user_id"]
            long_lived_token_url = f"""https://graph.instagram.com/access_token?
                grant_type=ig_exchange_token&client_secret="
                {settings.INSTAGRAM_CLIENT_SECRET}
                &access_token={short_lived_token}"""
            long_lived_response = requests.get(long_lived_token_url)

            if long_lived_response.status_code == 200:
                long_lived_json = json.loads(response.text)
                long_lived_token = long_lived_json["access_token"]
                expires_in = long_lived_json["expires_in"]
                expiry_date = datetime.today() + timedelta(seconds=expires_in)

                insta_token_obj, _ = InstaToken.objects.update_or_create(
                    user_id=user_id,
                    defaults={
                        "expiry_date": expiry_date,
                        "long_lived_token": long_lived_token,
                    },
                )
                html = "<html><body>It worked</body></html>"
            else:
                html = "<html><body>Something went wrong with getting the long life token</body></html>"
        else:
            html = "<html><body>Something went wrong with getting the short life token</body></html>"

        return HttpResponse(html)
