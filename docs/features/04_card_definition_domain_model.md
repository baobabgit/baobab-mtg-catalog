# Feature 04 — Card definition domain model

## Branche

`feature/04-card-definition-domain-model`

## Objectif

Modéliser l'entité métier `CardDefinition` et ses éventuelles faces.

## Périmètre

- entité `CardDefinition`
- `CardFace` si nécessaire
- identifiant métier de définition
- nom et nom normalisé
- coût de mana, type line, oracle text
- force / endurance, loyauté si pertinents
- couleurs et identité couleur
- mots-clés si retenus
- gestion des faces multiples

## Livrables attendus

- `CardDefinition`
- `CardFace` si nécessaire
- type d'identité logique si utile
- tests unitaires complets

## Critères d'acceptation

- distinction claire entre carte logique et impression
- gestion propre du mono-face et multi-face
- modèle réutilisable par les autres briques

## Prompt pour l'IA de développement

```text
Tu développes la feature `04_card_definition_domain_model` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/04-card-definition-domain-model`

Objectif :
Créer le modèle métier `CardDefinition`, indépendant des éditions concrètes.

Travaux à réaliser :
1. Créer l'entité `CardDefinition`.
2. Créer `CardFace` si nécessaire.
3. Définir la stratégie d'identité logique de la carte.
4. Représenter au minimum :
   - identifiant métier
   - identifiants externes stables utiles
   - nom
   - nom normalisé
   - coût de mana
   - valeur de mana
   - type line
   - oracle text
   - force / endurance si pertinent
   - loyauté si pertinent
   - couleurs
   - identité couleur
   - mots-clés si retenus
   - faces éventuelles
5. Gérer proprement les cartes multifaces.
6. Ajouter validations et exceptions adaptées.
7. Écrire les tests unitaires complets.

Points d'attention :
- distinguer clairement `CardDefinition` de `CardPrinting`
- ne pas dépendre du format Scryfall dans le domaine
- préparer la réutilisation par la collection, le moteur de règles et le deckbuilder

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

