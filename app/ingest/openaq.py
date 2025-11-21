from datetime import datetime
from typing import List, Dict, Any
import requests

LOCATIONS_URL = "https://api.openaq.org/v3/locations"


class OpenAQAuthError(RuntimeError):
    pass


class OpenAQNotFound(RuntimeError):
    pass


def fetch_openaq(lat: float, lon: float, api_key: str | None, radius_m: int = 10000, limit: int = 1) -> List[Dict[str, Any]]:
    """
    Récupère les dernières mesures d'une station OpenAQ proche d'un point (lat/lon).
    - Cherche la station la plus proche via /v3/locations
    - Récupère ses mesures récentes via /v3/locations/{id}/latest
    """
    if not api_key:
        raise OpenAQAuthError("OPENAQ_API_KEY manquant (l'API v3 l'exige).")

    headers = {"X-API-Key": api_key}
    params = {"coordinates": f"{lat},{lon}", "radius": radius_m, "limit": limit}
    loc_resp = requests.get(LOCATIONS_URL, params=params, headers=headers, timeout=30)
    loc_resp.raise_for_status()
    locations = loc_resp.json().get("results", [])
    if not locations:
        raise OpenAQNotFound("Aucune station OpenAQ trouvée à proximité.")

    location = locations[0]
    location_id = location.get("id")
    sensor_map = {s["id"]: s for s in location.get("sensors", []) if s.get("id")}

    latest_resp = requests.get(f"{LOCATIONS_URL}/{location_id}/latest", headers=headers, timeout=30)
    latest_resp.raise_for_status()
    measurements = latest_resp.json().get("results", [])

    out: List[Dict[str, Any]] = []
    for item in measurements:
        ts = item.get("datetime", {}).get("utc")
        if not ts:
            continue
        sensor_id = item.get("sensorsId")
        param_info = sensor_map.get(sensor_id, {}).get("parameter", {}) if sensor_id else {}
        out.append(
            {
                "type": param_info.get("name") or "unknown",
                "value": item.get("value"),
                "unit": param_info.get("units") or "",
                "timestamp": datetime.fromisoformat(ts.replace("Z", "+00:00")),
                "extra": {
                    "coordinates": item.get("coordinates"),
                    "location_id": location_id,
                    "sensor_id": sensor_id,
                },
            }
        )
    return out
