# Journal de développement

Les entrées sont classées par **date décroissante** (les plus récentes en premier).

---

## 2026-04-04

### Feature 07 — Repositories in-memory du référentiel

#### Modifications

- Package `repositories` : ABC `SetRepository`, `CardDefinitionRepository`, `CardPrintingRepository` ; implémentations `InMemory*` avec index par id métier, clés naturelles et (le cas échéant) ids Scryfall.
- Exceptions `SetNotFoundError`, `CardDefinitionNotFoundError`, `CardPrintingNotFoundError`, `RepositoryEntityConflictError`.
- Tests miroir `tests/baobab_mtg_catalog/repositories/in_memory/`.
- Version **0.7.0**.

#### Décisions d’architecture

- **Pas de moteur de recherche** : filtres limités (`list_by_normalized_name` en égalité exacte, `list_by_set_id`, `list_by_set_and_collector`) ; le tri est par id métier pour un ordre stable.
- **Idempotence stockage** : `upsert` remplace l’entité de même id métier et réindexe code / oracle / clé naturelle printing (y compris retrait des anciens index lors d’une correction).
- **Unicité** : un `SetCode` et un `scryfall_set_id` (si présent) par `SetId` ; un `OracleId` par `CardDefinitionIdentifier` ; une clé naturelle printing (`ScryfallId` ou triplet set/collector/langue) par `CardPrintingIdentifier`.

### Feature 06 — Adaptateurs de normalisation Scryfall

#### Modifications

- Package `adapters/scryfall` : `ScryfallSetAdapter`, `ScryfallCardDefinitionAdapter`, `ScryfallCardPrintingAdapter` ; modules `scryfall_payload`, `scryfall_normalize`.
- Exceptions `InvalidPayloadError`, `NormalizationError`, `MappingError` exportées depuis `baobab_mtg_catalog.exceptions` (suffixe `Error` aligné sur le projet ; équivalent aux *Exception* évoquées dans le cahier des charges).
- Tests sous `tests/.../adapters/scryfall/`.
- Version **0.6.0**.

#### Décisions d’architecture

- **Isolement** : aucun type du domaine ne référence Scryfall ; seuls les adaptateurs connaissent les noms de champs JSON.
- **Identifiants métier** : toujours injectés depuis l’extérieur pour préparer l’import idempotent (résolution par `natural_key()` puis réutilisation des UUID persistés).
- **Multi-face** : si `card_faces` est une liste non vide, elle est la source des `CardFace` ; sinon la racine carte est traitée comme face unique.
- **Erreurs** : `InvalidPayloadError` / `NormalizationError` ne sont pas enveloppées par `MappingError` ; ce dernier encapsule les autres `BaobabMtgCatalogException` lors du mapping vers valeur / entité.

### Feature 05 — Modèle domaine `CardPrinting`

#### Modifications

- Package `domain/card_printings` : `CardPrinting`, `CardPrintingIdentifier`, `PrintingImageUris`, `validation_utils` (URIs http(s)).
- Exceptions `InvalidCardPrintingError`, `InvalidCardPrintingIdentifierError`.
- Réexport depuis `baobab_mtg_catalog.domain`.
- Tests miroir sous `tests/.../domain/card_printings/`.
- Version **0.5.0**.

#### Décisions d’architecture

- **Identité d’entité** : `__eq__` / `__hash__` sur `CardPrintingIdentifier` (UUID métier persistance).
- **Idempotence** : `natural_key()` retourne `ScryfallId` si `scryfall_printing_id` est défini ; sinon `(set_id, collector_number, language)` pour les sources sans UUID fournisseur stable.
- **Relations** : références par `CardDefinitionIdentifier` et `SetId` uniquement (pas d’agrégat chargé) pour limiter le couplage et les cycles.
- **Finitions** : `frozenset[Finish]` non vide ; pas de logique inventaire ni de consultation référentiel dans l’entité.

### Feature 04 — Modèle domaine `CardDefinition`

#### Modifications

- Package `domain/card_definitions` : `CardDefinition`, `CardFace`, `CardDefinitionIdentifier`, `validation_utils`.
- Exceptions `InvalidCardDefinitionError`, `InvalidCardFaceError`, `InvalidCardDefinitionIdentifierError`.
- Réexport depuis `baobab_mtg_catalog.domain`.
- Tests miroir sous `tests/.../domain/card_definitions/`.
- Version **0.4.0**.

#### Décisions d’architecture

- **Identité d’entité** : `__eq__` / `__hash__` sur `CardDefinitionIdentifier` (UUID métier persistance).
- **Idempotence / même carte Oracle** : `natural_key()` et `same_logical_card_as()` s’appuient sur `OracleId` ; les ids Scryfall / Multiverse restent optionnels pour les adaptateurs.
- **Mono-face** : alignement obligatoire entre champs agrégés carte et l’unique `CardFace` (y compris P/T / loyauté).
- **Multi-face** : `power` / `toughness` / `loyalty` au niveau carte interdits (portés par chaque face) ; `mana_cost` carte = celui de la première face.
- **Couleurs** : `Color` est un `StrEnum` ; une chaîne égale à une valeur d’enum n’est pas un second membre dans un `frozenset` — les tests rejettent explicitement un type non `Color` (ex. `object()`).

### Feature 03 — Modèle domaine `Set`

#### Modifications

- Package `domain/sets` : entité immuable `Set`, `SetId` (UUID métier), `SetType` (`StrEnum`).
- Exceptions `InvalidSetError`, `InvalidSetIdError`, `InvalidSetTypeError`.
- Réexport `Set`, `SetId`, `SetType` depuis `baobab_mtg_catalog.domain`.
- Tests miroir sous `tests/.../domain/sets/`.
- Version **0.3.0**.

#### Décisions d’architecture

- **Identité d’entité** : égalité et hachage basés uniquement sur `SetId` (UUID métier attribué par la couche application / persistance).
- **Idempotence d’import** : clé naturelle `natural_key()` = `SetCode` ; corrélation optionnelle via `scryfall_set_id` pour les adaptateurs, sans coupler l’entité au JSON Scryfall.
- **Champs optionnels** : `card_count`, `parent_set_code`, `block_code`, drapeaux `digital_only` / `foil_only`, sans logique d’import dans l’entité.

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
