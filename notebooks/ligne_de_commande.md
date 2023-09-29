# Initiation aux commandes Unix

Dans cette séance, vous allez apprendre à utiliser une interface en ligne de commande pour exécuter des tâches simples.

On parlera ici de commandes Unix, par abus de langage.
Unix est en fait un système d'exploitation dans lequel la ligne de commande joue un grand rôle.

Pour cette séance, vous pourrez travailler dans un Terminal si vous disposez d'un système d'exploitation basé sur Unix (Linux ou MacOS, typiquement). Sinon, il vous est recommandé de créer un compte sur [la plateforme Deepnote](www.deepnote.com), et d'y créer un nouveau projet nommé `TP_ligne_de_commande`. Une fois ce nouveau projet ouvert, vous pourrez démarrer un Terminal (_cf._ bandeau de gauche) et travailler, à distance, sur un système de type Unix.

## 1. Principes de base

Une commande Unix a le format suivant :

```bash
nom_du_programme arg1 arg2 --nom_arg3 val_arg3
```

où `arg1`, `arg2`, et `--nom_arg3 val_arg3` sont des arguments passés en entrée au programme, un peu à la façon d'une fonction Python qui prendrait 3 arguments et que l'on appellerait via :

```python
f(arg1, arg2, nom_arg3=val_arg3)
```

On voit donc ici que la séparation entre les différents arguments passés en entrée d'un programme se fait à chaque espace. Si on souhaite insérer un espace dans la valeur d'un argument lors de l'appel, il faudra donc entourer cette valeur par des guillemets :

```bash
nom_du_programme arg1 "arg2 avec des espaces dedans"
```

**Question 1.1.** Créez, avec votre navigateur de fichier préféré, un dossier dans vos documents dédié à la séance de ce jour. Démarrez un terminal. Sachant que l'utilitaire `cd` permet de changer le dossier de travail du terminal, et qu'il prend comme unique argument le chemin (relatif ou absolu) vers le nouveau dossier de travail, quelle commande faut-il entrer pour vous placer dans le dossier nouvellement créé ?

```bash
cd "./chemin vers/mon_dossier/de travail"
```

**Question 1.2.** Dans les deux commandes suivantes, quel est le nom du programme exécuté, et quels sont les arguments qui lui sont passés en entrée ?

```bash
wget https://raw.githubusercontent.com/rtavenar/m2-big_data/main/notebooks/data/unix/unix.zip unix_data.zip
unzip unix_data.zip
chmod ugo+x lire_args.py
```

**TODO:** `wget` d'une archive des fichiers nécessaires suivi d'un `unzip`

**Question 1.3.** Exécutez les commandes précédentes l'une après l'autre et vérifiez que de nouveaux fichiers et dossiers ont été téléchargés puis décompressés (c'est le sens respectif des commandes `wget` et `unzip`). **TODO:** ajouter `chmod` ou les droits persistent dans le zip ?

**Question 1.4.** Exécutez le script Python `./lire_args.py` en lui passant les arguments de votre choix (quel que soit leur sens, il s'agit d'un exemple jouet). Quelle sortie obtenez-vous ?

```
./lire_args.py truc machin --nom_chose chose
Nom du programme : ./lire_args.py
Valeur de l'argument : truc
Valeur de l'argument : machin
Nom de l'argument : --nom_chose
Valeur de l'argument : chose
```

**Question 1.5.** Répétez l'opération précédente en lui passant `data/*.csv` comme un des arguments. Qu'observez-vous ?

## 2. Système de fichiers Unix

Le système de fichiers Unix possède plusieurs caractéristiques importantes. Toutes les données dans Unix sont organisées sous forme de fichiers. Tous les fichiers sont regroupés dans des dossiers. Ces dossiers sont organisés dans une structure arborescente appelée système de fichiers, comme vous y êtes habitués dans d'autres sytèmes de fichiers.

En haut de la hiérarchie du système de fichiers Unix se trouve un répertoire appelé "racine", représenté par `/`. Tous les autres fichiers sont des "descendants" de la racine.
Dans la plupart des OS qui utilisent cette structure pour leur système de fichiers, un dossier spécifique est créé pour chaque utilisateur et il est désigné par le raccourci `~/` (`~/` pointe donc toujours vers le le dossier "home" de l'utilisateur courant, qui correspond souvent au chemin `/home/nom_d_utilisateur/`, ou `/Users/nom_d_utilisateur/` sous macOS).

À n'importe quel niveau de la hiérarchie, le dossier `.` représente le dossier courant et `..` son dossier parent dans la hiérarchie des dossiers.

Les commandes importantes pour naviguer dans un système de fichiers Unix sont les suivantes :

* [`pwd`](https://www.gnu.org/software/coreutils/manual/html_node/pwd-invocation.html) : obtenir le chemin vers le dossier courant
* [`ls`](https://www.gnu.org/software/coreutils/manual/html_node/ls-invocation.html) : lister les dossiers et fichiers
* `cd` : changer le dossier courant
* [`mkdir`](https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html) : créer un répertoire
* [`cp`](https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html) : copier un fichier ou dossier
* [`mv`](https://www.gnu.org/software/coreutils/manual/html_node/mv-invocation.html) : déplacer un fichier ou dossier
* [`rm`](https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html) : supprimer un fichier

**Question 2.1.** Utilisez la commande `whoami` pour connaître le nom de l'utilisateur courant. Vérifiez qu'un dossier `/home/nom_d_utilisateur/` (ou `/Users/nom_d_utilisateur/` si vous êtes sous macOS) existe bien.

```
% whoami
rtavenar
% ls /home/rtavenar
ls: /home/rtavenar: No such file or directory
% ls /Users/rtavenar
```

**Question 2.2.** Créez un sous-dossier `data/` dans le dossier courant et déplacez-y tous les fichiers dont l'extension est `.txt` ou `.csv` du dossier courant.

```bash
mkdir data
mv *.csv *.txt data/
```

Sous Unix, les fichiers ont des permissions, c'est-à-dire que chaque utilisateur a le droit ou non d'interagir avec eux.
Il existe trois types de permissions :
* permission de lecture, notée `"r"`
* permission d'écriture (ou de modification), notée `"w"`
* permission d'exécution, notée `"x"`

De plus, ces permissions peuvent être accordées à l'utilisateur qui détient ces fichiers (`"user"`), au groupe auquel il est associé (`"group"`) ou à tous les utilisateurs du système.

Si on liste les fichiers du dossier courant avec `ls -al`, on a des informations sur les droits associés aux différents fichiers :

```bash
% ls -al
total 8
drwxr-xr-x@ 3 rtavenar  staff   96 29 sep 10:02 .
drwxr-xr-x@ 6 rtavenar  staff  192 29 sep 10:02 ..
-rwxr--r--@ 1 rtavenar  staff  373 29 sep 09:40 lire_args.py
```

On voit ci-dessus que le fichier `lire_args.py` appartient à l'utilisateur `rtavenar`, du groupe `staff`, et la liste des droits accordés est la suivante : `-rwxr--r--`.
Si l'on décortique cette chaîne de caractères, on obtient :
* le premier caractère `-` sert à indiquer s'il d'agit d'un fichier (`-`) ou d'un dossier (`d`) ;
* les trois caractères suivants correspondent aux droits de l'utilisateur propriétaire du fichier (`rtavenar` ici) ;
* les trois caractères suivants correspondent aux droits du groupe propriétaire du fichier (`staff` ici) ;
* les trois derniers caractères correspondent aux droits des autres utilisateurs.

L'utilitaire `chmod` permet de modifier les droits d'un utilisateur sur un ou plusieurs fichiers.
Prenons quelques exemples pour comprendre son usage :
* Ajout (`+`) du droit de lecture (`r`) pour l'utilisateur (`u`) propriétaire du fichier :
    ```bash
    chmod u+r mon_fichier
    ```
* Suppression (`-`) du droit de lecture (`r`) pour l'utilisateur (`u`) propriétaire du fichier :
    ```bash
    chmod u+r mon_fichier
    ```
* Ajout (`+`) du droit d'écriture (`w`) pour le groupe (`g`) propriétaire du fichier :
    ```bash
    chmod g+w mon_fichier
    ```
* Ajout (`+`) du droit d'écriture (`w`) pour les autres utilisateurs (_other_, ou `o`) :
    ```bash
    chmod o+w mon_fichier
    ```
* Ajout (`-`) du droit de lecture (`r`) pour tous les utilisateurs (`ugo`) :
    ```bash
    chmod ugo+r mon_fichier
    ```

**Question 2.3.** Quels sont les droits accordés à votre utilisateur sur les fichiers `.txt` que vous avez déplacés dans le sous-dossier `data/` ? Vérifiez que vous êtes bien propriétaire de ces fichiers.

**Question 2.4.** Que signifie la commande `chmod ugo+x lire_args.py` que l'on vous a demandé d'exécuter à la question 1.3 ? Pourquoi était-ce nécessaire ?

Dans les deux dernières questions de la section 1., vous avez spécifié expressément le chemin du script / programme à exécuter. 
Lorsque vous ne spécifiez pas cette information, le _shell_ (le système qui permet d'exécuter les commandes dans votre terminal) va chercher si le programme que vous souhaitez exécuter existe dans l'un de dossiers enregistrés comme pouvant contenir des programmes du systèmes.

Cette liste de dossiers est contenue dans une variable d'environnement nommée `$PATH`.

**Question 2.5.** Sachant que la commande `echo` permet d'afficher le contenu d'une variable d'environnement, utilisez-le pour voir le contenu de votre `$PATH`. Que signifie le caractère `:` dans l'affichage que vous obtenez ?

```bash
echo $PATH
/Users/rtavenar/py3.10_ml/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Library/TeX/texbin:/opt/homebrew/opt/ruby/bin:/opt/homebrew/bin:/Users/rtavenar/py3.10_ml/bin:/Users/rtavenar/.rvm/bin
```

**Question 2.6.** Le dossier courant (`.`) est-il inclus dans votre `$PATH` ? 
Confirmer / infirmer en essayant d'exécuter le programme `lire_args.py` du dossier courant sans préciser son chemin relatif.


**Trucs & Astuces**

La commande `which` permet de connaître le chemin complet vers le programme visé, par exemple :

```bash
which python
/Users/rtavenar/py3.10_ml/bin/python
```

Indique que, lorsque l'on entre la commande `python` dans le terminal, c'est le programme `/Users/rtavenar/py3.10_ml/bin/python` qui sera exécuté.

Autre astuce qui peut s'avérer utile, on peut, dans le terminal, déclencher la complétion automatique en utilisant la touche `<TAB>`. Cela peut permettre de compléter un nom de programme (situé dans l'un des dossiers du `$PATH`), ou un nom de fichier (tant que le chemin indiqué, relatif ou absolu, est correct).


## 3. Premières commandes

Dans le monde des lignes de commandes, un grand nombre de logiciels libres (dont ceux présentés à la section précédente pour interagir avec un système de fichiers) sont proposés par la _Free Software Foundation_ à travers le projet GNU. Ces logiciels sont intégrés par défaut dans la plupart des systèmes Linux (on parle même parfois de distributions GNU/Linux) ou macOS.

Dans cette section, nous allons notamment nous concentrer sur les logiciels qui permettent de manipuler simplement des fichiers textuels.

La première chose que l'on peut vouloir faire lorsqu'on a un fichier textuel à disposition est de le lire.
C'est ce que permet [le programme `cat`](https://www.gnu.org/software/coreutils/manual/html_node/cat-invocation.html).

Parfois, les fichiers sont trop volumineux et les afficher entièrement dans le terminal ne permet pas d'y voir très clair, on peut alors utiliser [`head`](https://www.gnu.org/software/coreutils/manual/html_node/head-invocation.html) pour n'afficher que les premières lignes ou [`tail`](https://www.gnu.org/software/coreutils/manual/html_node/tail-invocation.html) si l'on ne souhaite afficher que la fin du fichier.

On peut également souhaiter trouver les occurrences d'une chaîne de caractères ou d'une expression régulière dans un (ou plusieurs) fichier(s). Cela se fait en utilisant l'outil [`grep`](https://www.gnu.org/software/grep/manual/grep.html#Invoking-grep).

[`wc`](https://www.gnu.org/software/coreutils/manual/html_node/wc-invocation.html) est un autre utilitaire bien pratique qui permet de compter le nombre de lignes, de caractères, ou de mots d'un fichier texte.

**Question 3.1.** Quels sont les champs (en-tête de colonnes) des fichiers `M1_2022-2023.csv` et `M2_2023-2024.csv` ?

```bash
head -n 1 M1_2022-2023.csv
head -n 1 M2_2023-2024.csv
```

**Question 3.2.** Combien de lignes contiennent respectivement ces fichiers ?

```bash
wc -l M1_2022-2023.csv
wc -l M2_2023-2024.csv
```

**Question 3.3.** Affichez toutes les lignes débutant par un numéro étudiant de la forme `221`.

```bash
grep "^221" *.csv
```

**Question 3.4.** Listez les étudiants qui n'étaient pas en M1 en 2022-2023 et qui sont en M2 en 2023-2024 et, respectivement, ceux qui étaient en M1 en 2022-2023 et qui sont pas en M2 en 2023-2024.

```bash
diff M1_2022-2023.csv M2_2023-2024.csv
```

## 4. Enchaînement de commandes

Les programmes, lorsqu'ils s'exécutent, produisent une sortie sous forme textuelle, qui est affichée dans le terminal.
Cette sortie correspond en fait au contenu de deux canaux : `stdout` stocke la "sortie standard" alors que `stderr` stocke l'"erreur standard", c'est-à-dire les affichages liés à des erreurs dans le programme.

Ces deux flux sont traités comme des fichiers dans lesquels les programmes écrivent au fur et à mesure de leur exécution et dont les contenus sont affichés en quasi-temps réel dans le terminal.

Il est possible de rediriger la sortie standard d'un programme pour que, au lieu de s'écrire dans un terminal, soit elle s'écrive dans un fichier texte, soit elle serve d'entrée à un autre programme :
```bash
# Écriture dans un fichier texte
nom_du_programme arg1 arg2 > fichier_sortie.txt

# Redirection de la sortie vers l'entrée
# d'un autre programme
nom_du_programme arg1 arg2 | autre_programme
```

**Question 4.1.** Afficher uniquement la ligne 10 du fichier `M1_2022-2023.csv`.

```bash
head -n 10 M1_2022-2023.csv | tail -n 1
```

**Question 4.2.** Comptez le nombre de lignes des fichiers `M1_2022-2023.csv` et `M2_2023-2024.csv` débutant par un numéro étudiant de la forme `221`.

```bash
grep "^221" *.csv | wc -l
```

**Question 4.3.** Même question en supprimant les doublons. (jetez un oeil aux documentations de `sort` et `uniq`)
