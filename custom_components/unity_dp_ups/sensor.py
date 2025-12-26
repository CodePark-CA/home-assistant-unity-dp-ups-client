from dataclasses import dataclass
from typing import Callable, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTime,
    UnitOfApparentPower,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

@dataclass
class UnityDPSensorEntityDescription(SensorEntityDescription):
    """Class describing Unity DP UPS sensor entities."""
    value_fn: Callable[[Any], Any] = None

SENSORS: tuple[UnityDPSensorEntityDescription, ...] = (
    UnityDPSensorEntityDescription(
        key="battery_charge",
        name="Battery Charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["battery"]["status"].get("charge"),
    ),
    UnityDPSensorEntityDescription(
        key="battery_time_remaining",
        name="Battery Time Remaining",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["battery"]["status"].get("time_remaining"),
    ),
    UnityDPSensorEntityDescription(
        key="battery_charge_status",
        name="Battery Charge Status",
        value_fn=lambda data: data["battery"]["status"].get("charge_status"),
    ),
    UnityDPSensorEntityDescription(
        key="dc_bus_voltage",
        name="DC Bus Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["battery"]["status"].get("dc_bus_voltage"),
    ),
    UnityDPSensorEntityDescription(
        key="battery_charger_state",
        name="Battery Charger State",
        value_fn=lambda data: data["battery"]["status"].get("charger_state"),
    ),
    UnityDPSensorEntityDescription(
        key="input_voltage",
        name="Input Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["input"]["status"].get("voltage_ln"),
    ),
    UnityDPSensorEntityDescription(
        key="input_current",
        name="Input Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["input"]["status"].get("current_amps"),
    ),
    UnityDPSensorEntityDescription(
        key="input_frequency",
        name="Input Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["input"]["status"].get("frequency_hz"),
    ),
    UnityDPSensorEntityDescription(
        key="input_nominal_voltage",
        name="Input Nominal Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["input"]["status"].get("nominal_voltage"),
    ),
    UnityDPSensorEntityDescription(
        key="output_voltage",
        name="Output Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["output"]["status"].get("voltage_ln"),
    ),
    UnityDPSensorEntityDescription(
        key="output_current",
        name="Output Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["output"]["status"].get("amps"),
    ),
    UnityDPSensorEntityDescription(
        key="output_frequency",
        name="Output Frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["output"]["status"].get("frequency"),
    ),
    UnityDPSensorEntityDescription(
        key="output_power",
        name="Output Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["output"]["status"].get("watts"),
    ),
    UnityDPSensorEntityDescription(
        key="output_power_percent",
        name="Output Power Percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["output"]["status"].get("load_percent"),
    ),
    UnityDPSensorEntityDescription(
        key="output_apparent_power",
        name="Output Apparent Power",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data["output"]["status"].get("va"),
    ),
)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up UPS sensors based on a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    async_add_entities(
        [
            UnityDPSensor(coordinator, entry, description)
            for description in SENSORS
        ]
    )

class UnityDPSensor(CoordinatorEntity, SensorEntity):
    """Representation of an  Unity DP UPS sensor.
    
    This class handles the display and update of individual sensor points from the UPS.
    """

    entity_description: UnityDPSensorEntityDescription

    def __init__(
        self,
        coordinator,
        entry,
        description: UnityDPSensorEntityDescription,
    ):
        """Initialize the sensor with the coordinator and description."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"UPS {description.name}"
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Unity DP UPS",
            manufacturer="Vertiv",
            model="Unity DP",
        )

    @property
    def native_value(self):
        """Return the state of the sensor by extracting it from the coordinator data."""
        try:
            value = self.entity_description.value_fn(self.coordinator.data)
            if value is None or value == '--':
                return None
            
            # If we have a unit or device class, we expect a numeric value
            if self.entity_description.native_unit_of_measurement or self.entity_description.device_class:
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None
            
            return value
        except (KeyError, TypeError):
            return None
