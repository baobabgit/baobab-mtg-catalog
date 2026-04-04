# Feature 06 — Scryfall normalization adapters

## Branche

`feature/06-scryfall-normalization-adapters`

## Objectif

Créer la couche de normalisation et d'adaptation entre les payloads Scryfall et le modèle métier local.

## Périmètre

- validation de payloads
- normalisation de structures Scryfall
- adapters vers `CardDefinition`, `CardPrinting` et `Set`
- gestion des champs absents et cas spéciaux
- exceptions de mapping

## Livrables attendus

- adapters Scryfall
- logique de validation
- exceptions spécifiques
- tests unitaires riches

## Critères d'acceptation

- les adapters encapsulent toute la logique liée à Scryfall
- le domaine reste propre et indépendant
- les cas limites principaux sont couverts

## Prompt pour l'IA de développement

```text
Tu développes la feature `06_scryfall_normalization_adapters` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/06-scryfall-normalization-adapters`

Objectif :
Créer la couche de normalisation Scryfall vers le modèle métier local.

Travaux à réaliser :
1. Créer les adapters vers :
   - CardDefinition
   - CardPrinting
   - Set
2. Définir une stratégie de validation minimale des payloads.
3. Normaliser les données brutes avant mapping.
4. Gérer les champs optionnels, absents ou ambigus.
5. Gérer les cartes multifaces.
6. Lever des exceptions dédiées en cas de payload invalide ou incohérent.
7. Écrire des tests unitaires complets.

Points d'attention :
- ne jamais faire fuiter la structure Scryfall dans le domaine
- cette couche doit être la frontière claire entre le brut distant et le modèle local
- préparer les imports idempotents

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

