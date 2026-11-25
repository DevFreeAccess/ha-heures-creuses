# ⚡ Heures Creuses pour Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![Validate](https://github.com/DevFreeAccess/ha-heures-creuses/actions/workflows/validate.yml/badge.svg)](https://github.com/DevFreeAccess/ha-heures-creuses/actions/workflows/validate.yml)

Définissez vos plages d'**heures creuses** (par période, année, jours de la semaine) et affichez, façon Tempo :

> **Vous êtes en Heure Creuse (0,1696 €/kWh)** – Heure Pleine à partir de 06:00

## Installation via HACS

[![Ouvrir dans HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=DevFreeAccess&repository=ha-heures-creuses&category=integration)

Ou manuellement dans HACS :
1. HACS → menu ⋮ → **Dépôts personnalisés**.
2. URL : `https://github.com/DevFreeAccess/ha-heures-creuses` — Catégorie : **Intégration**.
3. Téléchargez **Heures Creuses**, puis **redémarrez** Home Assistant.
4. Paramètres → Appareils et services → **Ajouter une intégration** → *Heures Creuses*.

### Installation manuelle
Copiez `custom_components/heures_creuses` dans `/config/custom_components/` et redémarrez.

## Configuration
À la création : nom, prix HP, prix HC (€/kWh) et plages creuses par défaut (ex. `22:00-06:00, 13:00-15:00`).

Bouton **Configurer** :
- **Modifier les tarifs**
- **Ajouter une règle** : nom, dates de début/fin (optionnelles), jours, plages `HH:MM-HH:MM`
- **Supprimer des règles**

Priorité : la règle dont la date de début est la plus récente l'emporte ; à égalité, la dernière ajoutée.
Le passage de minuit est géré (`22:00-06:00`).

| Exemple | Dates | Jours | Plages |
|---|---|---|---|
| Toute l'année | – | tous | `22:00-06:00` |
| Hiver 2026-2027 | 01/11/2026 → 31/03/2027 | tous | `22:00-06:00, 13:00-15:00` |
| Week-end tout en creux | – | Sam, Dim | `00:00-23:59` |

## Entités
| Entité | Contenu |
|---|---|
| `sensor.heures_creuses_periode` | `Heure Creuse` / `Heure Pleine` + attributs (prix, couleur, prochain changement, règles) |
| `sensor.heures_creuses_message` | Texte prêt à afficher |
| `sensor.heures_creuses_prix_actuel` | Prix actuel en €/kWh |
| `sensor.heures_creuses_prochain_changement` | Horodatage de la prochaine bascule |
| `binary_sensor.heures_creuses_heure_creuse` | ON = Heure Creuse |

Les identifiants dépendent du nom choisi à la création.

## Carte Lovelace
```yaml
type: markdown
content: >
  <ha-alert alert-type="{{ 'info' if is_state('binary_sensor.heures_creuses_heure_creuse','on') else 'warning' }}">
  {{ states('sensor.heures_creuses_message') }}
  </ha-alert>
```

```yaml
type: tile
entity: sensor.heures_creuses_periode
name: Tarif actuel
state_content: [state, prix]
vertical: true
```

## Automatisation (exemple)
```yaml
trigger:
  - platform: state
    entity_id: binary_sensor.heures_creuses_heure_creuse
    to: "on"
action:
  - service: switch.turn_on
    target:
      entity_id: switch.chauffe_eau
```

## Licence
MIT
