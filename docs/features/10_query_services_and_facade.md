# Feature 10 — Query services and facade

## Branche

`feature/10-query-services-and-facade`

## Objectif

Exposer une façade publique simple à consommer par les autres librairies Baobab.

## Périmètre

- services de consultation de haut niveau
- navigation entre `CardDefinition`, `CardPrinting` et `Set`
- façade publique
- API stable d'intégration

## Livrables attendus

- services d'accès de haut niveau
- `MtgCatalogFacade` ou équivalent
- tests unitaires et d'intégration internes

## Critères d'acceptation

- une autre librairie peut consommer le catalogue sans connaître l'architecture interne
- les cas d'usage d'intégration sont simples
- l'API publique est stable et lisible

## Prompt pour l'IA de développement

```text
Tu développes la feature `10_query_services_and_facade` de la librairie Python `baobab-mtg-catalog`.

Branche de travail obligatoire : `feature/10-query-services-and-facade`

Objectif :
Créer la façade publique de haut niveau de la librairie.

Travaux à réaliser :
1. Créer les services de consultation de haut niveau nécessaires.
2. Permettre les cas d'usage minimum :
   - récupérer une `CardDefinition`
   - récupérer un `CardPrinting`
   - récupérer un `Set`
   - naviguer d'une définition vers ses printings
   - naviguer d'un printing vers son set et sa définition
3. Créer une façade publique simple, par exemple `MtgCatalogFacade`.
4. Faire en sorte qu'une autre librairie puisse utiliser la façade sans connaître les détails internes.
5. Écrire les tests unitaires et d'intégration internes.

Workflow obligatoire de fin :
1. tests
2. qualité
3. PR
4. merge sur `main` si tout est vert
```

