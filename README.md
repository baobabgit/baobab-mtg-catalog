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
from baobab_mtg_catalog import BaobabMtgCatalogException, MtgCatalogFacade, __version__

print(__version__)

facade = MtgCatalogFacade.in_memory()
# facade.import_set_and_cards(set_payload, card_payloads)
# facade.sets.get_by_code(...), facade.definitions.get_by_oracle_id(...), etc.

raise BaobabMtgCatalogException("exemple d'erreur métier catalogue")
```

## Façade catalogue (`MtgCatalogFacade`)

Point d’entrée stable pour les autres briques Baobab : import idempotent, consultation par entité et accès aux filtres combinés sans assembler manuellement repositories et services.

- **`MtgCatalogFacade.in_memory()`** : repositories in-memory vides, prêts pour tests ou prototypage.
- **Injection** : `MtgCatalogFacade(set_repository=..., definition_repository=..., printing_repository=...)` pour brancher une persistance partagée.
- **`sets` / `definitions` / `printings`** : `SetQueryService`, `CardDefinitionQueryService`, `CardPrintingQueryService` (get, listes par set ou par carte logique, `find` / `find_in_set` pour les critères métier).
- **`catalog`** : `CatalogQueryService` inchangé (filtres `Catalog*Filter`).
- **`importer`** : `CatalogImportService` ; **`import_set_and_cards`** sur la façade est un raccourci équivalent.

```python
from baobab_mtg_catalog import MtgCatalogFacade
from baobab_mtg_catalog.domain import SetCode

facade = MtgCatalogFacade.in_memory()
# Importer des Mapping JSON Scryfall via facade.import_set_and_cards(...)
st = facade.sets.get_by_code(SetCode.parse("lea"))
defs = facade.definitions.list_for_set(st.set_id)
prints = facade.printings.list_for_set(st.set_id)
```

## Objets de valeur du domaine

Les types partagés (couleurs, langue, rareté, finition, codes set / collector, coût de mana, ligne de types, identifiants externes, légalité de format) vivent sous `baobab_mtg_catalog.domain` et `baobab_mtg_catalog.domain.value_objects`. Ils sont **indépendants des DTO Scryfall** : les adaptateurs doivent parser puis construire ces types.

```python
from baobab_mtg_catalog.domain import Color, ColorIdentity, ManaCost, SetCode

blue = Color.parse("u")
identity = ColorIdentity.from_iterable([Color.GREEN, Color.BLUE])
cost = ManaCost.parse("{2}{G}")
code = SetCode.parse("mh3")
```

Les erreurs de validation lèvent des sous-classes de `InvalidDomainValueError` (elle-même sous-classe de `BaobabMtgCatalogException`), par exemple `InvalidManaCostError`, `InvalidSetCodeError`.

## Entité `CardDefinition` (carte logique)

La **carte Oracle** (indépendante d’une impression précise) est modélisée par `CardDefinition` avec des `CardFace` (mono ou multi-face). L’**identité objet** repose sur `CardDefinitionIdentifier` ; la **clé naturelle** pour fusionner un import est `OracleId` (`natural_key()`). Aucun attribut de printing (set, collector number, finition, langue) n’appartient à ce modèle.

```python
from baobab_mtg_catalog.domain import (
    CardDefinition,
    CardDefinitionIdentifier,
    CardFace,
    CardTypeLine,
    Color,
    ColorIdentity,
    ManaCost,
    OracleId,
)

face = CardFace(
    name="Elvish Mystic",
    normalized_name="elvish mystic",
    mana_cost=ManaCost.parse("{G}"),
    type_line=CardTypeLine.parse("Creature — Elf Druid"),
    oracle_text="{T}: Add {G}.",
    colors=frozenset({Color.GREEN}),
    power="1",
    toughness="1",
)
card = CardDefinition(
    card_definition_id=CardDefinitionIdentifier.parse(
        "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
    ),
    oracle_id=OracleId.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"),
    name=face.name,
    normalized_name=face.normalized_name,
    mana_cost=face.mana_cost,
    mana_value=1.0,
    type_line=face.type_line,
    oracle_text=face.oracle_text,
    colors=face.colors,
    color_identity=ColorIdentity.from_iterable([Color.GREEN]),
    faces=(face,),
    power=face.power,
    toughness=face.toughness,
)
assert card.natural_key() == card.oracle_id
```

## Entité `CardPrinting` (impression)

Une **impression** relie une `CardDefinition` à un `Set` (références par identifiants métier), avec langue, numéro de collection, rareté, finitions et métadonnées optionnelles (artiste, URIs d’image, date de sortie, ids externes). L’**identité objet** repose sur `CardPrintingIdentifier` ; la **clé naturelle** pour l’import idempotent privilégie `scryfall_printing_id` s’il est présent, sinon le triplet `(set_id, collector_number, language)`.

```python
from baobab_mtg_catalog.domain import (
    CardDefinitionIdentifier,
    CardPrinting,
    CardPrintingIdentifier,
    CollectorNumber,
    Finish,
    Language,
    Rarity,
    ScryfallId,
    SetId,
)

printing = CardPrinting(
    card_printing_id=CardPrintingIdentifier.parse(
        "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
    ),
    card_definition_id=CardDefinitionIdentifier.parse(
        "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
    ),
    set_id=SetId.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc"),
    collector_number=CollectorNumber.parse("123"),
    language=Language.EN,
    rarity=Rarity.RARE,
    finishes=frozenset({Finish.NONFOIL, Finish.FOIL}),
    scryfall_printing_id=ScryfallId.parse(
        "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
    ),
)
assert isinstance(printing.natural_key(), ScryfallId)
```

## Entité `Set` (extension)

Une extension catalogue est modélisée par `Set` (`baobab_mtg_catalog.domain`). L’**identité objet** repose sur `SetId` (UUID métier) ; la **clé naturelle** pour fusionner un réimport sans doublon est le `SetCode` (`natural_key()`).

```python
from datetime import date

from baobab_mtg_catalog.domain import Set, SetCode, SetId, SetType

st = Set(
    set_id=SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
    code=SetCode.parse("one"),
    name="Phyrexia: All Will Be One",
    release_date=date(2023, 2, 3),
    set_type=SetType.EXPANSION,
    card_count=271,
    digital_only=False,
)
assert st.natural_key().value == "ONE"
```

## Consultation filtrée (requêtes métier)

`CatalogQueryService` (`baobab_mtg_catalog.services`) parcourt les repositories (typiquement in-memory) et applique des filtres immuables : `CatalogSetFilter`, `CatalogDefinitionFilter`, `CatalogPrintingFilter`. Les critères renseignés sont combinés par un **ET** ; les sous-chaînes (`name_contains`, `type_line_contains`, etc.) ignorent la casse après normalisation. Les impressions peuvent restreindre la définition liée via `CatalogPrintingFilter.definition`. La légalité de format n’est pas portée par `CardDefinition` : aucun filtre de légalité n’est proposé.

```python
from baobab_mtg_catalog.services import (
    CatalogDefinitionFilter,
    CatalogPrintingFilter,
    CatalogQueryService,
    CatalogSetFilter,
)

# q = CatalogQueryService(set_repository=..., definition_repository=..., printing_repository=...)
# q.find_printings(CatalogPrintingFilter(set_code=..., definition=CatalogDefinitionFilter(...)))
```

## Import catalogue idempotent (Scryfall → référentiel)

Le service `CatalogImportService` (`baobab_mtg_catalog.services`) enchaîne les adaptateurs Scryfall et les repositories : résolution des `SetId` / `CardDefinitionIdentifier` / `CardPrintingIdentifier` par clés naturelles (`SetCode`, `OracleId`, id Scryfall carte ou triplet set/collector/langue), `upsert` systématique et contrôles de cohérence (code set du lot vs champ `set` de la carte, alignement `scryfall_set_id`, lien printing ↔ définition). Aucun appel HTTP : les `Mapping` sont fournis par l’appelant (fichiers, cache, client existant).

```python
from baobab_mtg_catalog.repositories import (
    InMemoryCardDefinitionRepository,
    InMemoryCardPrintingRepository,
    InMemorySetRepository,
)
from baobab_mtg_catalog.services import CatalogImportService

svc = CatalogImportService(
    set_repository=InMemorySetRepository(),
    definition_repository=InMemoryCardDefinitionRepository(),
    printing_repository=InMemoryCardPrintingRepository(),
)
# set_payload et card_payloads : objets JSON Scryfall typiques (champs attendus par les adaptateurs).
result = svc.import_set_and_cards(set_payload, card_payloads)
```

## Repositories in-memory (référentiel local)

Les contrats de persistance vivent sous `baobab_mtg_catalog.repositories` : `upsert` idempotent par identifiant métier, index sur les clés naturelles (`SetCode`, `OracleId`, `CardPrinting.natural_key()`), lectures simples (`get_by_id`, `get_by_code`, `get_by_oracle_id`, `get_by_scryfall_printing_id`, `list_by_set_id`, etc.) et listes ordonnées de façon déterministe. Les absences lèvent `SetNotFoundError`, `CardDefinitionNotFoundError` ou `CardPrintingNotFoundError` ; les collisions d’unicité lèvent `RepositoryEntityConflictError`.

```python
from baobab_mtg_catalog.repositories import InMemorySetRepository

repo = InMemorySetRepository()
repo.upsert(st)
assert repo.get_by_code(st.code) == st
```

## Adaptateurs Scryfall (normalisation)

Les objets JSON Scryfall (`Mapping[str, Any]`, typiquement issus de `baobab-scryfall-api-caller` ou d’un parseur JSON) sont convertis en entités domaine sous `baobab_mtg_catalog.adapters` : `ScryfallSetAdapter`, `ScryfallCardDefinitionAdapter`, `ScryfallCardPrintingAdapter`. Les **UUID métier** (`SetId`, `CardDefinitionIdentifier`, `CardPrintingIdentifier`) restent la responsabilité de l’appelant (persistance, résolution idempotente via `natural_key()`).

- `InvalidPayloadError` : structure minimale absente ou types JSON incorrects.
- `NormalizationError` : valeur Scryfall ambiguë ou incohérente après normalisation.
- `MappingError` : échec de construction d’un type domaine (cause conservée).

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
