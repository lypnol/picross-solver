# Résolution du problème de Picross

## Fichiers présents

- main.py : script d'entrée python permettant de lancer la résolution des fichiers picross.
- picross_files/ : répertoire contenant plusieurs fichiers au format PICROSS
- Dimacs.py : classe python permettant de lire / écrire les fichiers au format Dimacs
- Picross.py : classe permettant de lire les fichiers au format PICROSS
- solver/ : répertoire contenant le code lié au SAT solveur
    - BaseSolver : interface à implémenter
    - PycoSatSolver : classe utilisant la librairie python pycosat.
    - Solver.py : contient la liste des solveurs
- model/ : Contient le code lié à la modélisation
    - BaseModel : interface à implémenter pour écrire une modélisation du problème
    - ModelSpots : modèle qui n'utilise pas de blocs (juste les cases, et des variables suplémentaires)
    - ModelIKJ : modèle qui utilise les blocs de cases consécutives.
    - Model.py : liste des modèles
- requirements.txt : librairies python nécessaires
- utils.py : diverses fonctions utiles (notamment pour mesurer le temps d'execution des fontions)


## Comment ça marche

Il faut installer les packages dans `requirements.txt`.
Ensuite, pour lancer une résolution, il faut lancer la commande suivante (ici sur un fichier picross de test) :

```
python3 main.py picross_files/test.PICROSS [-m spots / ikj]
```

L'option '-m spots / ikj' est pour choisir quelle modélisation sera utilisée pour résoudre le problème.
Par défaut, la modélisation ikj (qui a de meilleures performances) est utilisée.

Le résultat sera alors enregistré dans un fichier, a coté du fichier initial, sous le format .GRID


## Champion

Pour le moment, le champion est le lost-78-ikj-pycosat.GRID, qui est resolu en 2 minutes.

## Ajouter une modélisation ou un sat solveur

### Modélisation
Pour ajouter une modélisation il faut créer une sous-classe de `BaseModel` dans `model/`:

```python
from model.BaseModel import BaseModel

class MyAwesomeModel(BaseModel):
    @staticmethod
    def name():
        return 'awesome'

    @staticmethod
    @timed("MyAwesomeModel", "modelize")
    def modelize(n, line_blocks, col_blocks):
        # n est la taille de la grille
        # line_blocks sont les règles de remplissage sur les lignes
        # col_blocks sont les règles de remplissage sur les colonnes

        # il faut retourner le problème en format DIMACS:
        # un couple (n_var, clauses, index)
        # index est un index qui sera utilisé dans la reconstruction de la solution
        # en format grid

    @staticmethod
    def sat_solution_to_grid(n, n_var, solution, index):
        # transformer la solution retournée par le sat solveur en grille
        # les cases de la grille retournée sont 1 ou 0 (remplie ou non)

```

Il faut aussi l'enregistrer dans les fonction `all_models` et `get` dans `Model.py`.

### Sat Solveur
Pareil que les modélisation, il faut les ajouter dans `Solver.py`
Nous n'avons pas réalisé de SAT solver.