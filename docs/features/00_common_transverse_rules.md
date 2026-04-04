# Règles transverses communes

À inclure ou rappeler dans chaque développement de feature.

```text
Règles transverses obligatoires :
- ne jamais casser l'API publique déjà en place sans justification
- ne pas introduire de dépendance inutile
- garder le domaine découplé de Scryfall hors couche d'adaptation
- toute erreur métier spécifique doit avoir une exception spécifique
- toute nouvelle classe doit avoir son test dédié
- mettre à jour `docs/dev_diary.md`
- utiliser des commits Conventional Commits
- si une décision d'architecture est prise, la documenter dans le code et/ou dans la documentation de développement

En fin de feature, produire un court récapitulatif de :
- ce qui a été développé
- les fichiers créés/modifiés
- les tests ajoutés
- les commandes exécutées
- le résultat des contrôles qualité
```

