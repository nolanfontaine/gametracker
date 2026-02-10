# GameTracker ETL Project

Projet d'automatisation et de pipeline de données (ETL) pour l'analyse de performances de joueurs de jeux vidéo.
Ce projet nettoie des données brutes (CSV), les charge dans une base MySQL, et génère un rapport statistique, le tout orchestré via Docker.

## Prérequis

* **Docker** et **Docker Compose** installés.
* Fichiers de données présents dans `data/raw/` (`Players.csv` et `Scores.csv`).

## Démarrage Rapide (100% Automatisé)

Le projet est conçu pour être **totalement autonome**. Une seule commande suffit pour monter l'infrastructure, nettoyer les données et générer le rapport.

1.  **Lancer le projet :**
    ```bash
    docker compose up -d --build
    ```

    *Le conteneur Python va automatiquement :*
    * Attendre que la base de données MySQL soit prête.
    * Initialiser les tables.
    * Lancer le pipeline ETL (Extraction, Transformation, Chargement).
    * Générer le rapport final.

2.  **Vérifier le résultat :**
    Attendez environ **15 à 20 secondes**, puis ouvrez le fichier généré :
     `output/rapport.txt`

    *Optionnel : Pour suivre l'avancement en temps réel dans le terminal :*
    ```bash
    docker compose logs -f app
    ```

## Structure du Projet

```text
gametracker/
├── data/raw/          # Données sources (CSV)
├── output/            # Rapports générés (automatique)
├── scripts/           # Scripts d'automatisation (Bash, SQL)
├── src/               # Code source Python (ETL)
├── docker-compose.yml # Orchestration et Automatisation
└── Dockerfile         # Configuration de l'image Python
```

## Qualité des Données

Le pipeline (src/transform.py) traite automatiquement les 7 problèmes suivants :

1. Doublons : Suppression des lignes dupliquées (Joueurs et Scores).

2. Emails invalides : Les emails sans '@' sont nettoyés (mis à NULL).

3. Dates incohérentes : Conversion standardisée, les erreurs deviennent NULL.

4. Espaces parasites : Nettoyage des pseudos (trimming).

5. Scores aberrants : Suppression des scores négatifs ou nuls.

6. Valeurs manquantes : Gestion des NaN pour compatibilité SQL.

7. Intégrité Référentielle : Suppression des scores orphelins (joueurs inexistants).

## Auteur

Projet réalisé par **Nolan FONTAINE** dans le cadre du module Automatisation et Tests (BUT SD).
