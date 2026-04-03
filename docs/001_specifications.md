# Cahier des charges — `baobab-mtg-catalog`

## 1. Présentation générale

### 1.1 Nom du projet

* **Nom du repository** : `baobab-mtg-catalog`
* **Nom du package Python** : `baobab_mtg_catalog`

### 1.2 Finalité

La librairie `baobab-mtg-catalog` a pour objectif de fournir une **représentation métier, claire, stable et réutilisable du catalogue Magic: The Gathering**, indépendante de l’API source et exploitable par d’autres briques Baobab.

Elle doit permettre de manipuler de manière cohérente :

* les **cartes** ;
* les **printings** ;
* les **sets** ;
* les **données enrichies issues de Scryfall** mais transformées pour le domaine métier.

Cette librairie constitue une **brique cœur du domaine MTG**, destinée à être réutilisée par d’autres composants, notamment les briques de collecte, de deckbuilding, de collection, d’analyse ou de recherche.

---

## 2. Vision produit

`baobab-mtg-catalog` ne doit pas être une simple copie des objets Scryfall.

Elle doit jouer le rôle de **couche d’anticorruption métier** entre :

* les données externes Scryfall ;
* les besoins fonctionnels des projets Baobab autour de Magic.

L’objectif est donc de :

* **normaliser** la donnée ;
* **stabiliser** la représentation métier ;
* **masquer** les variations du fournisseur externe ;
* **exposer** un modèle orienté domaine ;
* **préparer** les usages futurs sans coupler les autres projets au schéma brut Scryfall.

---

## 3. Objectifs

## 3.1 Objectifs fonctionnels

La librairie doit permettre :

* de représenter une **carte métier** ;
* de représenter ses différents **printings** ;
* de représenter un **set** ;
* d’associer correctement cartes, printings et sets ;
* d’ingérer des données Scryfall brutes ;
* de transformer ces données en objets métier cohérents ;
* de proposer des services de consultation du catalogue ;
* de fournir des enrichissements utiles au domaine Baobab.

## 3.2 Objectifs techniques

La librairie doit :

* être **réutilisable** comme dépendance Python ;
* être **découplée** des appels HTTP ;
* pouvoir fonctionner à partir de données déjà récupérées ;
* être **testable unitairement** ;
* respecter les **contraintes de qualité communes** ;
* être prête à évoluer vers une v1.0.0 stable.

---

## 4. Périmètre fonctionnel

Le périmètre de `baobab-mtg-catalog` couvre les domaines suivants :

### 4.1 Représentation des cartes

La librairie doit permettre de représenter une carte Magic au niveau métier.

Une carte doit au minimum pouvoir porter les informations suivantes :

* identifiant logique stable de carte ;
* identifiant Oracle lorsque disponible ;
* nom principal ;
* noms alternatifs éventuels ;
* texte de règle ;
* coût de mana ;
* valeur de mana ;
* identité couleur ;
* couleurs ;
* type line ;
* supertypes, types, sous-types ;
* mots-clés ;
* statut légendaire si applicable ;
* informations liées aux faces pour les cartes multifaces ;
* informations utiles au domaine Baobab.

### 4.2 Représentation des printings

Un printing représente une **édition concrète** d’une carte dans un set donné.

Un printing doit pouvoir inclure au minimum :

* identifiant propre du printing ;
* référence vers la carte métier ;
* référence vers le set ;
* code de set ;
* numéro de collection ;
* rareté ;
* langue ;
* date de sortie si disponible ;
* finitions disponibles ;
* statut promo si applicable ;
* statut digital ou papier ;
* disponibilité image ;
* variations utiles à la collection ou à la recherche.

### 4.3 Représentation des sets

Un set doit pouvoir contenir :

* identifiant du set ;
* code court ;
* nom ;
* type de set ;
* date de sortie ;
* nombre de cartes ;
* informations parent/enfant si le modèle source le permet ;
* statut digital ;
* autres métadonnées utiles.

### 4.4 Relations entre les objets

La librairie doit garantir les relations suivantes :

* une **carte** peut avoir plusieurs **printings** ;
* un **printing** appartient à un **set** ;
* un **set** regroupe plusieurs **printings** ;
* les cartes multifaces ou variantes doivent être représentées sans ambiguïté.

### 4.5 Enrichissement métier des données Scryfall

La librairie doit enrichir la donnée source afin de produire des éléments métier plus facilement exploitables.

Exemples d’enrichissements attendus :

* normalisation des types ;
* extraction claire des sous-types ;
* représentation propre des couleurs et de l’identité couleur ;
* représentation métier des faces ;
* regroupement logique des printings d’une même carte ;
* indicateurs utiles pour la recherche, le deckbuilding ou la collection ;
* normalisation des raretés ;
* normalisation des langues ;
* représentation cohérente des finitions ;
* exposition d’objets métier plus simples que le JSON source.

---

## 5. Hors périmètre

La librairie ne doit pas, dans son périmètre initial, prendre en charge :

* les appels HTTP vers Scryfall ;
* la persistance en base de données ;
* la gestion des collections utilisateurs ;
* la gestion des decks ;
* la gestion des prix temps réel ;
* les images binaires ;
* l’interface web ;
* la synchronisation distante.

Ces sujets pourront être couverts par d’autres librairies Baobab ou par des évolutions futures.

---

## 6. Cas d’usage principaux

La librairie doit couvrir au minimum les usages suivants :

### 6.1 Ingestion

* transformer un payload Scryfall brut en objet métier `Card` ;
* transformer un payload Scryfall brut en objet métier `Printing` ;
* transformer un payload Scryfall brut en objet métier `Set` ;
* transformer des collections de payloads en catalogue exploitable.

### 6.2 Consultation

* récupérer une carte par identifiant ;
* récupérer un printing par identifiant ;
* récupérer un set par code ou identifiant ;
* lister les printings d’une carte ;
* lister les cartes ou printings d’un set ;
* filtrer selon certains critères simples.

### 6.3 Navigation métier

* naviguer d’une carte vers ses printings ;
* naviguer d’un printing vers son set ;
* naviguer d’un set vers ses cartes ou printings ;
* exploiter les enrichissements de domaine sans connaître le format brut Scryfall.

### 6.4 Intégration

* être utilisée par une autre librairie Baobab à partir d’objets Python ou de dictionnaires ;
* permettre l’ajout futur d’autres fournisseurs de données sans casser le modèle métier.

---

## 7. Architecture attendue

L’architecture doit suivre la logique modulaire déjà utilisée dans les autres projets Baobab : **modèle métier + interfaces + adapters + services/facades**.

## 7.1 Principes

* séparation claire entre **domaine** et **source externe** ;
* dépendances orientées vers les abstractions ;
* objets métier stables ;
* adapters de transformation isolés ;
* services de consultation distincts des modèles ;
* exceptions spécifiques au projet.

## 7.2 Proposition de structure

```text
src/baobab_mtg_catalog/
├── adapters/
│   ├── scryfall/
│   │   ├── card_adapter.py
│   │   ├── printing_adapter.py
│   │   └── set_adapter.py
├── domain/
│   ├── cards/
│   │   ├── card.py
│   │   ├── card_face.py
│   │   └── card_identifier.py
│   ├── printings/
│   │   ├── printing.py
│   │   ├── rarity.py
│   │   └── finish.py
│   ├── sets/
│   │   ├── set.py
│   │   └── set_type.py
│   └── shared/
│       ├── color.py
│       ├── color_identity.py
│       └── language.py
├── services/
│   ├── catalog_service.py
│   ├── card_query_service.py
│   ├── printing_query_service.py
│   └── set_query_service.py
├── repositories/
│   ├── interfaces/
│   │   ├── card_repository.py
│   │   ├── printing_repository.py
│   │   └── set_repository.py
│   └── in_memory/
│       ├── in_memory_card_repository.py
│       ├── in_memory_printing_repository.py
│       └── in_memory_set_repository.py
├── facades/
│   └── mtg_catalog_facade.py
├── exceptions/
│   ├── baobab_mtg_catalog_exception.py
│   ├── mapping_exception.py
│   ├── card_not_found_exception.py
│   ├── printing_not_found_exception.py
│   ├── set_not_found_exception.py
│   └── invalid_payload_exception.py
└── builders/
    └── catalog_builder.py
```

Cette structure devra respecter les contraintes communes : code sous `src/`, tests miroir, une classe par fichier, organisation claire, conventions PEP 8, typage, docstrings et exceptions spécifiques. 

---

## 8. Modèle métier attendu

## 8.1 Entités principales

### Card

Représente le concept métier de carte indépendamment de ses éditions.

### Printing

Représente une impression concrète d’une carte dans un set donné.

### Set

Représente une édition / extension.

## 8.2 Objets de valeur possibles

La librairie pourra introduire, selon besoin :

* `Color`
* `ColorIdentity`
* `ManaCost`
* `Rarity`
* `Language`
* `Finish`
* `SetCode`
* `CollectorNumber`

## 8.3 Identifiants

La stratégie d’identification doit être explicite.

Exemple attendu :

* `oracle_id` pour le regroupement logique de carte ;
* `scryfall_id` pour le printing ;
* `set_code` ou identifiant interne pour le set ;
* identifiants métier dédiés si nécessaire.

---

## 9. Services attendus

La librairie doit exposer des services simples et lisibles.

### Exemples de services attendus

* construire un catalogue à partir de données sources ;
* retrouver une carte ;
* retrouver un printing ;
* retrouver un set ;
* lister les printings d’une carte ;
* lister les printings d’un set ;
* appliquer des filtres simples ;
* exposer une façade de haut niveau pour les consommateurs.

La façade devra être pensée pour être facilement utilisée par une autre librairie Baobab sans lui imposer la connaissance du modèle interne.

---

## 10. Gestion de l’ingestion Scryfall

## 10.1 Principe

La librairie doit accepter des données Scryfall brutes déjà récupérées ailleurs.

Elle ne doit pas dépendre, dans son cœur métier, d’un client HTTP concret.

## 10.2 Adapters

Des adapters dédiés devront :

* valider le payload minimal attendu ;
* mapper le payload vers les objets métier ;
* lever des exceptions spécifiques en cas d’incohérence ;
* isoler totalement la logique de mapping.

## 10.3 Robustesse

Le mapping doit gérer :

* champs absents ;
* champs optionnels ;
* cartes multifaces ;
* cas particuliers de langues ;
* variations d’éditions ;
* cartes non standards ;
* payloads partiels ou invalides.

---

## 11. Exigences non fonctionnelles

## 11.1 Qualité

Le projet doit être maintenable, testé, lisible et strictement typé.

## 11.2 Performance

Pour la v1, l’objectif principal est la clarté et la fiabilité, pas l’optimisation extrême.
La bibliothèque devra néanmoins pouvoir manipuler des volumes raisonnables de données catalogue sans comportement aberrant.

## 11.3 Extensibilité

L’architecture doit permettre :

* l’ajout d’un autre fournisseur que Scryfall ;
* l’ajout de nouveaux enrichissements métier ;
* l’ajout futur d’une persistance ;
* l’ajout de critères de recherche plus riches.

## 11.4 Stabilité d’API

Les objets et services publics devront être pensés pour rester stables en v1.x.

---

## 12. Règles de développement

Les règles de développement sont les mêmes que pour tes autres librairies Python Baobab. Elles incluent notamment :

* code sous `src/nom_du_projet` ;
* tests sous `tests/` avec arborescence miroir ;
* une classe par fichier ;
* docstrings sur les éléments publics ;
* annotations de type obligatoires ;
* base d’exceptions dédiée au projet ;
* exceptions spécifiques par domaine ;
* couverture cible minimale de 90 % ;
* configuration centralisée dans `pyproject.toml` ;
* qualité validée par `black`, `pylint`, `mypy`, `flake8`, `bandit` ;
* `README.md`, `CHANGELOG.md` et `docs/dev_diary.md` obligatoires ;
* versioning SemVer ;
* workflow Git avec branches dédiées et Pull Request. 

---

## 13. Tests attendus

## 13.1 Tests unitaires

Ils doivent couvrir au minimum :

* les entités métier ;
* les objets de valeur ;
* les adapters Scryfall ;
* les services de consultation ;
* les repositories in-memory ;
* les exceptions.

## 13.2 Tests d’intégration internes

Ils doivent vérifier :

* qu’un ensemble de payloads Scryfall peut être converti en catalogue exploitable ;
* que les relations carte / printing / set sont correctement construites ;
* que les cas multifaces et cas limites sont correctement gérés.

## 13.3 Couverture

Le projet doit atteindre le seuil défini par les contraintes communes, soit **90 % minimum**. 

---

## 14. Documentation attendue

La documentation devra contenir au minimum :

* un `README.md` expliquant le rôle de la librairie ;
* un exemple d’ingestion d’un payload Scryfall ;
* un exemple de navigation carte / printing / set ;
* un exemple d’utilisation de la façade ;
* un `CHANGELOG.md` ;
* un `docs/dev_diary.md` ;
* une documentation des choix métier importants.

---

## 15. Livrables attendus

La v1 de développement doit livrer :

* l’arborescence complète du projet ;
* les modèles métier principaux ;
* les adapters Scryfall ;
* les repositories in-memory ;
* les services de requête ;
* la façade publique ;
* les exceptions spécifiques ;
* les tests ;
* la configuration `pyproject.toml` ;
* le `README.md` ;
* le `CHANGELOG.md` ;
* le journal de développement.

---

## 16. Critères d’acceptation

La librairie sera considérée conforme si :

1. elle représente correctement **cartes**, **printings** et **sets** ;
2. elle transforme des payloads Scryfall en objets métier stables ;
3. elle expose une API Python claire et réutilisable ;
4. elle isole le fournisseur externe du reste du domaine ;
5. elle respecte les contraintes communes de qualité, de tests, de typage, de documentation et de workflow ; 
6. elle est packagée proprement et installable ;
7. elle dispose d’un socle suffisant pour une évolution en v1.x.

---

## 17. Critères de GO / NO GO v1.0.0

### GO si

* le modèle métier public est cohérent et stable ;
* les mappings Scryfall sont couverts ;
* les cas nominaux et cas limites principaux sont testés ;
* la qualité outillée est au vert ;
* la documentation d’usage est suffisante ;
* la librairie est installable et exploitable par une autre brique.

### NO GO si

* la librairie n’est qu’un miroir brut de Scryfall ;
* les relations métier ne sont pas fiables ;
* les adapters mélangent logique source et logique domaine ;
* les exceptions ne sont pas spécifiques ;
* la couverture ou les contrôles qualité ne sont pas atteints ;
* l’API publique reste floue ou instable.

---

## 18. Feuille de route fonctionnelle recommandée

### Lot 1 — Bootstrap projet

* structure du package ;
* outillage qualité ;
* exceptions de base ;
* documentation initiale.

### Lot 2 — Modèle métier

* cartes ;
* printings ;
* sets ;
* objets de valeur communs.

### Lot 3 — Mapping Scryfall

* adapters ;
* validation des payloads ;
* gestion des cas spéciaux.

### Lot 4 — Services catalogue

* construction du catalogue ;
* services de recherche ;
* façade publique.

### Lot 5 — Stabilisation

* enrichissements métier ;
* durcissement des tests ;
* documentation ;
* préparation v1.0.0.

---

## 19. Positionnement dans l’écosystème Baobab

`baobab-mtg-catalog` doit devenir la **référence métier catalogue MTG** dans l’écosystème Baobab.

Le rôle attendu est le suivant :

* `baobab-scryfall-api-caller` récupère la donnée ;
* `baobab-mtg-catalog` la transforme en domaine exploitable ;
* d’autres librairies, comme celles de collection, d’analyse ou de deckbuilding, consomment ensuite ce modèle stable.

---

## 20. Résumé de la cible

La cible n’est pas une simple librairie technique de mapping JSON.

La cible est une **librairie métier de catalogue MTG**, stable, typed, testée, documentée, réutilisable, capable de représenter clairement le monde Magic et d’enrichir la donnée Scryfall pour les besoins réels de l’écosystème Baobab.

Étape suivante naturelle : le découpage de ce cahier des charges en **features détaillées**, chacune avec son **prompt pour l’IA de développement** et une **branche dédiée**.
