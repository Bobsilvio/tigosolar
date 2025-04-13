import requests
import logging
_LOGGER = logging.getLogger(__name__)

API_BASE_URL = "https://api2.tigoenergy.com/api/v3"
LOGIN_ENDPOINT = f"{API_BASE_URL}/users/login"
SYSTEMS_ENDPOINT = f"{API_BASE_URL}/systems"
LAYOUT_ENDPOINT = f"{API_BASE_URL}/systems/layout"
VIEW_ENDPOINT = f"{API_BASE_URL}/systems/view"

def login_and_get_token(email: str, password: str) -> str:
    response = requests.get(LOGIN_ENDPOINT, auth=(email, password))
    response.raise_for_status()
    return response.json()["user"]["auth"]

def get_system_id(token: str) -> int:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(SYSTEMS_ENDPOINT, headers=headers)
    response.raise_for_status()
    systems = response.json().get("systems", [])
    if not systems:
        raise ValueError("No systems found for this account")
    return systems[0]["system_id"]

def fetch_system_layout(system_id: int, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(f"{LAYOUT_ENDPOINT}?id={system_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_system_info(system_id: int, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    response = requests.get(f"{VIEW_ENDPOINT}?id={system_id}", headers=headers)
    response.raise_for_status()
    return response.json().get("system", {})

def fetch_system_summary(system_id: int, token: str) -> dict:
    url = f"https://api2.tigoenergy.com/api/v3/data/summary?system_id={system_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    raw = response.json().get("summary", {})

    clean = {}
    for key, val in raw.items():
        try:
            if isinstance(val, (int, float)):
                if "energy" in key.lower():
                    # Converti Wh in kWh
                    clean[key] = round(val / 1000, 2)
                else:
                    # Lascia intatto (es. potenza in Watt)
                    clean[key] = round(val, 2)
        except Exception as e:
            _LOGGER.warning(f"Errore parsing {key}: {val} → {e}")
            continue

    return clean






