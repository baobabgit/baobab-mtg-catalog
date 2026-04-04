# Feature 11 — Documentation, examples and release readiness

## Branche

`feature/11-documentation-examples-and-release-readiness`

## Objectif

Finaliser la documentation, les exemples d'usage et la préparation à une v1.0.0.

## Périmètre

- README complet
- exemples d'usage
- documentation des imports idempotents
- documentation des dépendances autorisées / interdites
- vérification des exports publics
- checklist de readiness

## Livrables attendus

- README riche
- exemples clairs
- CHANGELOG mis à jour
- dev diary à jour
- checklist v1.0.0

## Critères d'acceptation

- la librairie est compréhensible sans lire le code
- les différences entre `CardDefinition` et `CardPrinting` sont explicites
- l'idempotence et les usages d'intégration sont documentés

## Prompt pour l'IA de développement

```text
Tu développes la feature `11_documentation_examples_and_release_readiness` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/11-documentation-examples-and-release-readiness`

Objectif :
Finaliser la documentation, les exemples d'usage et préparer la librairie pour une version stable.

Travaux à réaliser :
1. Compléter `README.md` avec :
   - description du projet
   - rôle de source de vérité locale
   - différence entre `CardDefinition` et `CardPrinting`
   - installation
   - architecture rapide
   - exemple d'import depuis payload Scryfall
   - exemple de consultation du référentiel
2. Vérifier les exports publics du package.
3. Compléter `CHANGELOG.md`.
4. Mettre à jour `docs/dev_diary.md`.
5. Ajouter si utile des tests de non-régression.
6. Préparer une checklist de readiness v1.0.0.

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

