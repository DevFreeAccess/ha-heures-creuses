"""Sélecteur du mode saison : Auto / Été / Hiver."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity

from .const import CONF_SEASONS, DOMAIN, SEASON_MODES
from .entity import HCEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([SeasonModeSelect(hass.data[DOMAIN][entry.entry_id])])


class SeasonModeSelect(HCEntity, SelectEntity):
    _attr_icon = "mdi:sun-snowflake"
    _attr_options = list(SEASON_MODES.values())

    def __init__(self, c):
        super().__init__(c, "mode_saison", "Mode saison")

    @property
    def current_option(self):
        mode = (self.coordinator.entry.options.get(CONF_SEASONS) or {}).get("mode", "auto")
        return SEASON_MODES.get(mode, "Auto")

    @property
    def available(self):
        return bool(self.coordinator.data.get("seasons_enabled"))

    async def async_select_option(self, option: str) -> None:
        mode = next((k for k, v in SEASON_MODES.items() if v == option), "auto")
        entry = self.coordinator.entry
        seasons = {**(entry.options.get(CONF_SEASONS) or {}), "mode": mode}
        self.hass.config_entries.async_update_entry(
            entry, options={**entry.options, CONF_SEASONS: seasons}
        )
