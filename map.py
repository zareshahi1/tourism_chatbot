import os
from pydantic import BaseModel, Field
import requests


class GeocodeInput(BaseModel):
    address: str = Field(..., description="آدرس متنی برای تبدیل به مختصات")


class GeocodeOutput(BaseModel):
    url: str = Field(..., description="لینک مستقیم گوگل‌مپ برای نمایش مکان")


def geocode_address(input: GeocodeInput) -> GeocodeOutput:
    """دریافت لینک گوگل‌مپ از روی آدرس متنی"""
    url = "https://api.neshan.org/v6/geocoding"
    params = {
        "address": input.address
    }
    headers = {
        "User-Agent": "langgraph-geocoder",
        "Api-Key": os.environ.get("NESHAN_API_KEY")
    }
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return GeocodeOutput(url="Not found")

    lat, lon = data["location"]["y"], data["location"]["x"]
    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    return GeocodeOutput(url=gmaps_url)

