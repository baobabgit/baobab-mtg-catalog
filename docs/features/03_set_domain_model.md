# Feature 03 — Set domain model

## Branche

`feature/03-set-domain-model`

## Objectif

Modéliser l'entité métier `Set`.

## Périmètre

- entité `Set`
- `SetType` si nécessaire
- stratégie d'identité du set
- propriétés principales
- validations de cohérence

## Livrables attendus

- modèle métier `Set`
- types associés
- exceptions dédiées
- tests unitaires

## Critères d'acceptation

- le modèle représente un set métier et non le JSON brut Scryfall
- la stratégie d'identité est claire
- la recharge d'un set connu pourra être supportée sans ambiguïté

## Prompt pour l'IA de développement

```text
Tu développes la feature `03_set_domain_model` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/03-set-domain-model`

Objectif :
Créer le modèle métier `Set` représentant une édition/extension Magic.

Travaux à réaliser :
1. Créer l'entité métier `Set`.
2. Créer si nécessaire `SetType` et des objets de valeur associés.
3. Modéliser au minimum :
   - identifiant métier du set
   - code
   - nom
   - type
   - date de sortie
   - taille estimée si disponible
   - métadonnées utiles au domaine
4. Définir la stratégie d'identité du set.
5. Ajouter les validations métier nécessaires.
6. Écrire les tests unitaires complets.

Points d'attention :
- ne pas coupler l'entité au format brut Scryfall
- préparer le support des imports idempotents
- garder une API publique stable et lisible

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

