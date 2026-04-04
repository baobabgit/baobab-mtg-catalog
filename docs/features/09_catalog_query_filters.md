# Feature 09 — Catalog query filters

## Branche

`feature/09-catalog-query-filters`

## Objectif

Créer la couche de consultation riche du référentiel catalogue.

## Périmètre

- recherche par nom
- recherche par identifiant métier
- recherche par identifiant externe
- filtrage par set
- filtrage par collector number
- filtrage par couleur
- filtrage par identité couleur
- filtrage par rareté
- filtrage par type
- filtrage par légalité si retenue

## Livrables attendus

- services de recherche / filtrage
- critères de requête métier
- tests unitaires et d'intégration internes

## Critères d'acceptation

- le référentiel est réellement interrogeable selon les cas d'usage métier
- les filtres sont composables si pertinent
- l'API de recherche est claire et testée

## Prompt pour l'IA de développement

```text
Tu développes la feature `09_catalog_query_filters` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/09-catalog-query-filters`

Objectif :
Créer les services de recherche et filtrage métier du référentiel catalogue.

Travaux à réaliser :
1. Créer les services de recherche / filtrage nécessaires.
2. Couvrir au minimum les cas d'usage suivants :
   - recherche par nom
   - recherche par identifiant métier
   - recherche par identifiant externe
   - filtrage par set
   - filtrage par collector number
   - filtrage par couleur
   - filtrage par identité couleur
   - filtrage par rareté
   - filtrage par type
   - filtrage par légalité si cette donnée est conservée
3. Concevoir une API claire de critères de recherche.
4. Ajouter les tests unitaires et d'intégration internes.

Points d'attention :
- viser une vraie couche de consultation de référentiel, pas seulement quelques getters
- garder une API stable et compréhensible pour les autres briques Baobab

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

