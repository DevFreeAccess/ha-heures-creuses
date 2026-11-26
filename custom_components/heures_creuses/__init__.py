"""Intégration Heures Creuses."""
from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import HCCoordinator

_LOGGER = logging.getLogger(__name__)
CARD_VERSION = "1.3.1"
CARD_URL = f"/{DOMAIN}/heures-creuses-card.js"
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SELECT]


async def _register_card(hass: HomeAssistant) -> None:
    """Expose la carte Lovelace fournie avec l'intégration (une seule fois)."""
    flag = f"{DOMAIN}_card_registered"
    if hass.data.get(flag):
        return
    try:
        from homeassistant.components.frontend import add_extra_js_url
        from homeassistant.components.http import StaticPathConfig

        path = Path(__file__).parent / "frontend" / "heures-creuses-card.js"
        await hass.http.async_register_static_paths(
            [StaticPathConfig(CARD_URL, str(path), False)]
        )
        add_extra_js_url(hass, f"{CARD_URL}?v={CARD_VERSION}")
        hass.data[flag] = True
    except Exception as err:  # noqa: BLE001 - ne doit jamais bloquer l'intégration
        _LOGGER.warning("Carte Heures Creuses non enregistrée : %s", err)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await _register_card(hass)
    coordinator = HCCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_reload))
    return True


async def _reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Les options (règles, tarifs, saisons) sont relues à chaque mise à jour."""
    coordinator = hass.data[DOMAIN].get(entry.entry_id)
    if coordinator:
        await coordinator.async_request_refresh()


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()
    return ok
