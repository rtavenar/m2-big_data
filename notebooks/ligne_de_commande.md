# Initiation à la ligne de commande

Dans cette séance, vous allez apprendre à utiliser une interface en ligne de commande pour exécuter des tâches simples.

Pour cette séance, vous pourrez travailler dans un Terminal si vous disposez d'un système d'exploitation basé sur Unix (Linux ou MacOS, typiquement). Sinon, il vous est recommandé de créer un compte sur la plateforme Deepnote, et d'y créer un nouveau projet nommé `TP_ligne_de_commande`. Une fois ce nouveau projet ouvert, vous pourrez démarrer un Terminal (_cf._ bandeau de gauche) et travailler, à distance, sur un système Unix.

**TODO :** ne laisser que des exercices de base dans les sections, tous les exos qui demandent un peu de "réflexion" se trouvant reportés à la fin, pour les forcer à revenir sur ce qui a été présenté dans les différentes partiers et se l'approprier

## Principes de base

* Format des commandes (`nomduprog arg1 arg2 --nom_arg val_arg`)
    * Donner une commande qui fait `wget` puis `unzip` et dire "on présentera ces commandes plus tard mais pour l'instant, quels sont les arguments" ?
    * vérifier par exemple que l'on peut accéder à ces arguments en Python
    * regarder ce qui se passe lorsqu'on utilise un wildcard dans un des arguments
* Gestion des espaces, échappement de caractères
* Astuce : utilisation de la touche `<TAB>` pour compléter des noms de fichier, d'utilitaire, etc.


## Premières commandes

* Fichiers texte : `cat`, `head`, `tail`, `wc`, `diff`, `grep`
* insister sur la lecture des man pages, ou au moins du `--help` (`man` n'existe pas sur deepnote)
* Fichiers distants / serveurs distants : `ssh`, `scp`, `wget` 
    * présenter rapidement (à part `wget`) car on n'aura pas de serveurs distants avec des credentials prêts pour eux
* Exercice : Télécharger 2 fichiers mis à disposition sur GitHub (genre liste d'étudiants extraite de CURSUS ou ce genre de choses ?), vérifier que les fichiers ont bien été enregistrés dans le dossier courant, comptez leurs nombres de lignes et rechercher dans ces fichiers toutes les lignes qui contiennent le mot `XXX`

## Système de fichiers Unix

* arborescence Unix (notion de `/`, de `~/`)
    * et chemins absolus / relatifs (avec `.` et `..`)
* `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm`, `rmdir`
* permissions, `whoami`

## Enchaînement de commandes

* Notions de `stdin`, `stdout`, `stderr`
* Pipe, redirections d'entrées/sorties, utilisation du résultat textuel d'une commande dans une autre commande (utilisation de ` `` `) etc.
*  Exercice : afficher uniquement la ligne 10 d'un des fichiers téléchargés à la section précédente
* Exercice : reprendre la question de l'exercice précédent mais en comptant cette fois ci le nombre de lignes qui contiennent le mot `XXX`

## Notions "avancées"

* Variables d'environnement (et `echo`, `export` ?)
    * Parler de comment on récupère une variable d'environnement en Python par exemple ?
* `which`
