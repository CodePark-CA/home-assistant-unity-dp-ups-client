from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

def get_ups_device_info(entry_id: str, data: dict) -> DeviceInfo:
    """Return device info for the UPS."""
    system_status = data.get("system", {}).get("status", {})
    manufacturer = system_status.get("manufacturer")
    if not manufacturer or manufacturer == "--":
        manufacturer = "Vertiv"
    
    model = system_status.get("model_number")
    if not model or model == "--":
        model = "Unity DP"

    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry_id}_ups")},
        name=f"{manufacturer} UPS",
        manufacturer=manufacturer,
        model=model,
        via_device=(DOMAIN, f"{entry_id}_agent"),
    )

def get_agent_device_info(entry_id: str, data: dict) -> DeviceInfo:
    """Return device info for the Agent (Unity Card)."""
    agent_status = data.get("agent", {}).get("status", {})
    model = agent_status.get("model")
    if not model or model == "--":
        model = "IntelliSlot Unity"

    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry_id}_agent")},
        name="Vertiv™ Liebert© IntelliSlot™ Unity Card",
        manufacturer="Vertiv",
        model=model,
    )
