"""Entité de base."""
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HCCoordinator


class HCEntity(CoordinatorEntity[HCCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: HCCoordinator, key: str, name: str) -> None:
        super().__init__(coordinator)
        entry = coordinator.entry
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_name = name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            entry_type=DeviceEntryType.SERVICE,
            manufacturer="Personnalisé",
            model="Heures Creuses / Heures Pleines",
        )
