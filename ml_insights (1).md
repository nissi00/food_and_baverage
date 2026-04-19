# ML Insights – AnyCompany Food & Beverage

## Vue d'ensemble des modeles

| Modele | Algorithme | Objectif | Donnees |
|--------|-----------|----------|---------|
| Segmentation clients | KMeans (K=4) | Identifier des groupes clients homogenes | ANALYTICS.CLIENTS_ENRICHIS (5 000 clients) |
| Propension a l'achat | RandomForest Classifier | Predire si une transaction sera un achat | ANALYTICS.VENTES_ENRICHIES (8 227 transactions) |
| Reponse aux promotions | GradientBoosting Regressor | Predire le montant de vente et l'impact promo | ANALYTICS.VENTES_ENRICHIES (ventes uniquement) |

---

## Modele 1 : Segmentation Clients

### Methodologie
- **Features** : Revenu annuel, age, nombre d'interactions service client, satisfaction, taux de resolution, genre, statut marital, region
- **Preprocessing** : LabelEncoding des variables categoriques, StandardScaler
- **Selection de K** : Methode du coude + score silhouette

### Resultats attendus
- 4 clusters identifies avec des profils distincts
- Chaque cluster represente un segment marketing actionnable

### Interpretation business
- Les segments permettent de cibler les campagnes selon le profil client
- Les clients a haut revenu et forte satisfaction sont les cibles prioritaires pour le cross-selling
- Les clients insatisfaits necessitent des actions de retention

---

## Modele 2 : Propension a l'Achat

### Methodologie
- **Features** : Montant, moyen de paiement, region, temporalite (annee, trimestre, mois, jour), presence promo, budget campagne, reach, taux de conversion
- **Cible** : IS_SALE (binaire : Sale=1, autre=0)
- **Split** : 80% train / 20% test (stratifie)

### Metriques attendues
- **AUC ROC** : Mesure la capacite du modele a discriminer acheteurs vs non-acheteurs
- **Matrice de confusion** : Precision des predictions

### Interpretation business
- Le montant de la transaction et le moyen de paiement sont les premiers predicteurs
- La presence de promotions influence positivement la propension a l'achat
- Permet de scorer les prospects et prioriser les actions commerciales

---

## Modele 3 : Reponse aux Promotions

### Methodologie
- **Features** : Variables temporelles, region, moyen de paiement, presence promo, taux de remise, type de promo, budget et reach campagne
- **Cible** : AMOUNT (montant de la vente)
- **Simulation** : Comparaison predictions avec/sans promo pour mesurer le lift

### Metriques attendues
- **MAE** : Erreur absolue moyenne en dollars
- **RMSE** : Erreur quadratique moyenne
- **R2** : Coefficient de determination

### Interpretation business
- Le lift promotionnel mesure l'impact incremental des promotions sur les ventes
- Certaines periodes et regions sont plus sensibles aux promotions
- Le taux de remise optimal peut etre identifie via simulation

---

## Recommandations marketing globales

### Court terme
1. **Segmentation** : Adapter les messages marketing par cluster client
2. **Scoring** : Utiliser le modele de propension pour cibler les clients a forte probabilite d'achat
3. **Promotions** : Ajuster les taux de remise selon la sensibilite par region/categorie

### Moyen terme
1. **Personnalisation** : Combiner segmentation + propension pour des offres sur mesure
2. **Optimisation budgetaire** : Allouer le budget marketing aux canaux et segments a plus fort ROI
3. **Prevention churn** : Identifier les clients du segment "insatisfait" et lancer des actions de retention

### Long terme
1. **Automatisation** : Integrer les modeles dans le pipeline marketing pour un scoring en temps reel
2. **A/B Testing** : Valider les recommandations par experimentation controlee
3. **Enrichissement** : Ajouter des donnees comportementales (parcours web, app) pour ameliorer les modeles
