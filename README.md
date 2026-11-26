<p align="center">
  <img src="https://raw.githubusercontent.com/VOTRE-COMPTE/ha-heures-creuses/main/images/banner.png" alt="Heures Creuses pour Home Assistant" width="100%">
</p>

<p align="center">
  <a href="https://hacs.xyz"><img alt="HACS" src="https://img.shields.io/badge/HACS-Custom-orange.svg"></a>
  <a href="https://github.com/VOTRE-COMPTE/ha-heures-creuses/releases"><img alt="Version" src="https://img.shields.io/github/v/release/VOTRE-COMPTE/ha-heures-creuses"></a>
  <a href="https://github.com/VOTRE-COMPTE/ha-heures-creuses/actions/workflows/validate.yml"><img alt="Validation" src="https://github.com/VOTRE-COMPTE/ha-heures-creuses/actions/workflows/validate.yml/badge.svg"></a>
  <img alt="Licence" src="https://img.shields.io/badge/licence-MIT-blue.svg">
</p>

# ⚡ Heures Creuses

Sachez à tout moment si vous êtes en **Heure Creuse** ou en **Heure Pleine**, avec le prix du kWh en cours — façon Tempo.

> **Vous êtes en Heure Creuse (0,1696 €/kWh)** – Heure Pleine à partir de 06:00

![Aperçu](https://raw.githubusercontent.com/VOTRE-COMPTE/ha-heures-creuses/main/images/preview.png)

## ✨ Fonctionnalités

- 🕐 **Plages horaires libres** : plusieurs plages par jour (`22:00-06:00, 13:00-15:00`), passage de minuit géré.
- 📅 **Règles par période** : dates de début/fin (année, saison, nouveau contrat) et jours de la semaine.
- ☀️❄️ **Modes été / hiver** : plages et tarifs différents selon la saison, changement automatique chaque année (ou forcé en un clic).
- 💶 **Tarifs HP / HC** modifiables à tout moment, sans redémarrage.
- 🔔 **Bascule exacte** : les automatisations se déclenchent à l'heure pile du changement.
- 🧩 **100 % interface** : aucune ligne de YAML pour configurer.
- ⚡ **Compatible tableau de bord Énergie** (entité de prix en €/kWh).

## ⚙️ Configuration

Paramètres → Appareils et services → **Ajouter une intégration** → *Heures Creuses*, puis saisissez le nom, les prix HP/HC et vos plages creuses par défaut.

Le bouton **Configurer** permet ensuite de **modifier les tarifs**, **ajouter une règle** ou **supprimer des règles**.

| Règle | Dates | Jours | Plages |
|---|---|---|---|
| Toute l'année | – | tous | `22:00-06:00` |
| Hiver 2026-2027 | 01/11/2026 → 31/03/2027 | tous | `22:00-06:00, 13:00-15:00` |
| Week-end | – | Sam, Dim | `00:00-23:59` |

**Priorité :** la règle dont la date de début est la plus récente l'emporte ; à égalité, la dernière ajoutée. Une règle « toute l'année » peut donc être surchargée pour une saison précise.

## ☀️❄️ Modes été / hiver

Votre contrat change selon la saison ? Dans **Configurer → Modes été / hiver (saisons)** :

| Champ | Exemple |
|---|---|
| Début de l'hiver | 1er novembre |
| Plages creuses hiver | `22:00-06:00, 13:00-15:00` |
| Prix HP / HC hiver | `0,2700` / `0,1900` |
| Début de l'été | 1er avril |
| Plages creuses été | `23:00-07:00` |
| Prix HP / HC été | `0,2300` / `0,1600` |

- Seuls le **jour et le mois** comptent : la bascule se répète **chaque année** toute seule.
- Le sélecteur `select.heures_creuses_mode_saison` permet de passer en **Auto**, **Été** ou **Hiver** manuellement (utile si votre fournisseur décale la date).
- Les règles avec dates ou jours précis (ex. week-end) restent **prioritaires** sur la saison.
- Les règles « toute l'année » sans jour précis sont remplacées par les saisons tant qu'elles sont activées.

## 📊 Entités

| Entité | Contenu |
|---|---|
| `sensor.heures_creuses_periode` | `Heure Creuse` / `Heure Pleine` + attributs (prix, couleur, prochain changement…) |
| `sensor.heures_creuses_message` | Texte prêt à afficher |
| `sensor.heures_creuses_prix_actuel` | Prix en cours (€/kWh) |
| `sensor.heures_creuses_prochain_changement` | Horodatage de la prochaine bascule |
| `sensor.heures_creuses_temps_restant` | Minutes avant la prochaine bascule |
| `sensor.heures_creuses_saison` | `Été`, `Hiver` ou `Désactivée` |
| `select.heures_creuses_mode_saison` | Auto / Été / Hiver |
| `binary_sensor.heures_creuses_heure_creuse` | `on` pendant les heures creuses |
| `sensor.heures_creuses_prix_heure_pleine` / `_prix_heure_creuse` | Tarifs configurés (diagnostic) |

> Les identifiants dépendent du nom choisi à la création de l'intégration.

## 🖼️ Tableau de bord

Des cartes prêtes à copier se trouvent dans le dossier [`dashboards/`](dashboards). Elles s'adaptent à la largeur de l'écran, du téléphone à la tablette murale.

| Fichier | Usage |
|---|---|
| [`carte_couleur.yaml`](dashboards/carte_couleur.yaml) | Carte bleue / rouge complète : période, prix, prochain changement, saison |
| [`carte_native.yaml`](dashboards/carte_native.yaml) | Sans HTML, la plus compatible |
| [`carte_compacte.yaml`](dashboards/carte_compacte.yaml) | Une ligne, pour petit écran ou bandeau |
| [`carte_ecran_mural.yaml`](dashboards/carte_ecran_mural.yaml) | Très grand affichage |
| [`selecteur_saison.yaml`](dashboards/selecteur_saison.yaml) | Changer de mode en un clic |

**Utiliser une carte :** ouvrez votre tableau de bord → ⋮ → *Modifier* → **+ Ajouter une carte** → tout en bas **Manuel** → collez le contenu du fichier → **Enregistrer**.

> Si vous avez donné un autre nom que « Heures Creuses » à l'intégration, remplacez `heures_creuses` dans les identifiants (Paramètres → Entités, recherche « heures »).

## 🤖 Automatisation (exemple)

Lancer le chauffe-eau dès le début des heures creuses :

```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.heures_creuses_heure_creuse
    to: "on"
actions:
  - action: switch.turn_on
    target:
      entity_id: switch.chauffe_eau
```

## 🔌 Tableau de bord Énergie

Dans Paramètres → Tableaux de bord → Énergie, pour votre consommation réseau, choisissez **Utiliser une entité avec le prix actuel** et sélectionnez `sensor.heures_creuses_prix_actuel` : vos coûts HP/HC sont alors calculés automatiquement.

<details>
<summary>📦 Installation (hors HACS)</summary>

Copiez le dossier `custom_components/heures_creuses` dans `/config/custom_components/`, puis redémarrez Home Assistant.

Via HACS : menu ⋮ → *Dépôts personnalisés* → URL `https://github.com/VOTRE-COMPTE/ha-heures-creuses` → catégorie *Intégration*.

</details>

## 🐞 Problème ou idée ?

Ouvrez une [issue](https://github.com/VOTRE-COMPTE/ha-heures-creuses/issues) en précisant votre version de Home Assistant et les lignes du journal contenant `heures_creuses`.

## Licence

MIT
