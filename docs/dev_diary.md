# Journal de développement

Les entrées sont classées par **date décroissante** (les plus récentes en premier).

---

## 2026-04-04

### Feature 02 — Objets de valeur domaine partagés

#### Modifications

- Package `domain/value_objects` : `Color`, `ColorIdentity`, `Language`, `Rarity`, `Finish`, `SetCode`, `CollectorNumber`, `ManaCost`, `CardTypeLine`, `ScryfallId`, `OracleId`, `MultiverseId`, `LegalityStatus`, `GameFormat`, `FormatLegality`.
- Module utilitaire `uuid_canon` pour la normalisation UUID partagée (sans couplage HTTP).
- Hiérarchie d’exceptions : `InvalidDomainValueError` et erreurs fines par type (`InvalidManaCostError`, …) dérivées de `BaobabMtgCatalogException`.
- Réexport domaine via `domain/__init__.py` (wildcard contrôlé + ignores flake8/pylint documentés).
- Tests miroir par classe, couverture > 90 % ; configuration pylint `SIMILARITIES.min-similarity-lines` et `flake8` `per-file-ignores` pour le réexport.
- Version **0.2.0**.

#### Buts

- Fournir un socle de types métier stables pour `CardDefinition`, `CardPrinting` et `Set`, découplés des payloads Scryfall bruts.

#### Décisions d’architecture

- **Validation syntaxique pour `ManaCost`** : acceptation de toute suite de jetons `{...}` non imbriqués ; pas de simulation complète des règles Oracle (évolution possible ultérieure).
- **`Language` / `Finish` / `Rarity` en `StrEnum`** : liste fermée documentée ; les adaptateurs Scryfall devront mapper ou étendre l’enum si de nouvelles valeurs officielles apparaissent.
- **`GameFormat` en slug validé** plutôt qu’enum fermée : nouveaux formats Wizards sans release bibliothèque.
- **Légalité** : `FormatLegality` agrège `GameFormat` + `LegalityStatus` pour usage futur en filtrage catalogue.

### Feature 01 — Bootstrap projet

#### Modifications

- Création du layout `src/baobab_mtg_catalog` avec sous-packages `exceptions`, `domain`, `adapters`, `repositories`, `services`, `facades`, `builders`.
- Ajout de `BaobabMtgCatalogException` et exports publics dans `baobab_mtg_catalog.__init__` (version via `importlib.metadata`, repli `0.1.0` si metadata absente).
- Configuration `pyproject.toml` : setuptools, pytest + coverage (seuil 90 %, artefacts sous `docs/tests/coverage/`), black, pylint, mypy strict sur le code source, flake8 via `Flake8-pyproject`, bandit sur `src/`.
- Documentation : `README.md`, `CHANGELOG.md`, marqueur `py.typed`.
- Tests miroir : `test_baobab_mtg_catalog_exception`, `test_package_init`.

#### Buts

- Livrer la **feature 01 — project bootstrap** : projet installable en éditable, outillage qualité homogène, exception racine et arborescence prête pour les features métier.

#### Impact

- Base industrielle alignée sur `docs/000_dev_constraints.md` ; les prochaines features pourront ajouter classes de domaine et adaptateurs sans restructurer le dépôt.

#### Décisions d’architecture

- **Séparation stricte** : sous-packages vides documentés par docstrings de module pour cadrer `CardDefinition` / `CardPrinting` / `Set` et les flux Scryfall → domaine dans des emplacements dédiés.
- **Dépendance runtime** : `baobab-scryfall-api-caller` comme seule dépendance métier externe explicite au bootstrap ; aucune intégration collection / UI / HTTP dans ce package.
- **Couverture** : fichiers de coverage localisés sous `docs/tests/coverage/` conformément aux contraintes projet.
