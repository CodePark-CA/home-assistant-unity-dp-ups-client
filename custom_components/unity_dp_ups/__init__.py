import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from unity_dp import UPSLibrary

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Unity DP UPS from a config entry."""
    # Fix entry title if it contains the old format or "None"
    if "None" in entry.title or "via" in entry.title:
        host = entry.data.get(CONF_HOST, "")
        # Try to get model from current data if available, but for now just use a better default
        new_title = f"Unity DP UPS at {host}"
        hass.config_entries.async_update_entry(entry, title=new_title)

    host = entry.data[CONF_HOST]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    ups = UPSLibrary(host, username, password)

    async def async_update_data():
        """Fetch data from UPS. This is the main update function for the coordinator."""
        try:
            # We use executor because UPSLibrary is synchronous
            data = await hass.async_add_executor_job(ups.get_all_status)
            if not data:
                raise UpdateFailed("Error communicating with UPS")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with UPS: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="UPS",
        update_method=async_update_data,
        update_interval=timedelta(seconds=60),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "ups": ups,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry and clean up resources."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
