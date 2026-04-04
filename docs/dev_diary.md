# Journal de développement

Les entrées sont classées par **date décroissante** (les plus récentes en premier).

---

## 2026-04-04

### Modifications

- Création du layout `src/baobab_mtg_catalog` avec sous-packages `exceptions`, `domain`, `adapters`, `repositories`, `services`, `facades`, `builders`.
- Ajout de `BaobabMtgCatalogException` et exports publics dans `baobab_mtg_catalog.__init__` (version via `importlib.metadata`, repli `0.1.0` si metadata absente).
- Configuration `pyproject.toml` : setuptools, pytest + coverage (seuil 90 %, artefacts sous `docs/tests/coverage/`), black, pylint, mypy strict sur le code source, flake8 via `Flake8-pyproject`, bandit sur `src/`.
- Documentation : `README.md`, `CHANGELOG.md`, marqueur `py.typed`.
- Tests miroir : `test_baobab_mtg_catalog_exception`, `test_package_init`.

### Buts

- Livrer la **feature 01 — project bootstrap** : projet installable en éditable, outillage qualité homogène, exception racine et arborescence prête pour les features métier.

### Impact

- Base industrielle alignée sur `docs/000_dev_constraints.md` ; les prochaines features pourront ajouter classes de domaine et adaptateurs sans restructurer le dépôt.

### Décisions d’architecture

- **Séparation stricte** : sous-packages vides documentés par docstrings de module pour cadrer `CardDefinition` / `CardPrinting` / `Set` et les flux Scryfall → domaine dans des emplacements dédiés.
- **Dépendance runtime** : `baobab-scryfall-api-caller` comme seule dépendance métier externe explicite au bootstrap ; aucune intégration collection / UI / HTTP dans ce package.
- **Couverture** : fichiers de coverage localisés sous `docs/tests/coverage/` conformément aux contraintes projet.
