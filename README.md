# baobab-mtg-catalog

Bibliothèque Python de **référentiel catalogue** pour Magic: The Gathering au sein de l’écosystème Baobab.

Elle modélise de façon stable et normalisée les données de référence du jeu (cartes, printings, sets, éditions, finitions, langues, raretés et métadonnées utiles au domaine). Elle constitue la **source de vérité métier locale** sur ce qu’est une carte et sur la manière dont une même carte peut exister sous plusieurs impressions.

## Périmètre explicite

- **Inclus** : catalogue de référence, normalisation Scryfall → modèle métier, import idempotent, consultation filtrable via services / façades.
- **Exclu** : possession / inventaire, produits scellés, règles de jeu, construction de deck, interface utilisateur, protocole HTTP.

## Dépendances

- **Autorisée (métier)** : [`baobab-scryfall-api-caller`](https://pypi.org/project/baobab-scryfall-api-caller/) — client d’accès à l’API Scryfall aligné Baobab.
- **Interdites dans ce package** : modules collection, produits scellés, moteur de règles, API web ou front-end (pas de couplage UI / transport).

## Prérequis

- Python **3.11+**

## Installation (mode éditable)

```bash
pip install -e ".[dev]"
```

## Tests et qualité

```bash
pytest
black src tests
flake8 src tests
pylint src/baobab_mtg_catalog tests
mypy src/baobab_mtg_catalog tests
bandit -r src/baobab_mtg_catalog
```

La couverture est mesurée avec seuil minimal **90 %** ; les artefacts sont générés sous `docs/tests/coverage/` (voir `pyproject.toml`).

## Utilisation minimale

```python
from baobab_mtg_catalog import BaobabMtgCatalogException, __version__

print(__version__)

raise BaobabMtgCatalogException("exemple d'erreur métier catalogue")
```

## Documentation projet

- Spécifications : `docs/001_specifications.md`
- Contraintes de développement : `docs/000_dev_constraints.md`
- Journal : `docs/dev_diary.md`
- Changelog : `CHANGELOG.md`

## Contribution

- Branches de fonctionnalité : `feature/nom` (kebab-case).
- Commits : [Conventional Commits](https://www.conventionalcommits.org/).
- Respecter les contraintes `docs/000_dev_constraints.md` (structure `src/`, tests miroir, une classe par fichier, types et docstrings publics, outillage black / pylint / mypy / flake8 / bandit).

## Licence

Propriétaire — usage selon les conditions du dépôt Baobab.
