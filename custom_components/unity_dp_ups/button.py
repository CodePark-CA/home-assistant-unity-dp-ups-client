from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up UPS buttons based on a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    ups = data["ups"]

    async_add_entities([BatteryTestButton(ups, entry)])

class BatteryTestButton(ButtonEntity):
    """Representation of a UPS battery test button.
    
    This button allows users to manually trigger a battery self-test on the UPS.
    """

    def __init__(self, ups, entry):
        """Initialize the battery test button."""
        self._ups = ups
        self._entry = entry
        self._attr_name = "UPS Manual Battery Test"
        self._attr_unique_id = f"{entry.entry_id}_manual_battery_test"
        self._attr_icon = "mdi:battery-check"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Unity DP UPS",
            manufacturer="Vertiv",
            model="Unity DP",
        )

    async def async_press(self) -> None:
        """Handle the button press to start the manual battery test."""
        await self.hass.async_add_executor_job(self._ups.battery_test)
