 
from datetime import datetime
from typing import List, Dict, Any
import requests

API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_openmeteo(lat: float, lon: float, days: int = 3) -> List[Dict[str, Any]]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "past_days": days,
        "forecast_days": 0,
        "timezone": "UTC",
    }
    resp = requests.get(API_URL, params=params, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    times = payload.get("hourly", {}).get("time", [])
    temp = payload.get("hourly", {}).get("temperature_2m", [])
    precip = payload.get("hourly", {}).get("precipitation", [])
    wind = payload.get("hourly", {}).get("wind_speed_10m", [])
    units = payload.get("hourly_units", {})
    out: List[Dict[str, Any]] = []
    for idx, ts in enumerate(times):
        dt = datetime.fromisoformat(ts)
        if idx < len(temp):
            out.append({"type": "temperature", "value": temp[idx], "unit": units.get("temperature_2m", "C"), "timestamp": dt, "extra": {"lat": lat, "lon": lon}})
        if idx < len(precip):
            out.append({"type": "precipitation", "value": precip[idx], "unit": units.get("precipitation", "mm"), "timestamp": dt, "extra": {"lat": lat, "lon": lon}})
        if idx < len(wind):
            out.append({"type": "windspeed", "value": wind[idx], "unit": units.get("wind_speed_10m", "m/s"), "timestamp": dt, "extra": {"lat": lat, "lon": lon}})
    return out

