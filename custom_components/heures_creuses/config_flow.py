"""Configuration par l'interface (création + gestion des règles)."""
from __future__ import annotations

from datetime import date

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_DELETE,
    CONF_END,
    CONF_HOURS,
    CONF_NAME,
    CONF_PRICE_HC,
    CONF_PRICE_HP,
    CONF_RULE_NAME,
    CONF_RULES,
    CONF_START,
    CONF_WEEKDAYS,
    DEFAULT_HOURS,
    DEFAULT_PRICE_HC,
    DEFAULT_PRICE_HP,
    DOMAIN,
)
from .planning import Rule, parse_ranges

WEEKDAYS = [
    selector.SelectOptionDict(value=str(i), label=n)
    for i, n in enumerate(
        ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    )
]
ALL_DAYS = [str(i) for i in range(7)]
PRICE = selector.NumberSelector(
    selector.NumberSelectorConfig(
        min=0, max=5, step="any", mode=selector.NumberSelectorMode.BOX,
        unit_of_measurement="€/kWh",
    )
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlow()

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                parse_ranges(user_input[CONF_HOURS])
            except ValueError:
                errors[CONF_HOURS] = "invalid_hours"
            else:
                rule = Rule("Par défaut", user_input[CONF_HOURS]).to_dict()
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={},
                    options={
                        CONF_PRICE_HP: user_input[CONF_PRICE_HP],
                        CONF_PRICE_HC: user_input[CONF_PRICE_HC],
                        CONF_RULES: [rule],
                    },
                )
        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Heures Creuses"): str,
                vol.Required(CONF_PRICE_HP, default=DEFAULT_PRICE_HP): PRICE,
                vol.Required(CONF_PRICE_HC, default=DEFAULT_PRICE_HC): PRICE,
                vol.Required(CONF_HOURS, default=DEFAULT_HOURS): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


class OptionsFlow(config_entries.OptionsFlow):
    def _save(self, **changes):
        return self.async_create_entry(data={**self.config_entry.options, **changes})

    async def async_step_init(self, user_input=None):
        return self.async_show_menu(
            step_id="init", menu_options=["tarifs", "add_rule", "delete_rule"]
        )

    async def async_step_tarifs(self, user_input=None):
        if user_input is not None:
            return self._save(**user_input)
        o = self.config_entry.options
        schema = vol.Schema(
            {
                vol.Required(CONF_PRICE_HP, default=o.get(CONF_PRICE_HP)): PRICE,
                vol.Required(CONF_PRICE_HC, default=o.get(CONF_PRICE_HC)): PRICE,
            }
        )
        return self.async_show_form(step_id="tarifs", data_schema=schema)

    async def async_step_add_rule(self, user_input=None):
        errors = {}
        if user_input is not None:
            start = user_input.get(CONF_START)
            end = user_input.get(CONF_END)
            try:
                parse_ranges(user_input[CONF_HOURS])
            except ValueError:
                errors[CONF_HOURS] = "invalid_hours"
            if start and end and date.fromisoformat(end) < date.fromisoformat(start):
                errors[CONF_END] = "invalid_dates"
            if not user_input[CONF_WEEKDAYS]:
                errors[CONF_WEEKDAYS] = "no_weekdays"
            if not errors:
                rule = Rule(
                    user_input[CONF_RULE_NAME],
                    user_input[CONF_HOURS],
                    sorted(int(x) for x in user_input[CONF_WEEKDAYS]),
                    date.fromisoformat(start) if start else None,
                    date.fromisoformat(end) if end else None,
                ).to_dict()
                rules = list(self.config_entry.options.get(CONF_RULES, [])) + [rule]
                return self._save(**{CONF_RULES: rules})
        schema = vol.Schema(
            {
                vol.Required(CONF_RULE_NAME, default="Nouvelle règle"): str,
                vol.Optional(CONF_START): selector.DateSelector(),
                vol.Optional(CONF_END): selector.DateSelector(),
                vol.Required(CONF_WEEKDAYS, default=ALL_DAYS): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=WEEKDAYS, multiple=True,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(CONF_HOURS, default=DEFAULT_HOURS): str,
            }
        )
        return self.async_show_form(
            step_id="add_rule", data_schema=schema, errors=errors
        )

    async def async_step_delete_rule(self, user_input=None):
        rules = list(self.config_entry.options.get(CONF_RULES, []))
        if user_input is not None:
            drop = {int(i) for i in user_input[CONF_DELETE]}
            return self._save(
                **{CONF_RULES: [r for i, r in enumerate(rules) if i not in drop]}
            )
        opts = []
        for i, r in enumerate(rules):
            period = f"{r.get('start') or '…'} → {r.get('end') or '…'}"
            opts.append(
                selector.SelectOptionDict(
                    value=str(i), label=f"{r['name']} | {period} | {r['hours']}"
                )
            )
        schema = vol.Schema(
            {
                vol.Required(CONF_DELETE, default=[]): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=opts, multiple=True)
                )
            }
        )
        return self.async_show_form(step_id="delete_rule", data_schema=schema)
