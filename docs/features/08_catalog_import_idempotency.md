# Feature 08 — Catalog import and idempotency

## Branche

`feature/08-catalog-import-idempotency`

## Objectif

Créer le composant d'import du catalogue avec garanties d'idempotence.

## Périmètre

- import d'ensembles de payloads
- coordination des adapters
- consolidation des objets existants
- rechargement d'un set connu
- prévention des doublons
- exceptions d'incohérence

## Livrables attendus

- service ou builder d'import du catalogue
- règles de matching et consolidation
- tests unitaires et d'intégration internes

## Critères d'acceptation

- réimporter un lot connu ne crée pas de doublons incohérents
- les relations entre définitions, printings et sets restent fiables
- les stratégies d'identité sont documentées dans le code

## Prompt pour l'IA de développement

```text
Tu développes la feature `08_catalog_import_idempotency` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/08-catalog-import-idempotency`

Objectif :
Créer le composant d'import du catalogue garantissant des imports idempotents.

Travaux à réaliser :
1. Créer un builder ou service d'import du catalogue.
2. Définir une API permettant d'importer des payloads Scryfall déjà récupérés.
3. Utiliser les adapters de normalisation existants.
4. Alimenter et consolider les repositories.
5. Définir les règles de matching des objets déjà présents.
6. Garantir qu'un rechargement d'un set déjà connu ne produit pas de doublons incohérents.
7. Lever des exceptions métier adaptées si des incohérences sont détectées.
8. Écrire des tests :
   - import nominal
   - rechargement d'un lot connu
   - déduplication
   - relations correctes
   - cas incohérents

Points d'attention :
- documenter clairement la stratégie d'identité
- l'idempotence est un critère majeur de réussite de la librairie

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

