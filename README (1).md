# AnyCompany Food & Beverage – Data-Driven Marketing Analytics

## Description du projet

Ce projet implémente une plateforme d'analyse marketing data-driven pour AnyCompany Food & Beverage, utilisant Snowflake comme plateforme analytique centrale. L'objectif est d'inverser la tendance à la baisse des ventes et d'atteindre une augmentation de 10 points de part de marché.

## Architecture des données

```
S3 (source) → BRONZE (raw) → SILVER (clean) → ANALYTICS (enrichi)
```

- **BRONZE** : Données brutes chargées depuis S3 (11 tables)
- **SILVER** : Données nettoyées (suppression doublons, valeurs manquantes, formats harmonisés)
- **ANALYTICS** : Tables analytiques enrichies (ventes enrichies, clients enrichis, promotions actives)

## Structure du projet

```
├── sql/
│   ├── Load_data.sql           # Création environnement + chargement BRONZE
│   ├── clean_data.sql          # Nettoyage BRONZE → SILVER
│   ├── sales_trends.sql        # Analyse des tendances de ventes
│   ├── promotion_impact.sql    # Analyse de l'impact des promotions
│   └── campaign_performance.sql # Performance des campagnes marketing
├── streamlit/
│   ├── sales_dashboard.py      # Dashboard des ventes
│   ├── promotion_analysis.py   # Analyse des promotions
│   └── marketing_roi.py        # ROI marketing et KPIs opérationnels
├── README.md
└── business_insights.md        # Synthèse des constats business
```

## Données sources

| Fichier | Format | Volume | Description |
|---------|--------|--------|-------------|
| customer_demographics.csv | CSV | 5 000 | Données démographiques clients |
| customer_service_interactions.csv | CSV | 5 000 | Interactions service client |
| financial_transactions.csv | CSV | 5 000 | Transactions financières |
| promotions-data.csv | CSV | 87 | Promotions |
| marketing_campaigns.csv | CSV | 5 000 | Campagnes marketing |
| product_reviews.csv | TSV | 996 | Avis produits |
| inventory.json | JSON | 5 000 | Niveaux de stock |
| store_locations.json | JSON | 5 000 | Magasins |
| logistics_and_shipping.csv | CSV | 5 000 | Logistique et expéditions |
| supplier_information.csv | CSV | 5 000 | Informations fournisseurs |
| employee_records.csv | CSV | 5 000 | Données employés |

## Exécution

### Phase 1 – Data Preparation
1. Exécuter `sql/Load_data.sql` dans Snowflake
2. Exécuter `sql/clean_data.sql` dans Snowflake

### Phase 2 – Analyses
Exécuter les scripts SQL dans `sql/` pour les analyses exploratoires.

### Dashboards Streamlit
Déployer les applications Streamlit depuis `streamlit/` dans Snowflake Streamlit in Snowflake.

## Base de données Snowflake

- **Database** : `ANYCOMPANY_LAB`
- **Schémas** : `BRONZE`, `SILVER`, `ANALYTICS`
