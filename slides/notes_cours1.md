# Notes pour structurer la première séance du cours Big Data

* Durée : 2h (présentation + notebook / manipulations)
* Plan de la présentation
    * Généralités sur le cours, où trouver les supports, cloner le git, quels packages installer [10 minutes]
    * Comment sont codées les données ? [20 minutes]
        * montrer des exemples d'aberrations de calcul de flottants
        * calculer la taille en mémoire d'un tenseur `numpy`, float vs float64 (parler de `x.nbytes`, `x.dtype`, _etc._)
    * mémoire (RAM vs disque, notion de swap) [20 minutes]
        * illustration : demander de créer un tenseur numpy avec `arange` qui soit de taille trop grande pour leur RAM et voir ce qui se passe, demander de faire +1 dessus, observer l'occupation mémoire, demander de libérer la mémoire (`del x`), puis demander de créer un tenseur qui ce coup-ci soit de taille un peu plus petite et voir la différence
        * rapide vs permanent vs capacité
    * process / thread [20 minutes]
        * process ~ programme (pas exactement, mais...), ne partage pas sa mémoire avec les autres process
        * threads d'un même process partagent la mémoire (ex : répartition d'un calcul sur différents coeurs)
        * **TODO** : quelle illustration ?
    * processeur, coeur [20 minutes]
        * single/multi core : utiliser la métaphore du resto (thread = commande, core = cuisinier, resto = processeur)
        * notion de GPU
        * demander de regarder ce que eux ont
        * dans un notebook python, fournir un code qui profite bien du parallélisme (sleep) et jouer avec le nombre de threads vs nb de coeurs pour voir l'effet sur le temps de calcul
