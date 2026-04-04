# Feature 01 — Project bootstrap

## Branche

`feature/01-project-bootstrap`

## Objectif

Mettre en place le squelette industrialisable du projet `baobab-mtg-catalog`.

## Périmètre

- création du package `baobab_mtg_catalog`
- arborescence initiale
- configuration `pyproject.toml`
- outillage qualité
- fichiers racine de documentation
- exception racine projet
- base d'exports package
- dépendances autorisées / interdites documentées

## Livrables attendus

- structure `src/baobab_mtg_catalog/`
- structure `tests/`
- `pyproject.toml`
- `README.md`
- `CHANGELOG.md`
- `docs/dev_diary.md`
- `BaobabMtgCatalogException`
- configuration outillage complète

## Critères d'acceptation

- package installable en mode editable
- contrôles qualité configurés
- tests bootstrap au vert
- exception de base présente
- documentation initiale créée

## Prompt pour l'IA de développement

```text
Tu développes la feature `01_project_bootstrap` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/01-project-bootstrap`

Contexte :
`baobab-mtg-catalog` est la librairie centrale de référentiel du catalogue Magic: The Gathering. Elle normalise et enrichit les données Scryfall pour fournir un modèle métier local stable, réutilisable par l'écosystème Baobab.

Objectif de la feature :
Mettre en place le bootstrap complet et propre du projet.

Contraintes obligatoires :
- respecter les contraintes de développement communes situées dans `00_dev_contraints.md`
- code source sous `src/baobab_mtg_catalog`
- tests sous `tests/` avec arborescence miroir
- une classe par fichier
- type hints obligatoires
- docstrings sur tout élément public
- couverture cible minimale : 90%
- qualité obligatoire : black, pylint, mypy, flake8, bandit
- toutes les erreurs spécifiques au projet doivent avoir une exception spécifique
- maintenir `docs/dev_diary.md`
- utiliser des commits Conventional Commits

Dépendances :
- dépendance métier autorisée naturelle : `baobab-scryfall-api-caller`
- ne pas dépendre de la collection, des produits scellés, du moteur de règles, de l'API web ou du front-end

Travaux à réaliser :
1. Créer l'arborescence initiale du projet.
2. Créer le package `baobab_mtg_catalog`.
3. Créer les sous-packages initiaux :
   - exceptions
   - domain
   - adapters
   - repositories
   - services
   - facades
   - builders
4. Créer l'exception racine `BaobabMtgCatalogException`.
5. Configurer `pyproject.toml`.
6. Ajouter `README.md`, `CHANGELOG.md` et `docs/dev_diary.md`.
7. Ajouter des tests bootstrap minimaux.
8. Vérifier que le projet est installable et testable.

Workflow obligatoire de fin :
1. lancer tous les tests unitaires
2. lancer tous les contrôles qualité
3. corriger jusqu'à ce que tout soit vert
4. créer une Pull Request vers `main`
5. merger la PR sur `main` seulement si tous les tests, contraintes et contrôles qualité sont OK
```

