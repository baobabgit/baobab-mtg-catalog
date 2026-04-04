# Feature 02 — Shared domain value objects

## Branche

`feature/02-shared-domain-value-objects`

## Objectif

Créer les objets de valeur partagés du domaine catalogue MTG.

## Périmètre

- `ManaCost`
- `Color`
- `ColorIdentity`
- `Language`
- `Rarity`
- `Finish`
- `CollectorNumber`
- `TypeLine`
- types d'identifiants externes utiles
- éventuellement légalité de format si retenue

## Livrables attendus

- objets de valeur et enums partagés
- validations dédiées
- exceptions spécifiques si nécessaire
- tests unitaires complets

## Critères d'acceptation

- types réutilisables et découplés de Scryfall
- validations fiables
- API lisible
- cas limites couverts

## Prompt pour l'IA de développement

```text
Tu développes la feature `02_shared_domain_value_objects` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/02-shared-domain-value-objects`

Pré-requis :
La feature `01_project_bootstrap` est mergée sur `main`.

Objectif :
Créer les objets de valeur et types partagés du domaine catalogue MTG.

Travaux à réaliser :
1. Créer les objets de valeur/enums partagés nécessaires, notamment :
   - ManaCost
   - Color
   - ColorIdentity
   - Language
   - Rarity
   - Finish
   - CollectorNumber
   - TypeLine
   - types d'identifiants externes utiles
2. Ajouter si pertinent la modélisation de la légalité de format.
3. Définir une API stable et lisible.
4. Ajouter des validations métier.
5. Lever des exceptions métier dédiées en cas de valeur invalide.
6. Écrire les tests unitaires correspondants.

Points d'attention :
- ne pas surcoupler ces objets à Scryfall
- préparer leur réutilisation par `CardDefinition`, `CardPrinting` et `Set`
- garder une représentation métier stable

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

