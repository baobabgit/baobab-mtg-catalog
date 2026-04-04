# Feature 05 — Card printing domain model

## Branche

`feature/05-card-printing-domain-model`

## Objectif

Modéliser l'entité métier `CardPrinting`.

## Périmètre

- entité `CardPrinting`
- relation stable vers `CardDefinition`
- relation stable vers `Set`
- collector number
- langue
- rareté
- finitions disponibles
- artist et image URIs si retenus
- identifiants externes utiles
- statut promo / papier / digital si retenus

## Livrables attendus

- `CardPrinting`
- types associés si nécessaires
- tests unitaires complets

## Critères d'acceptation

- distinction nette entre définition logique et impression
- relation claire avec `Set`
- modèle utile à la collection et aux produits

## Prompt pour l'IA de développement

```text
Tu développes la feature `05_card_printing_domain_model` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/05-card-printing-domain-model`

Objectif :
Créer le modèle métier `CardPrinting`, représentant une impression spécifique d'une carte dans un set.

Travaux à réaliser :
1. Créer l'entité `CardPrinting`.
2. Modéliser au minimum :
   - identifiant métier du printing
   - identifiant Scryfall si conservé
   - référence vers `CardDefinition`
   - référence vers `Set`
   - collector number
   - langue
   - rareté
   - finitions disponibles
   - artist si retenu
   - image URIs si retenues
   - identifiants externes utiles
   - statut promo / papier / digital si retenus
3. Définir une stratégie d'identité compatible avec l'import idempotent.
4. Ajouter validations et exceptions dédiées.
5. Écrire les tests unitaires complets.

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

