# Résolution du problème de Picross

## Comment ça marche

Il faut installer les packages dans `requirements.txt` et lancer sur le fichier de test:
```
python3 main.py test.PICROSS
```

## Ajouter une modélisation ou un sat solveur

### Modélisation
Pour ajouter une modélisation il faut créer une sous-classe de `Model` dans `Model.py`:

```python
class MyAwesomeModel(Model):
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
        # un couple (n_var, clauses)

    @staticmethod
    def sat_solution_to_grid(n, n_var, solution):
        # transformer la solution retournée par le sat solveur en grille
        # les cases de la grille retournée sont 1 ou 0 (remplie ou non)

```

Il faut aussi l'enregistrer dans la fonction `all_models` de la classe `Model`. 

### Sat Solveur
Pareil que les modélisation, il faut les ajouter dans `Solver.py`
