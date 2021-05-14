import json
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import InstaToken


def get_short_lived_token(code):
    payload = {
        "client_id": settings.INSTAGRAM_CLIENT_ID,
        "client_secret": settings.INSTAGRAM_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": settings.INSTAGRAM_REDIRECT_URI,
        "code": code,
    }
    response = requests.post(settings.INSTAGRAM_ACCESS_TOKEN_URL, data=payload)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


def get_long_lived_token(short_lived_token):
    payload = {
        "grant_type": "ig_exchange_token",
        "client_secret": settings.INSTAGRAM_CLIENT_SECRET,
        "access_token": short_lived_token,
    }
    response = requests.get(settings.INSTAGRAM_SHORT_TOKEN_URL, params=payload)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None


@require_http_methods(["GET"])
def generate_long_term_token(request):
    template_name = "instagramgobbler/result.html"
    code = request.GET.get("code")
    if not code:
        return render(request, template_name, {"step": 0})
    short_lived_token_response = get_short_lived_token(code)
    if not short_lived_token_response:
        return render(request, template_name, {"step": 1})
    short_lived_token = short_lived_token_response["access_token"]
    user_id = short_lived_token_response["user_id"]
    long_lived_token_response = get_long_lived_token(short_lived_token)
    if not long_lived_token_response:
        return render(request, template_name, {"step": 2})
    long_lived_token = long_lived_token_response["access_token"]
    expires_in = long_lived_token_response["expires_in"]
    expiry_date = datetime.today() + timedelta(seconds=expires_in)

    _, _ = InstaToken.objects.update_or_create(
        user_id=user_id,
        defaults={
            "expiry_date": expiry_date,
            "long_lived_token": long_lived_token,
        },
    )

    return render(request, template_name, {"step": 4})
