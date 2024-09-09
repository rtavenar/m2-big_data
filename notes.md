# Discussion migration Eskemm data

* Focalisé sur le cours de Big Data avec dans l'idée la possibilité d'en profiter sur d'autres modules autour
* Besoins du cours de Big Data
    * Service
    * Authentification fédération d'identité
        * Exemples
            * https://jupytercloud.math.cnrs.fr/instances/
            * https://jupyterhub.ijclab.in2p3.fr/
    * Outils
        * JupyterHub avec Python+Dask
            * https://jupyter.org/hub
            * Possibilité de préparer une liste de paquets python nécessaires de notre côté
        * Accès ligne de commande (éventuellement dans l'interface JupyterLab)
        * Cluster Hadoop+Spark


# Notes de préparation du cours de _big data_ en M2

* Découpage du cours en séances : <https://docs.google.com/spreadsheets/d/1lSmKtL6B6NwOhqxt1XXEDzRb7gYjyvQ1dDxt6HOplgs/edit?usp=sharing>

## Notes de cours de Pierre Navaro

* https://pnavaro.github.io/big-data/intro.html
* voir avec Pierre
    * quel timing il avait
    * pourquoi il avait besoin de louer des serveurs OVH
    * des exemples de projets

## Sujets à aborder

* Intro : limites de ce qu'ils font habituellement
    * Notion de mémoire vive / disque
    * Notion de coeurs de calcul
* Outils
    * Dask
    * Hadoop
    * Spark
* Techniques
    * Map Reduce en général
    * Calcul parallèle
    * Calcul asynchrone
* Réduction de l'empreinte mémoire de pandas
    * https://pythonspeed.com/articles/pandas-load-less-data/
    * https://pythonspeed.com/articles/pandas-reduce-memory-lossy/
    * https://pythonspeed.com/articles/chunking-pandas/
* Formats de fichier ?
    * HDF5
    * Parquet

## Discussion avec Pierre

* Paralléliser avec Python
    * map reduce pour compter les mots dans un texte
    * de moins en moins nécessaire de faire les rappels non parallèles avec leur maîtrise de Python
        * itérateurs
    * Puis outils dédiés
        * python pur, dask, spark (important pour les stages, mais difficile en termes d'infrastructure)
            * spark : zeppelin (spark + Jupyter) avec VM dédiée
            * sinon spark dans RStudio ?
        * regarder dask tutorials (coiled)
    * dataframes de dask et spark
    * ML avec données volumineuses ???
        * RegLog en numpy vs en sklearn, parallélisation de la sélection de variables (eg garder 4 variables parmi 12)
    * Exemple d'exercice
        * Coder une classe genre liste avec toutes les opérations en parallèles
* Systèmes de fichiers distribués
    * Hadoop
        * installé sur serveur MAS, avec les machines des salles comme noeuds
        * nécessite de revenir sur les bases des commandes unix
    * Retour sur MongoDB ?
* Remarques misc
    * Commencer par des choses de base sur gestion des paquets / des environnements / du système, etc
    * Éval QCM moodle
    * Soucis d'assiduité
    * regarder cours de Spark à l'ENSAI (Smart Data)
    * joblib plutot que concurrent futures ?
        * En tout cas leur faire prendre conscience de quoi paralleliser, notamment en cas de boucles imbriquées, penser à ne paralléliser que la boucle extérieure

## À améliorer pour l'an prochain

* Avoir un serveur (voire cluster) accessible bien configuré pour les TP ligne de commande, Hadoop et spark
* Mieux gérer l'enchaînement des séances et l'imbrication avec les cours de ML & deep (ne pas aller trop vite)
* TP ligne de commande : insister + sur les entrés / sorties standard (+ d'exemples en Python notamment) pour mieux préparer Hadoop MapReduce via Streaming
* Résoudre le bug des caractères de fin de ligne au format Windows
* Faire un meilleur 3ème exo pour Hadoop mapreduce
* DaskML : regarder `chunks="auto"` pour voir si ce n'est pas toujours la meilleure option pour décider de la taille des chunks (cf. https://docs.dask.org/en/stable/generated/dask.array.from_array.html)