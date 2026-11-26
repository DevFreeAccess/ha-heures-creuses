"""Capteurs."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import EntityCategory, UnitOfTime

from .const import DOMAIN
from .entity import HCEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            PeriodSensor(c),
            MessageSensor(c),
            PriceSensor(c),
            NextChangeSensor(c),
            RemainingSensor(c),
            SeasonSensor(c),
            FixedPriceSensor(c, "prix_hp", "Prix Heure Pleine", "price_hp", "mdi:flash"),
            FixedPriceSensor(c, "prix_hc", "Prix Heure Creuse", "price_hc", "mdi:weather-night"),
        ]
    )


class PeriodSensor(HCEntity, SensorEntity):
    """État : Heure Creuse / Heure Pleine (comme la couleur Tempo)."""

    def __init__(self, c):
        super().__init__(c, "periode", "Période")

    @property
    def native_value(self):
        return self.coordinator.data["label"]

    @property
    def icon(self):
        return "mdi:weather-night" if self.coordinator.data["is_hc"] else "mdi:flash"

    @property
    def extra_state_attributes(self):
        d = self.coordinator.data
        return {
            "prix": d["price"],
            "unite": "€/kWh",
            "couleur": "bleu" if d["is_hc"] else "rouge",
            "message": d["message"],
            "prochaine_periode": d["next_label"],
            "prochain_prix": d["next_price"],
            "prochain_changement": d["next_change"].isoformat() if d["next_change"] else None,
            "heure_prochain_changement": d["next_change"].strftime("%H:%M") if d["next_change"] else None,
            "temps_restant_min": d["remaining"],
            "saison": d["season"],
            "prix_heure_pleine": d["price_hp"],
            "prix_heure_creuse": d["price_hc"],
            "regles": d["rules"],
        }


class MessageSensor(HCEntity, SensorEntity):
    """Texte prêt à afficher : « Vous êtes en Heure Creuse (0,1696 €/kWh) »."""

    _attr_icon = "mdi:message-text-clock"

    def __init__(self, c):
        super().__init__(c, "message", "Message")

    @property
    def native_value(self):
        return self.coordinator.data["message"]


class PriceSensor(HCEntity, SensorEntity):
    _attr_native_unit_of_measurement = "€/kWh"
    _attr_icon = "mdi:currency-eur"
    _attr_suggested_display_precision = 4

    def __init__(self, c):
        super().__init__(c, "prix", "Prix actuel")

    @property
    def native_value(self):
        return self.coordinator.data["price"]


class NextChangeSensor(HCEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:clock-start"

    def __init__(self, c):
        super().__init__(c, "prochain_changement", "Prochain changement")

    @property
    def native_value(self):
        return self.coordinator.data["next_change"]


class RemainingSensor(HCEntity, SensorEntity):
    """Minutes restantes avant la prochaine bascule."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:timer-sand"

    def __init__(self, c):
        super().__init__(c, "temps_restant", "Temps restant")

    @property
    def native_value(self):
        return self.coordinator.data["remaining"]


class FixedPriceSensor(HCEntity, SensorEntity):
    """Tarif HP ou HC configuré (diagnostic)."""

    _attr_native_unit_of_measurement = "€/kWh"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_suggested_display_precision = 4

    def __init__(self, c, key, name, data_key, icon):
        super().__init__(c, key, name)
        self._data_key = data_key
        self._attr_icon = icon

    @property
    def native_value(self):
        return self.coordinator.data[self._data_key]


class SeasonSensor(HCEntity, SensorEntity):
    """Saison en cours : Été / Hiver (ou Désactivée)."""

    def __init__(self, c):
        super().__init__(c, "saison", "Saison")

    @property
    def native_value(self):
        return self.coordinator.data["season"]

    @property
    def icon(self):
        return {
            "Été": "mdi:white-balance-sunny",
            "Hiver": "mdi:snowflake",
        }.get(self.coordinator.data["season"], "mdi:calendar-blank")
