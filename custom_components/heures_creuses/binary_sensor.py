"""Capteur binaire : ON = Heure Creuse."""
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN
from .entity import HCEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([HeureCreuse(hass.data[DOMAIN][entry.entry_id])])


class HeureCreuse(HCEntity, BinarySensorEntity):
    _attr_icon = "mdi:cash-clock"

    def __init__(self, c):
        super().__init__(c, "heure_creuse", "Heure creuse")

    @property
    def is_on(self):
        return self.coordinator.data["is_hc"]
