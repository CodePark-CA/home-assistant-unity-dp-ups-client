import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback

from .const import DOMAIN
from unity_dp import UPSLibrary

class UnityDPConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Unity DP UPS.
    
    This class manages the user interface and logic for adding a new UPS integration.
    """

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user provides connection details."""
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]

            # Validate the connection
            ups = UPSLibrary(host, username, password)
            # Since UPSLibrary uses requests, we should run it in an executor
            success = await self.hass.async_add_executor_job(ups.login)

            if success:
                return self.async_create_entry(title=f"{ups.system.status.model_number} via {ups.agent.status.model} at {host}", data=user_input)
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
