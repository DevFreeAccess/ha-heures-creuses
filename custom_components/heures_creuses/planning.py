"""Logique de calcul des plages Heures Creuses (sans dépendance HA)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta

_RANGE_RE = re.compile(r"(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})")


def parse_ranges(text: str) -> list[tuple[time, time]]:
    """Convertit '22:00-06:00, 13:00-15:00' en liste de tuples. Lève ValueError."""
    ranges: list[tuple[time, time]] = []
    for part in re.split(r"[,;]", text or ""):
        part = part.strip()
        if not part:
            continue
        m = _RANGE_RE.fullmatch(part)
        if not m:
            raise ValueError(part)
        h1, m1, h2, m2 = (int(x) for x in m.groups())
        if h1 > 23 or h2 > 23 or m1 > 59 or m2 > 59:
            raise ValueError(part)
        ranges.append((time(h1, m1), time(h2, m2)))
    if not ranges:
        raise ValueError("empty")
    return ranges


def _d(value) -> date | None:
    if not value:
        return None
    return value if isinstance(value, date) else date.fromisoformat(value)


@dataclass
class Rule:
    name: str
    hours: str
    weekdays: list[int] = field(default_factory=lambda: list(range(7)))
    start: date | None = None
    end: date | None = None

    @property
    def ranges(self) -> list[tuple[time, time]]:
        return parse_ranges(self.hours)

    def matches(self, d: date) -> bool:
        return (
            (self.start is None or d >= self.start)
            and (self.end is None or d <= self.end)
            and d.weekday() in self.weekdays
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Rule":
        return cls(
            name=data.get("name", "Règle"),
            hours=data["hours"],
            weekdays=[int(x) for x in data.get("weekdays", range(7))],
            start=_d(data.get("start")),
            end=_d(data.get("end")),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "hours": self.hours,
            "weekdays": self.weekdays,
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None,
        }


class Planning:
    """Ensemble de règles. La règle la plus spécifique (date de début la plus
    récente, puis la dernière ajoutée) l'emporte pour un jour donné."""

    def __init__(self, rules: list[Rule], price_hp: float, price_hc: float) -> None:
        self.rules = rules
        self.price_hp = price_hp
        self.price_hc = price_hc

    @classmethod
    def from_options(cls, options: dict) -> "Planning":
        return cls(
            [Rule.from_dict(r) for r in options.get("rules", [])],
            float(options.get("price_hp", 0)),
            float(options.get("price_hc", 0)),
        )

    def select_rule(self, d: date) -> Rule | None:
        cands = [(i, r) for i, r in enumerate(self.rules) if r.matches(d)]
        if not cands:
            return None
        return max(cands, key=lambda c: (c[1].start or date.min, c[0]))[1]

    def is_hc(self, dt: datetime) -> bool:
        t = dt.time()
        rule = self.select_rule(dt.date())
        if rule:
            for s, e in rule.ranges:
                if s < e and s <= t < e:
                    return True
                if s > e and t >= s:  # début de plage qui passe minuit
                    return True
        prev = self.select_rule(dt.date() - timedelta(days=1))
        if prev:
            for s, e in prev.ranges:
                if s > e and t < e:  # fin de plage de la veille
                    return True
        return False

    def price(self, hc: bool) -> float:
        return self.price_hc if hc else self.price_hp

    def next_change(self, now: datetime) -> datetime | None:
        current = self.is_hc(now)
        times = {time(0, 0)}
        for r in self.rules:
            for s, e in r.ranges:
                times.update((s, e))
        cands = sorted(
            c
            for off in range(0, 10)
            for t in times
            if (c := datetime.combine(now.date() + timedelta(days=off), t, tzinfo=now.tzinfo)) > now
        )
        for c in cands:
            if self.is_hc(c) != current:
                return c
        return None
