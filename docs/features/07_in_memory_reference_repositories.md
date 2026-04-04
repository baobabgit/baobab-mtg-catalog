# Feature 07 — In-memory reference repositories

## Branche

`feature/07-in-memory-reference-repositories`

## Objectif

Créer les repositories in-memory du référentiel catalogue.

## Périmètre

- interfaces de repositories
- implémentations in-memory
- contraintes d'unicité
- recherche par identifiants métier et externes
- recherche par nom normalisé
- recherche par set et collector number
- exceptions not found

## Livrables attendus

- interfaces repository
- implémentations in-memory
- exceptions associées
- tests unitaires complets

## Critères d'acceptation

- stockage déterministe et cohérent
- support de l'idempotence côté référentiel
- API claire de lecture et de consolidation

## Prompt pour l'IA de développement

```text
Tu développes la feature `07_in_memory_reference_repositories` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/07-in-memory-reference-repositories`

Objectif :
Créer les repositories permettant de stocker, retrouver et consolider cartes, printings et sets en mémoire.

Travaux à réaliser :
1. Définir les interfaces repository pour :
   - CardDefinition
   - CardPrinting
   - Set
2. Créer les implémentations in-memory correspondantes.
3. Ajouter les opérations utiles minimales :
   - add / save / upsert selon la stratégie retenue
   - get_by_business_id
   - get_by_external_id si pertinent
   - get_by_name_normalized si pertinent
   - list_all
   - find_by_set
   - find_by_collector_number
   - find_printings_by_definition
4. Gérer les cas not found avec exceptions spécifiques.
5. Implémenter les garde-fous nécessaires pour éviter les doublons incohérents.
6. Écrire les tests unitaires complets.

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

