# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format s’inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/)
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [0.9.0] - 2026-04-04

### Added

- Consultation catalogue : `CatalogQueryService` avec filtres `CatalogSetFilter`, `CatalogDefinitionFilter`, `CatalogPrintingFilter` (ET sur critères non nuls, résultats triés).
- Tests `test_catalog_query_service.py` et payloads JSON partagés `tests/.../scryfall_json_fixtures.py`.

## [0.8.0] - 2026-04-04

### Added

- Service `CatalogImportService` (`services/catalog_import_service.py`) : import idempotent de payloads Scryfall normalisés (`Mapping`) vers les repositories, sans accès réseau.
- DTO `CatalogImportBatchResult` pour le lot set + cartes.
- Exceptions `CatalogImportInconsistencyError`, `CatalogImportSetScryfallMismatchError`, `CatalogImportBatchSetMismatchError`, `CatalogImportPrintingDefinitionMismatchError`.
- Tests sous `tests/baobab_mtg_catalog/services/` (scénarios nominal, réimport, mise à jour partielle, incohérences, clé locale sans `id` carte).

## [0.7.0] - 2026-04-04

### Added

- Interfaces `SetRepository`, `CardDefinitionRepository`, `CardPrintingRepository` et implémentations `InMemorySetRepository`, `InMemoryCardDefinitionRepository`, `InMemoryCardPrintingRepository` (`repositories/`, `repositories/in_memory/`).
- Exceptions `SetNotFoundError`, `CardDefinitionNotFoundError`, `CardPrintingNotFoundError`, `RepositoryEntityConflictError` pour la consultation référentiel et les violations d’unicité.
- Tests unitaires sous `tests/baobab_mtg_catalog/repositories/`.

## [0.6.0] - 2026-04-04

### Added

- Couche `adapters/scryfall` : `ScryfallSetAdapter`, `ScryfallCardDefinitionAdapter`, `ScryfallCardPrintingAdapter` (payloads JSON `Mapping` → entités domaine).
- Modules `scryfall_payload`, `scryfall_normalize` (validation minimale, alias `set_type` / langue / rareté, CMC, finitions, URIs).
- Exceptions `InvalidPayloadError`, `NormalizationError`, `MappingError` (sous `BaobabMtgCatalogException`).
- Tests unitaires adaptateurs sous `tests/.../adapters/scryfall/`.

## [0.5.0] - 2026-04-04

### Added

- Entité domaine `CardPrinting` (`domain/card_printings`) : impression concrète liée à une `CardDefinition` et un `Set`.
- `CardPrintingIdentifier` (UUID métier), `PrintingImageUris` (URIs http(s) d’illustration).
- Exceptions `InvalidCardPrintingError`, `InvalidCardPrintingIdentifierError`.
- Réexport depuis `baobab_mtg_catalog.domain`.

## [0.4.0] - 2026-04-04

### Added

- Entité domaine `CardDefinition` (`domain/card_definitions`) : carte logique Oracle, distincte de toute impression.
- `CardFace` (face texte / jeu), `CardDefinitionIdentifier` (UUID métier), utilitaires de validation partagés.
- Exceptions `InvalidCardDefinitionError`, `InvalidCardFaceError`, `InvalidCardDefinitionIdentifierError`.
- Réexport `CardDefinition`, `CardFace`, `CardDefinitionIdentifier` depuis `baobab_mtg_catalog.domain`.

## [0.3.0] - 2026-04-04

### Added

- Entité domaine `Set` (`domain/sets`) avec `SetId`, `SetType`, validations métier et corrélation optionnelle `scryfall_set_id`.
- Exceptions `InvalidSetError`, `InvalidSetIdError`, `InvalidSetTypeError`.
- Réexport depuis `baobab_mtg_catalog.domain`.

## [0.2.0] - 2026-04-04

### Added

- Objets de valeur partagés sous `baobab_mtg_catalog.domain.value_objects` : couleurs, identité couleur, langue, rareté, finition, code set, collector number, coût de mana, ligne de types, UUID Scryfall / Oracle, multiverse id, légalité de format.
- Exceptions de validation `InvalidDomainValueError` et types dérivés par famille de valeur.
- Utilitaire interne `uuid_canon` pour la normalisation d’UUID.
- Tests unitaires miroir et réexport public depuis `baobab_mtg_catalog.domain`.

### Changed

- Version catalogue ; configuration flake8 (`per-file-ignores` pour `domain/__init__.py`) et pylint (`SIMILARITIES`).

## [0.1.0] - 2026-04-04

### Added

- Squelette du package `baobab_mtg_catalog` (layout `src/`, sous-packages domaine).
- Exception racine `BaobabMtgCatalogException`.
- Configuration centralisée `pyproject.toml` (build, dépendances, tests, couverture, qualité).
- Documentation initiale (`README.md`, `docs/dev_diary.md`).
- Tests bootstrap et dépendance runtime `baobab-scryfall-api-caller`.
