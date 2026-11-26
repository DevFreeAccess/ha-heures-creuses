"""Constantes Heures Creuses."""
DOMAIN = "heures_creuses"

CONF_NAME = "name"
CONF_PRICE_HP = "price_hp"
CONF_PRICE_HC = "price_hc"
CONF_HOURS = "hours"
CONF_RULES = "rules"
CONF_RULE_NAME = "rule_name"
CONF_START = "start_date"
CONF_END = "end_date"
CONF_WEEKDAYS = "weekdays"
CONF_DELETE = "rules_to_delete"

DEFAULT_PRICE_HP = 0.2146
DEFAULT_PRICE_HC = 0.1696
DEFAULT_HOURS = "22:00-06:00"

LABEL_HC = "Heure Creuse"
LABEL_HP = "Heure Pleine"

CONF_SEASONS = "seasons"
CONF_SEASONS_ENABLED = "seasons_enabled"
CONF_WINTER_START = "winter_start"
CONF_SUMMER_START = "summer_start"
CONF_HOURS_WINTER = "hours_winter"
CONF_HOURS_SUMMER = "hours_summer"
CONF_PRICE_HP_WINTER = "price_hp_winter"
CONF_PRICE_HC_WINTER = "price_hc_winter"
CONF_PRICE_HP_SUMMER = "price_hp_summer"
CONF_PRICE_HC_SUMMER = "price_hc_summer"

SEASON_MODES = {"auto": "Auto", "ete": "Été", "hiver": "Hiver"}
SEASON_LABELS = {"ete": "Été", "hiver": "Hiver"}
