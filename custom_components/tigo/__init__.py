import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import datetime, timedelta, timezone
import aiohttp
import csv
import io

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)

PARAMS = {
    "Pin": "W",
    "Vin": "V",
    "Iin": "A",
    "RSSI": "dBm",
}

async def fetch_tigo_data(system_id: str, token: str) -> dict:
    async def fetch_param(param: str) -> dict:

        today = datetime.now(timezone.utc).date()
        start_time = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc)
        end_time = datetime.combine(today, datetime.max.time(), tzinfo=timezone.utc)

        start = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        

        url = (
            f"https://api2.tigoenergy.com/api/v3/data/aggregate"
            f"?system_id={system_id}&start={start}&end={end}&level=min"
            f"&param={param}&header=id&sensors=true"
        )
        
        headers = {"Authorization": f"Bearer {token}"}

        _LOGGER.debug("Fetching param: %s", param)
        _LOGGER.debug("Fetching url: %s", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.text()
                if response.status != 200:
                    raise UpdateFailed(f"Tigo API error [{param}]: {response.status}")
                return parse_param_csv(text, param, latest_only=True)

    combined: dict[str, dict[str, float]] = {}
    for param in PARAMS:
        param_data = await fetch_param(param)
        for panel_id, value in param_data.items():
            if panel_id not in combined:
                combined[panel_id] = {}
            combined[panel_id][param] = value

    return combined

def parse_param_csv(csv_text: str, param: str, latest_only=False) -> dict:
    result = {}
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    if len(rows) < 2:
        return {}

    headers = rows[0][1:]  # salta Datetime
    values_rows = rows[1:]  # tutte le righe dei dati

    if latest_only:
        # Cerca l'ultima riga con almeno un valore valido
        for row in reversed(values_rows):
            values = row[1:]
            if any(v.strip() not in ("", "NaN") for v in values):
                break
        else:
            return {}  # Nessuna riga valida trovata
    else:
        values = values_rows[0][1:]  # prima riga utile

    for panel_id, value in zip(headers, values):
        try:
            result[str(panel_id)] = float(value)
        except Exception:
            continue

    return result


def parse_csv(csv_text: str) -> dict:
    result = {}
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    if len(rows) < 2:
        return {}
    headers = rows[0][1:]
    values = rows[1][1:]
    for h, v in zip(headers, values):
        try:
            param, panel_id = h.split(":")
            if panel_id not in result:
                result[panel_id] = {}
            result[panel_id][param] = float(v)
        except Exception:
            continue
    return result

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    from .tigo_api import login_and_get_token, get_system_id

    _LOGGER.debug("Setting up Tigo integration")

    try:
        email = entry.data["email"]
        password = entry.data["password"]

        token = await hass.async_add_executor_job(login_and_get_token, email, password)
        system_id = await hass.async_add_executor_job(get_system_id, token)

        async def update_method():
            return await fetch_tigo_data(system_id, token)

        coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name="Tigo Panel Data",
            update_method=update_method,
            update_interval=SCAN_INTERVAL,
        )

        await coordinator.async_config_entry_first_refresh()

        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
            "coordinator": coordinator,
            "token": token,
            "system_id": system_id,
        }

    except Exception as e:
        raise ConfigEntryNotReady(f"Tigo setup failed: {e}")

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("Unloading Tigo integration")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
