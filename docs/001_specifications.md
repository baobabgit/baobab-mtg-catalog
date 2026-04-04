# Cahier des charges — `baobab-mtg-catalog`

## 1. Présentation

### 1.1 Nom du projet

- **Repository** : `baobab-mtg-catalog`
- **Package Python** : `baobab_mtg_catalog`

### 1.2 Définition

`baobab-mtg-catalog` est la librairie de **référentiel du catalogue Magic: The Gathering**. Son rôle est de représenter de manière stable, normalisée et exploitable les données de référence du jeu : cartes, printings, sets, éditions, finitions, langues, raretés et métadonnées utiles au domaine.

Elle constitue la **source de vérité métier locale** sur ce qu'est une carte et sur la manière dont une même carte peut exister sous plusieurs impressions. Elle ne gère ni la possession, ni les produits scellés, ni les règles de jeu, ni la construction de deck : elle décrit le **catalogue**, pas l'inventaire ni le gameplay.

## 2. Vision produit

La librairie doit jouer le rôle de **langage commun du catalogue MTG** pour l'écosystème Baobab. Elle doit absorber les structures techniques de Scryfall, en éliminer les ambiguïtés et exposer un modèle métier local, stable et réutilisable.

Les autres briques Baobab ne doivent pas réinterpréter directement Scryfall. Elles doivent consommer le modèle fourni par `baobab-mtg-catalog`.

## 3. Responsabilités principales

### 3.1 Représentation du catalogue Magic

La librairie doit fournir des modèles métiers clairs pour représenter :

- la carte logique ;
- son ou ses printings ;
- les sets ;
- les finitions disponibles ;
- les attributs structurants du jeu.

Elle doit distinguer clairement :

- la **carte logique** ;
- la **version imprimée** de cette carte ;
- le **set** dans lequel cette impression apparaît.

### 3.2 Normalisation des données Scryfall

La librairie doit consommer et transformer les données issues de `baobab-scryfall-api-caller` en objets de domaine propres, stables et adaptés au reste de l'écosystème Baobab.

Elle doit :

- absorber les structures brutes de l'API distante ;
- normaliser les champs utiles ;
- résoudre les ambiguïtés techniques ;
- produire un modèle local cohérent ;
- isoler le domaine Baobab des variations du fournisseur externe.

### 3.3 Enrichissement métier

Au-delà du simple mapping technique, la librairie doit pouvoir enrichir la donnée pour des usages métier, notamment :

- faciliter la comparaison entre printings ;
- exposer des critères de filtrage métiers ;
- consolider des champs utiles à la collection, aux produits ou au moteur de jeu ;
- fournir des identifiants et représentations stables au reste du système.

### 3.4 Consultation du référentiel

La librairie doit permettre de rechercher, filtrer, charger et parcourir le catalogue selon différents critères, par exemple :

- par nom de carte ;
- par identifiant externe ;
- par identifiant métier ;
- par set ;
- par numéro de collection ;
- par couleur ;
- par identité couleur ;
- par rareté ;
- par type ;
- par légalité de format si cette information est conservée.

### 3.5 Import idempotent

La librairie doit permettre des importations **idempotentes**. Réimporter un set ou un lot déjà connu ne doit pas produire de doublons incohérents.

Elle doit donc définir et documenter :

- la stratégie d'identification des `CardDefinition` ;
- la stratégie d'identification des `CardPrinting` ;
- la stratégie d'identification des `Set` ;
- les règles de consolidation lors d'un rechargement.

## 4. Ce que la librairie doit gérer

- cartes logiques ;
- faces de cartes si nécessaire ;
- printings ;
- sets ;
- finitions ;
- rareté ;
- langue ;
- coût de mana ;
- identité couleur ;
- texte oracle ;
- types et sous-types ;
- numéro de collection ;
- identifiants externes utiles ;
- images ou URI d'images si retenues ;
- éventuellement les légalitès de format si retenues dans le modèle.

## 5. Ce que la librairie ne doit pas gérer

`baobab-mtg-catalog` ne doit pas gérer :

- la possession d'une carte par un usager ;
- les copies physiques possédées ;
- les boosters, displays ou produits scellés ;
- les scans de codes-barres ;
- les probabilités d'ouverture ;
- les règles de partie ;
- la construction ou l'optimisation de decks ;
- l'exposition HTTP ;
- l'interface React.

## 6. Place dans l'architecture globale

`baobab-mtg-catalog` est une librairie **centrale et transversale**. Elle est consommée par :

- `baobab-mtg-products` ;
- `baobab-collection-core` ou la brique de collection ;
- `baobab-mtg-rules-engine` ;
- `baobab-mtg-deckbuilder` ;
- `baobab-mtg-platform` ;
- `baobab-mtg-api`.

Elle doit fournir à toutes ces briques un **langage commun** pour décrire le catalogue MTG.

## 7. Dépendances autorisées et interdites

### 7.1 Dépendance métier autorisée

La dépendance naturelle de cette librairie est :

- `baobab-scryfall-api-caller`

### 7.2 Dépendances possibles

La librairie peut éventuellement dépendre de briques techniques génériques de :

- sérialisation ;
- identifiants ;
- cache local ;
- outillage purement technique.

### 7.3 Dépendances interdites

La librairie ne doit pas dépendre de :

- la collection ;
- les produits scellés ;
- le moteur de règles ;
- l'API web ;
- le front-end.

## 8. Modèle métier attendu

La librairie doit distinguer explicitement les concepts suivants.

### 8.1 `CardDefinition`

Représente la carte logique.

Exemples d'attributs :

- identifiant métier de définition ;
- identifiants externes stables utiles ;
- nom ;
- nom normalisé ;
- coût de mana ;
- valeur de mana ;
- type line ;
- oracle text ;
- force / endurance si pertinent ;
- loyauté si pertinent ;
- identité couleur ;
- couleurs ;
- faces éventuelles ;
- mots-clés si conservés.

### 8.2 `CardPrinting`

Représente une impression spécifique.

Exemples d'attributs :

- identifiant métier de printing ;
- identifiant Scryfall si conservé ;
- `CardDefinition` associée ;
- `Set` associé ;
- collector number ;
- langue ;
- rareté ;
- finitions disponibles ;
- illustration / artist / image URIs si retenus ;
- statut promo si retenu ;
- disponibilité papier / digital si retenue.

### 8.3 `Set`

Représente un set Magic.

Exemples d'attributs :

- identifiant métier ;
- code ;
- nom ;
- date de sortie ;
- type de set ;
- taille estimée ;
- métadonnées utiles au domaine.

### 8.4 Objets de valeur partagés

Le modèle doit s'appuyer, selon besoin, sur des objets de valeur ou types dédiés, par exemple :

- `ManaCost` ;
- `Color` ;
- `ColorIdentity` ;
- `Language` ;
- `Rarity` ;
- `Finish` ;
- `CollectorNumber` ;
- `TypeLine` ;
- `ExternalIdentifiers` ;
- `FormatLegality` si retenu.

## 9. Cas d'usage typiques

- importer un set à partir de Scryfall ;
- recharger un set déjà connu sans dupliquer les objets ;
- rechercher toutes les printings d'une carte ;
- retrouver une carte par identifiant Scryfall ou identifiant métier ;
- filtrer les cartes d'un set par rareté ou couleur ;
- fournir à la collection la définition exacte d'une carte possédée ;
- fournir au moteur de jeu la représentation d'une carte jouable.

## 10. Exigences de conception

La librairie doit :

- être indépendante de l'interface utilisateur ;
- être indépendante du protocole HTTP ;
- exposer un modèle de domaine clair ;
- distinguer le brut Scryfall du métier local ;
- être testable sans accès réseau pour les tests unitaires ;
- permettre des importations idempotentes ;
- pouvoir être utilisée aussi bien dans un service local que dans un système central.

## 11. Architecture cible

L'architecture doit suivre une séparation nette entre :

- **domaine** ;
- **adapters Scryfall** ;
- **repositories** ;
- **services d'import** ;
- **services de consultation** ;
- **façade publique**.

Une structure cible possible est la suivante :

```text
src/baobab_mtg_catalog/
├── adapters/
│   └── scryfall/
├── builders/
├── domain/
│   ├── card_definitions/
│   ├── card_printings/
│   ├── sets/
│   └── shared/
├── exceptions/
├── facades/
├── repositories/
│   ├── interfaces/
│   └── in_memory/
└── services/
```

## 12. Services attendus

La librairie doit exposer au minimum :

- un service d'import / construction du catalogue ;
- des services de consultation des `CardDefinition` ;
- des services de consultation des `CardPrinting` ;
- des services de consultation des `Set` ;
- une façade de haut niveau simple à consommer.

## 13. Gestion des imports

La couche d'import doit :

- accepter des payloads déjà récupérés ;
- valider les structures minimales ;
- mapper vers les objets métier ;
- consolider les données existantes ;
- garantir l'idempotence ;
- lever des exceptions spécifiques en cas d'incohérence.

## 14. Gestion des exceptions

La librairie doit définir une hiérarchie propre d'exceptions, avec une exception racine projet et des exceptions spécialisées par domaine, conformément aux contraintes communes de développement. fileciteturn0file0

## 15. Exigences de qualité et de développement

Les mêmes contraintes de développement que les autres librairies Baobab s'appliquent ici, notamment :

- code sous `src/baobab_mtg_catalog` ;
- tests sous `tests/` avec arborescence miroir ;
- une classe par fichier ;
- annotations de type obligatoires ;
- docstrings sur les éléments publics ;
- couverture minimale cible de 90 % ;
- configuration centralisée dans `pyproject.toml` ;
- contrôles `black`, `pylint`, `mypy`, `flake8`, `bandit` ;
- `README.md`, `CHANGELOG.md` et `docs/dev_diary.md` ;
- versioning SemVer ;
- workflow Git avec branches dédiées, PR et merge uniquement lorsque tests et contrôles sont au vert. fileciteturn0file0

## 16. Tests attendus

Les tests doivent couvrir au minimum :

- les objets de valeur ;
- `CardDefinition` ;
- `CardPrinting` ;
- `Set` ;
- les adapters Scryfall ;
- les règles d'idempotence ;
- les repositories in-memory ;
- les services de recherche et filtrage ;
- la façade publique.

## 17. Documentation attendue

La documentation doit fournir :

- une présentation claire du rôle de la librairie ;
- la différence entre `CardDefinition` et `CardPrinting` ;
- le rôle de `Set` ;
- le fonctionnement des imports ;
- les garanties d'idempotence ;
- des exemples d'usage ;
- les dépendances autorisées et interdites.

## 18. Critères d'acceptation

La librairie sera considérée conforme si :

1. elle distingue clairement `CardDefinition`, `CardPrinting` et `Set` ;
2. elle normalise correctement les payloads Scryfall ;
3. elle expose un modèle métier stable ;
4. elle permet des imports idempotents ;
5. elle propose une consultation riche du référentiel ;
6. elle respecte les contraintes communes de qualité et de développement ;
7. elle est réutilisable par les autres briques Baobab.

## 19. Critères de GO / NO GO v1.0.0

### GO si

- le vocabulaire métier public est stable ;
- les imports sont idempotents et testés ;
- les relations entre définitions, printings et sets sont fiables ;
- la consultation du référentiel est exploitable ;
- la documentation est suffisante ;
- les contrôles qualité et les tests sont au vert.

### NO GO si

- la librairie reste un simple miroir brut de Scryfall ;
- les stratégies d'identité ne sont pas stabilisées ;
- l'import produit des doublons incohérents ;
- le domaine dépend encore du format source ;
- la consultation métier est trop pauvre ;
- la qualité, les tests ou la documentation sont insuffisants.

