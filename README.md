# baobab-mtg-catalog

Bibliothèque Python de **référentiel catalogue** pour Magic: The Gathering au sein de l’écosystème **Baobab**.

## Description du projet

Le package modélise de façon **stable**, **normalisée** et **exploitable** les données de référence du jeu : cartes logiques (Oracle), impressions dans un set, extensions, finitions, langues, raretés et métadonnées utiles au domaine. Il constitue la **source de vérité métier locale** sur ce qu’est une carte et sur la manière dont une même carte peut exister sous plusieurs printings.

## Rôle dans l’écosystème Baobab

- **Consommateurs typiques** : briques qui ont besoin d’un catalogue MTG partagé (applications métier, synchronisation de données, outils internes) **sans** réimplémenter la normalisation Scryfall ni le modèle domaine.
- **Positionnement** : couche **librairie** (pas de serveur HTTP imposé, pas d’UI). Les appels réseau vers Scryfall restent de la responsabilité de l’appelant ou de `baobab-scryfall-api-caller` ; ce package accepte des `Mapping` JSON déjà obtenus.
- **Contrat** : entités immuables, exceptions hiérarchisées sous `BaobabMtgCatalogException`, persistance abstraite derrière des repositories.

## Périmètre explicite

- **Inclus** : catalogue de référence, normalisation Scryfall → modèle métier, **import idempotent**, consultation par façade et services, **filtres métier** combinés (`CatalogQueryService` + `Catalog*Filter`).
- **Exclu** : possession / inventaire, produits scellés, règles de jeu, construction de deck, interface utilisateur, transport HTTP **métier** (aucun framework web imposé).

## Dépendances

### Autorisées

- **Runtime** : [`baobab-scryfall-api-caller`](https://pypi.org/project/baobab-scryfall-api-caller/) (≥ 1, &lt; 2) — client Scryfall aligné Baobab, optionnel pour **obtenir** les JSON ; l’import catalogue fonctionne sur des `Mapping` fournis par ailleurs.
- **Python** : 3.11+ (voir `pyproject.toml`).

### Interdites dans ce package

Ne pas introduire de dépendances vers : modules **collection** ou inventaire, **produits scellés**, **moteur de règles**, **API web** ou **front-end**. Le catalogue reste indépendant du protocole et de l’UI.

## Architecture (vue rapide)

Couches conceptuelles, du plus stable au plus orchestrateur :

| Couche | Rôle |
|--------|------|
| **Domaine** (`baobab_mtg_catalog.domain`) | Entités et value objects ; aucune dépendance Scryfall brute. |
| **Adaptateurs** (`baobab_mtg_catalog.adapters`) | JSON Scryfall (`Mapping`) → entités domaine ; validation / normalisation. |
| **Repositories** (`baobab_mtg_catalog.repositories`) | Contrats de persistance + impl. in-memory ; accès simple par id / clés naturelles. |
| **Services** (`baobab_mtg_catalog.services`) | Import idempotent, requêtes filtrées, services de lecture par entité. |
| **Façades** (`baobab_mtg_catalog.facades`) | `MtgCatalogFacade` : point d’entrée unique pour les autres briques Baobab. |

Les **données Scryfall brutes** ne traversent pas le domaine : elles sont converties par les adaptateurs, puis stockées et relues comme types métier.

## Carte logique, impression et extension

| Concept | Type domaine | Identité (objet) | Clé naturelle (import / fusion) | Contient typiquement |
|---------|----------------|------------------|----------------------------------|----------------------|
| **Carte logique (Oracle)** | `CardDefinition` | `CardDefinitionIdentifier` | `OracleId` | Nom, mana, texte Oracle, couleurs, faces, etc. **Pas** de set / collector / langue printing. |
| **Impression** | `CardPrinting` | `CardPrintingIdentifier` | `ScryfallId` carte si présent, sinon `(SetId, collector_number, language)` | Lien vers définition + set, rareté, finitions, langue, ids externes optionnels. |
| **Extension (set)** | `Set` | `SetId` | `SetCode` | Nom produit, dates, type d’extension, compteurs, etc. |

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

## API publique du package racine

Le module `baobab_mtg_catalog` expose volontairement peu de symboles pour une intégration simple :

| Symbole | Description |
|---------|-------------|
| `__version__` | Version du distribution package (`importlib.metadata`). |
| `BaobabMtgCatalogException` | Exception racine du projet. |
| `MtgCatalogFacade` | Façade catalogue (import + consultation). |

Le reste de l’API stable est **par sous-package** : `domain`, `repositories`, `adapters`, `services`, `exceptions`, `facades`. Les tests `tests/baobab_mtg_catalog/test_readme_documentation_examples.py` gardent un alignement minimal avec les exemples ci-dessous.

## Utilisation minimale

```python
from baobab_mtg_catalog import BaobabMtgCatalogException, MtgCatalogFacade, __version__

print(__version__)

facade = MtgCatalogFacade.in_memory()

raise BaobabMtgCatalogException("exemple d'erreur métier catalogue")
```

## Façade catalogue (`MtgCatalogFacade`)

Point d’entrée stable pour les autres briques Baobab : import idempotent, consultation par entité et accès aux filtres combinés sans assembler manuellement repositories et services.

- **`MtgCatalogFacade.in_memory()`** : repositories in-memory vides (tests, prototypage).
- **Injection** : `MtgCatalogFacade(set_repository=..., definition_repository=..., printing_repository=...)` pour une persistance partagée.
- **`sets` / `definitions` / `printings`** : services de lecture métier (`SetQueryService`, `CardDefinitionQueryService`, `CardPrintingQueryService`).
- **`catalog`** : `CatalogQueryService` et filtres `CatalogSetFilter`, `CatalogDefinitionFilter`, `CatalogPrintingFilter`.
- **`importer`** : `CatalogImportService` ; **`import_set_and_cards`** sur la façade en est le raccourci.

## Exemple : adapter des payloads Scryfall

Les adaptateurs attendent des objets **similaires au JSON Scryfall** (`Mapping[str, Any]`). Les **UUID métier** (`SetId`, `CardDefinitionIdentifier`, `CardPrintingIdentifier`) sont fournis par l’appelant (souvent issus de la persistance ou générés avant premier enregistrement).

```python
from baobab_mtg_catalog.adapters.scryfall import (
    ScryfallCardDefinitionAdapter,
    ScryfallCardPrintingAdapter,
    ScryfallSetAdapter,
)
from baobab_mtg_catalog.domain import (
    CardDefinitionIdentifier,
    CardPrintingIdentifier,
    SetId,
)

set_payload = {
    "object": "set",
    "id": "11111111-1111-4111-8111-111111111111",
    "code": "lea",
    "name": "Limited Edition Alpha",
    "set_type": "core",
    "released_at": "1993-08-05",
    "digital": False,
    "foil_only": False,
}

card_payload = {
    "object": "card",
    "id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
    "oracle_id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
    "multiverse_id": 600,
    "name": "Lightning Bolt",
    "mana_cost": "{R}",
    "cmc": 1.0,
    "type_line": "Instant",
    "oracle_text": "Lightning Bolt deals 3 damage to any target.",
    "colors": ["R"],
    "color_identity": ["R"],
    "lang": "en",
    "rarity": "common",
    "finishes": ["nonfoil"],
    "collector_number": "116",
    "set": "lea",
}

set_id = SetId.parse("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa")
st = ScryfallSetAdapter.to_set(set_payload, set_id=set_id)

definition_id = CardDefinitionIdentifier.parse("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb")
definition = ScryfallCardDefinitionAdapter.to_card_definition(
    card_payload,
    card_definition_id=definition_id,
)

printing_id = CardPrintingIdentifier.parse("cccccccc-cccc-4ccc-8ccc-cccccccccccc")
printing = ScryfallCardPrintingAdapter.to_card_printing(
    card_payload,
    card_printing_id=printing_id,
    card_definition_id=definition.card_definition_id,
    set_id=st.set_id,
)
```

En pratique, on enchaîne souvent cet enchaînement via **`CatalogImportService`** ou **`MtgCatalogFacade.import_set_and_cards`**, qui résolvent les ids métier de façon **idempotente** (voir section suivante).

## Exemple : import idempotent (façade)

Le service d’import réutilise les adaptateurs et **fusionne** par clés naturelles (`SetCode`, `OracleId`, id Scryfall carte ou triplet set/collector/langue). Réimporter le même lot met à jour le contenu **sans dupliquer** les entités métier lorsque les clés correspondent.

```python
from baobab_mtg_catalog import MtgCatalogFacade

facade = MtgCatalogFacade.in_memory()

set_payload = {
    "object": "set",
    "id": "11111111-1111-4111-8111-111111111111",
    "code": "lea",
    "name": "Limited Edition Alpha",
    "set_type": "core",
    "released_at": "1993-08-05",
    "digital": False,
    "foil_only": False,
}

lightning = {
    "object": "card",
    "id": "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
    "oracle_id": "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
    "multiverse_id": 600,
    "name": "Lightning Bolt",
    "mana_cost": "{R}",
    "cmc": 1.0,
    "type_line": "Instant",
    "oracle_text": "Lightning Bolt deals 3 damage to any target.",
    "colors": ["R"],
    "color_identity": ["R"],
    "lang": "en",
    "rarity": "common",
    "finishes": ["nonfoil"],
    "collector_number": "116",
    "artist": "Christopher Rush",
    "set": "lea",
}

bears = {
    "object": "card",
    "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    "oracle_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
    "multiverse_id": 601,
    "name": "Grizzly Bears",
    "mana_cost": "{1}{G}",
    "cmc": 2.0,
    "type_line": "Creature — Bear",
    "oracle_text": "",
    "colors": ["G"],
    "color_identity": ["G"],
    "lang": "en",
    "rarity": "common",
    "finishes": ["nonfoil"],
    "collector_number": "5",
    "set": "lea",
}

result = facade.import_set_and_cards(set_payload, [lightning, bears])
assert result.cards_imported == 2

# Second import : idempotent (mêmes clés naturelles)
again = facade.import_set_and_cards(set_payload, [lightning, bears])
assert again.cards_imported == 2
```

## Exemple : consulter le catalogue

En reprenant les dictionnaires `set_payload`, `lightning` et `bears` de la section **import idempotent** :

```python
from baobab_mtg_catalog import MtgCatalogFacade
from baobab_mtg_catalog.domain import SetCode
from baobab_mtg_catalog.services import CatalogDefinitionFilter, CatalogPrintingFilter

facade = MtgCatalogFacade.in_memory()
facade.import_set_and_cards(set_payload, [lightning, bears])

st = facade.sets.get_by_code(SetCode.parse("lea"))
definitions_in_set = facade.definitions.list_for_set(st.set_id)
printings_in_set = facade.printings.list_for_set(st.set_id)

bolts_in_lea = facade.printings.find_in_set(
    st.set_id,
    CatalogPrintingFilter(
        definition=CatalogDefinitionFilter(normalized_name_contains="bolt"),
    ),
)

creatures = facade.catalog.find_definitions(
    CatalogDefinitionFilter(type_line_contains="creature"),
)
```

Les critères non nuls des `Catalog*Filter` se combinent par un **ET** logique ; l’ordre des résultats est **déterministe** (tri par identifiant métier). La **légalité de format** n’est pas portée par `CardDefinition` dans cette version : aucun filtre de légalité n’est exposé.

## Objets de valeur du domaine

Les types partagés (couleurs, langue, rareté, finition, codes set / collector, coût de mana, ligne de types, identifiants externes, etc.) vivent sous `baobab_mtg_catalog.domain` et `baobab_mtg_catalog.domain.value_objects`.

```python
from baobab_mtg_catalog.domain import Color, ColorIdentity, ManaCost, SetCode

blue = Color.parse("u")
identity = ColorIdentity.from_iterable([Color.GREEN, Color.BLUE])
cost = ManaCost.parse("{2}{G}")
code = SetCode.parse("mh3")
```

Les erreurs de validation lèvent des sous-classes de `InvalidDomainValueError` (sous-classe de `BaobabMtgCatalogException`).

## Entité `CardDefinition` (carte logique)

La **carte Oracle** est modélisée par `CardDefinition` avec des `CardFace` (mono ou multi-face). Voir le tableau [Carte logique, impression et extension](#carte-logique-impression-et-extension).

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

Voir le tableau [Carte logique, impression et extension](#carte-logique-impression-et-extension).

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

## Consultation filtrée (`CatalogQueryService`)

Utilisable via **`facade.catalog`** ou en instanciant le service avec les trois repositories. Filtres : `CatalogSetFilter`, `CatalogDefinitionFilter`, `CatalogPrintingFilter`.

```python
from baobab_mtg_catalog.services import (
    CatalogDefinitionFilter,
    CatalogPrintingFilter,
    CatalogQueryService,
)

# q = CatalogQueryService(
#     set_repository=...,
#     definition_repository=...,
#     printing_repository=...,
# )
# q.find_printings(
#     CatalogPrintingFilter(
#         set_code=SetCode.parse("lea"),
#         definition=CatalogDefinitionFilter(any_of_colors=frozenset({Color.RED})),
#     )
# )
```

## Import catalogue (service bas niveau)

Équivalent de la façade pour qui compose déjà les repositories :

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
result = svc.import_set_and_cards(set_payload, card_payloads)
```

## Repositories in-memory

Contrats sous `baobab_mtg_catalog.repositories` : `upsert` idempotent, index sur clés naturelles, erreurs `SetNotFoundError`, `CardDefinitionNotFoundError`, `CardPrintingNotFoundError`, `RepositoryEntityConflictError`.

```python
from baobab_mtg_catalog.repositories import InMemorySetRepository

repo = InMemorySetRepository()
repo.upsert(st)
assert repo.get_by_code(st.code) == st
```

## Adaptateurs Scryfall (erreurs)

- `InvalidPayloadError` : structure minimale absente ou types JSON incorrects.
- `NormalizationError` : valeur Scryfall ambiguë ou incohérente après normalisation.
- `MappingError` : échec de construction d’un type domaine (cause conservée).

## Documentation projet

- Spécifications : `docs/001_specifications.md`
- Contraintes de développement : `docs/000_dev_constraints.md`
- Checklist audit **v1.0.0** : `docs/v1.0.0_release_readiness_checklist.md`
- Journal : `docs/dev_diary.md`
- Changelog : `CHANGELOG.md`

## Contribution

- Branches de fonctionnalité : `feature/nom` (kebab-case).
- Commits : [Conventional Commits](https://www.conventionalcommits.org/).
- Respecter les contraintes `docs/000_dev_constraints.md`.

## Licence

Propriétaire — usage selon les conditions du dépôt Baobab.
