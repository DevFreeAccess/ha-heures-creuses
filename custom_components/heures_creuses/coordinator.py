"""Coordinateur : met à jour l'état chaque minute et à chaque bascule exacte."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import DOMAIN, LABEL_HC, LABEL_HP
from .planning import Planning

_LOGGER = logging.getLogger(__name__)


def _fmt(price: float) -> str:
    return f"{price:.4f}".replace(".", ",")


class HCCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(minutes=1)
        )
        self.entry = entry
        self._unsub = None

    async def _async_update_data(self) -> dict:
        now = dt_util.now()
        planning = Planning.from_options(self.entry.options)
        hc = planning.is_hc(now)
        price = planning.price(hc)
        label = LABEL_HC if hc else LABEL_HP
        nxt = planning.next_change(now)
        next_label = next_price = None
        if nxt:
            next_label = LABEL_HP if hc else LABEL_HC
            next_price = planning.price(not hc)

        message = f"Vous êtes en {label} ({_fmt(price)} €/kWh)"
        if nxt:
            message += (
                f" - {next_label} à partir de {nxt:%H:%M}"
                if nxt.date() == now.date()
                else f" - {next_label} à partir de {nxt:%d/%m %H:%M}"
            )

        if self._unsub:
            self._unsub()
            self._unsub = None
        if nxt:
            self._unsub = async_track_point_in_time(self.hass, self._on_change, nxt)

        return {
            "is_hc": hc,
            "label": label,
            "price": price,
            "message": message,
            "next_change": nxt,
            "next_label": next_label,
            "next_price": next_price,
            "price_hp": planning.price_hp,
            "price_hc": planning.price_hc,
            "rules": [r.to_dict() for r in planning.rules],
        }

    @callback
    def _on_change(self, _now) -> None:
        self._unsub = None
        self.hass.async_create_task(self.async_request_refresh())

    async def async_shutdown(self) -> None:
        if self._unsub:
            self._unsub()
            self._unsub = None
        await super().async_shutdown()
