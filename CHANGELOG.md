# Changelog

## 1.3.1
- Carte : options `fill` et `height` pour occuper tout l'écran (vue panneau).
- Dashboard `echo_show_streamed.yaml` (plein écran).

## 1.3.0
- Nouvelle carte Lovelace intégrée `heures-creuses-card` (colorée, adaptative, options compact/taille/couleurs), enregistrée automatiquement.
- Les cartes Markdown colorées (HTML) sont supprimées : Home Assistant en retire le style.

## 1.2.0
- **Modes été / hiver** : plages et tarifs distincts par saison, bascule annuelle automatique.
- Nouveau sélecteur `Mode saison` (Auto / Été / Hiver) et capteur `Saison`.
- Les options (règles, tarifs, saisons) s'appliquent sans rechargement de l'intégration.
- Cartes de tableau de bord adaptatives (téléphone, tablette, écran mural) dans `dashboards/`.

## 1.1.0
- Icône et logo affichés dans Home Assistant (dossier `brand/`, HA 2026.3 ou plus récent).
- Nouveaux capteurs : temps restant avant la bascule, tarifs HP/HC (diagnostic).
- Nouveaux attributs : `heure_prochain_changement`, `temps_restant_min`.
- Appareil de type « service », icônes plus parlantes.
- README restructuré (bannière, aperçu, cartes de tableau de bord, tableau Énergie).

## 1.0.1
- Correction du chargement du flux de configuration (pas du sélecteur numérique).

## 1.0.0
- Première version.
