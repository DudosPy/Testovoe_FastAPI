import requests
from app.redis_cache import redis_client

def get_usd_to_rub_rate() -> float:
    cached_rate = redis_client.get("usd_to_rub_rate")
    if cached_rate:
        return float(cached_rate)

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    response.raise_for_status()
    usd_rate = response.json()["Valute"]["USD"]["Value"]

    redis_client.set("usd_to_rub_rate", usd_rate, ex=300)

    return usd_rate