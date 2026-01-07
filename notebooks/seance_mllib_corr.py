# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3
#     name: python3
# ---

# + [markdown] id="RLBXihMoLBuM"
# # Prise en main de Spark MLlib
#
# Dans ce TD vous allez utiliser les modules `pyspark.pandas` (pandas-on-spark) et `pyspark.ml` (MLlib) pour manipuler et traiter des données issue d'une enquête de *speed dating* contenues dans le fichier `SpeedDating.csv`.
#
# Des données ont été récoltées auprès de participant.e.s à des sessions de *speed dating* avant, pendant et après leurs rencontres avec plusieurs autres participant.e.s (de sexe opposé uniquement). La description (en anglais) des données récoltées est disponible dans le fichier `Speed Dating Data Key.pdf`. Chaque ligne de ce fichier fournit les données d'un.e des participant.e.s pour une de ses rencontres, ainsi que quelques données relatives à la personne rencontrée (mais ces données sont incomplètes).
#
# Le but est d'essayer de prédire un "match" entre deux personnes qui se rencontrent en utilisant uniquement les données récoltées avant la rencontre. Il y a "match" lorsque les deux personnes qui se rencontrent donnent une décision positive à l'issue de la rencontre.
#
# ## Initialisation de la `SparkSession` et lecture des données

# + [markdown] id="UHCXHhUiLzfc"
# **Question 0**
#
# Téléchargez le fichier <https://github.com/rtavenar/ml-datasets/releases/download/SpeedDating/SpeedDating.csv> avec l'utilitaire de ligne de commande adapté et ajoutez ce fichier dans un nouveau dossier `/user/VOTRE_PRENOM/tp_mllib` sur le HDFS.

# + [markdown] id="UHCXHhUiLzfc"
# **Question 1**
#
# Initialiser une `SparkSession` pour une application nommée "Prise en main de MLlib" se connectant au YARN du cluster.

# + id="qRcLyRAJMqgI"
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Prise en main de MLlib").master("yarn").getOrCreate()

# + [markdown] id="nyYy6pPjL167"
# **Question 2**
#
# A l'aide du module `pyspark.pandas` (renommé `ps`) lire les données du fichier `SpeedDating.csv` du HDFS dans une `DataFrame` pandas-on-spark que vous nommerez `psdf` et afficher le début de cette `DataFrame` avec la méthode `head()`.

# +  id="j2XQq6pAM_d6" outputId="dc3356da-6656-4b49-9e33-2d87f83c1b67"
import pyspark.pandas as ps

psdf = ps.read_csv("/user/VOTRE_PRENOM/tp_mllib/SpeedDating.csv")
psdf.head()

# + [markdown] id="rD_zBwWiQk7J"
# ## Sélection des données
#
# Certaines colonnes du fichier de données sont redondantes ou inexploitables, il faudra les éliminer.
#
# On va éliminer également les données relatives à la personne rencontrées car celles-ci sont incomplètes. On les complètera ultérieurement à l'aide d'une jointure afin d'obtenir une ligne de données par rencontre, comprenant les données complètes des deux personnes.
#
# Il faudra également éliminer les colonnes qui contiennent trop de données manquantes (inexploitables), et à la suite de ça, les lignes contenant encore des données manquantes.
#
# Enfin on éliminera les lignes correspondant aux sessions `6`, `7`, `8` et `9` (colonne `'wave'`) car les participant.e.s n'ont pas utilisé la même échelle pour donner leurs préférences quant aux qualités recherchées chez la personne de sexe opposé.
#
# **Question 3**
#
# En utilisant la méthode `loc`, sélectionner uniquement les colonnes des données récoltées avant la rencontre : toutes les colonnes du début jusqu'à la colonne `'amb5_1'`.

# + id="s8MlxWtPPdeR"  outputId="db5a833a-bf6d-4943-dd79-38a840fa4bec"
psdf = psdf.loc[:, :'amb5_1']

# + [markdown] id="Au3YG-CqTBDA"
# **Question 4**
#
# En utilisant la méthode `drop`, supprimer les colonnes redondantes ou inexploitables suivante : `'id', 'idg', 'partner', 'from', 'field', 'career'`

# + id="Uav8HwRlJZK1"
psdf = psdf.drop(['id', 'idg', 'partner', 'from', 'field', 'career'], axis=1)

# +  id="gTVW5_Ro-0kv" outputId="4d6db4ee-d007-4be8-afa6-67727709c1e1"
psdf.head()

# + [markdown] id="R3CapzZUcIF3"
# **Question 5**
#
# Supprimer les colonnes relatives à la personne rencontrée : toutes les colonnes dont le nom se termine par `_o` ou qui contient `_o_`.

# + id="C6Ayiek6cgit"
psdf = psdf.drop([c for c in psdf.columns if c.endswith("_o") or "_o_" in c], axis=1)

# + [markdown] id="dwPQEtiLc4iW"
# **Question 6**
#
# En utilisant la méthode `isna()`, compter le nombre de valeurs manquantes dans chaque colonne restante.

# +  id="FgR4c0vMdT7o" outputId="2ec0286a-5424-493f-dd88-f932d3897800"
psdf.isna().sum()

# + [markdown] id="5RYgqhbtePg6"
# **Question 7**
#
# Garder uniquement les colonnes qui ont moins de `90` valeurs manquantes (environ 1% du total) puis supprimer les lignes contenant encore des valeurs manquantes à l'aide de la méthode `dropna()`.
#
# *Indication: la méthode `to_numpy()` permet de convertir une `Serie` contenant des booléens en un tableau de booléens.*

# +  id="DTfZF1TWCNb4" outputId="bd171aaa-61d1-4029-c54e-d2a1bd850679"
psdf = psdf.loc[:, (psdf.isna().sum() < 90).to_numpy()].dropna()

# + [markdown] id="Xx8DBC-5fY5j"
# **Question 8**
#
# Supprimer les lignes correspondant aux sessions (`'wave'`) comprises entre 6 et 9 (bornes comprises).

# + id="BX_Ef4YgOL12"
psdf = psdf[~psdf['wave'].between(6,9)]

# +  id="7TgFJIBEEQs0" outputId="ad76fd3c-246c-4440-a492-d5b1b9e8b829"
# pour vérification
psdf[psdf['wave'] == 7]

# + [markdown] id="eULFuQXVhM79"
# ## Formatage des données
#
# **Question 9**
#
# Afficher l'attribut `dtypes` de la `DataFrame` afin de visualiser le type des données. Véririfer que la colonne `sports` devrait contenir des nombres alors qu'elle est de type `object` (type correspondant à des chaîne de caractères dans Pandas).

# +  id="561AFlPdhYPG" outputId="e0e02efe-97bb-4e86-e06e-696444545c44"
psdf.dtypes

# + [markdown] id="NEogVZDZlADX"
# **Question 10**
#
# A l'aide de la méthode `astype()` convertir les colonnes `sports` et `field_cd` (catégorie d'études) en type `'int32'`

# + id="_go-R5Azmwyo"
psdf = psdf.astype({'sports':'int32','field_cd':'int32'})

# +  id="nNjhTZA7F8HV" outputId="19cb0768-bbb4-4d10-a51e-fef031beeed0"
psdf.dtypes

# + [markdown] id="Bev4B6wULAfF"
# **Question 11**
#
# Les colonnes `'field_cd'` et `'race'` correspondent à des données catégorielles : il faut les convertir en colonne de "*dummies*" (*one-hot-encoding*).
#
# Utiliser la fonction `ps.get_dummies()` sur chacune de ces colonnes pour obtenir les colonnes de *dummies* correspondantes (on prendra le nom de la colonne d'origine comme préfixe des colonnes de *dummies*).
#
# Vous concaténerez à chaque fois ces colonnes de *dummies* à la `DataFrame` à l'aide de la fonction  `ps.concat()` et vous supprimerez la colonne catégorielle de départ.
#

# + id="nWUPjpXEmQ9D"  outputId="c9b6a56d-539f-42c7-b6d7-10100c258aa7"
psdf = ps.concat([psdf, ps.get_dummies(psdf['field_cd'], prefix='field_cd')], axis=1)
psdf = psdf.drop(['field_cd'], axis=1)

psdf = ps.concat([psdf, ps.get_dummies(psdf['race'], prefix='race')], axis=1)
psdf = psdf.drop(['race'], axis=1)
psdf.head()

# + [markdown] id="Q6a7ii6-pi31"
# ## Jointure
#
# Dans cette partie vous allez créer deux `DataFrames` à partir de la `DataFrame` obtenue après sélection et formatage des données, en séparant les données par sexe (colonne `'gender'`). Le but est de faire une jointure de ces deux `DataFrame` en utilisant les identifiant des participant.e.s afin d'obtenir une ligne de données par rencontre comprenant les données complète de la rencontre et des deux personnes.
#
# **Question 12**
#
# Créer deux `DataFrame` nommées `psdf_0` et `psdf_1` en filtrant les données de la `DataFrame` sur la colonne `'gender'`, et retirer de `psdf_1`  les colonnes `"condtn"`, `"wave"`, `"position"`, `"match"`, `"int_corr"` et `"samerace"` car leurs données se retrouveraient en double dans la jointure finale.
#
# Appliquer la méthode `spark.persist()` aux deux `DataFrame` afin de les garder en mémoire à la prochaine action sans avoir à refaire l'ensemble des transformations. Afficher les deux `DataFrame` avec `head()` dans les deux cellules de code suivantes.

# + id="pHbiGZzKJ4FV"
psdf_0 = psdf[psdf['gender'] == 0].spark.persist()
psdf_1 = psdf[psdf['gender'] == 1].drop(["condtn", "wave", "position", "match", "int_corr", "samerace"], axis=1).spark.persist()

# +  id="aGHaTUNexsUM" outputId="edaf1613-c512-4ebf-bd3a-3e950eb456cd"
psdf_0.head()

# +  id="KL4rO1axx72J" outputId="5a55ccdd-2250-4793-e400-cc64d2bf5ea9"
psdf_1.head()

# + [markdown] id="uy6XDz0drv19"
# **Question 13**
#
# Utiliser la méthode `merge()` pour obtenir une `DataFrame` nommée `psdf_all` par jointure des `DataFrame` `psdf_0` et `psdf_1` sur les deux identifiants des participants (`'iid'` et `'pid'`) à la fois : `'iid'` dans l'une doit correspondre à `'pid'` dans l'autre et inversement.
#
# Supprimer de la DataFrame obtenue les lignes contenant des données manquantes avec `drop_na()` puis appliquer la méthode `spark.persist()` à `psdf_all`.

# + id="C44C91UvDa1c"
psdf_all = psdf_0.merge(psdf_1, how="inner", left_on=["iid", "pid"], right_on=["pid", "iid"])
psdf_all = psdf_all.dropna().spark.persist()


# + [markdown] id="fwqFWmFL0iOs"
# **Question 14**
#
# Utiliser la méthode `set_index()` pour définir les colonnes `'iid'` et `'pid'` comme index (double) de `psdf_all` puis l'afficher avec `head()`.

# + id="u5b--PyVNP9r"  outputId="99080819-3034-437c-91a7-16b66b9fc856"
psdf_all = psdf_all.set_index(['iid', 'pid'])
psdf_all.head()

# + [markdown] id="QpDNMH1f2u0l"
# **Question 15**
#
# Afficher les dimensions de la DataFrame `psdf_all` avec l'attribut `shape` ainsi que le pourcentage de `'match'` dans ce jeu de données final.

# +  id="aafa7IU71toO" outputId="a2d078f5-0eea-4111-d8da-a9fdd7d5c534"
psdf_all.shape

# + [markdown] id="kCrC4uLr09j8"
# ## Prédiction de *match* avec MLlib
#
# Le but ici est de voir s'il est possible de prédire, à l'aide de la bibliothèque MLlib, la colonne `'match'` d'une ligne (i.e. une rencontre) à partir des données des autres colonnes sur un jeu de données de test, en utilisant un modèle de classification entrainé sur un jeu de données d'entrainement. On pourra ensuite analyser quelles sont les données les plus importantes pour faire cette prédiction.
#
# La première chose à faire est de convertir la DataFrame pandas-on-spark et DataFrame Spark SQL car c'est le format de donnée utilisé par MLlib.
#
# **Question 16**
#
# Utiliser la méthode `to_spark()` pour obtenir une DataFrame Spark SQL `sdf` à partir de `psdf_all` et afficher `sdf` avec la méthode `show()`.
#

# +  id="5XtSaWYDOnPH" outputId="476c1b7d-eb04-4cf8-968f-8e3fc235527f"
sdf = psdf_all.to_spark()
sdf.show()

# + [markdown] id="J_vxMaJZA37X"
# **Question 17**
#
# Utiliser la méthode `randomSplit()` sur `sdf` pour obtenir une DataFrame d'entrainement `trainDF` représentant 80% des données et une DataFrame de test `testDF` représentant 20% des données (fixer le paramètre `seed` pour pouvoir reproduire les résultats à l'identique).
#
# Appliquer les méthodes `persist()` puis `count()` sur ces deux DataFrame et afficher le résultat.

# +  id="XqfOhy3XB7qw" outputId="ee87fe7f-1123-4d5a-de45-f1009ffc59f4"
trainDF, testDF = sdf.randomSplit([0.8, 0.2], seed=24)
trainDF.persist().count()

# +  id="UasRGf6-OZe8" outputId="8b8f8027-f776-4875-859e-5fd38eb49ac9"
testDF.persist().count()

# + [markdown] id="sj-QnEfmCJ9Y"
# **Question 18**
#
# Utiliser la classe `VectorAssembler` du module `pyspark.ml.feature` pour créer un Transformer permettant d'assembler les colonnes des variables explicatives (toutes les colonnes sauf `'match'`) en vecteurs dans une unique colone de sortie `'features'`. Ce Transformer sera utilisé dans un Pipeline ultérieurement.

# + id="Od5m7k-4YFzC"
from pyspark.ml.feature import VectorAssembler

feat_col = [c for c in psdf_all.columns if c != 'match']

vecAssembler = VectorAssembler(inputCols=feat_col, outputCol="features")


# + [markdown] id="MNfDdjFurNnw"
# **Question 19**
#
# Utiliser la classe `MinMaxScaler` du module `pyspark.ml.feature` pour créer un Transformer permettant de remettre à l'échelle entre 0 et 1 les données contenues dans la colonne de sortie du `'VectorAssembler'` (utiliser la méthode `'getOutputCol()'` sur cet objet) dans une nouvelle colonne `'features_scaled'`. Ce Transformer sera utilisé dans un Pipeline ultérieurement.

# + id="xZsW9xvIs09S"
from pyspark.ml.feature import MinMaxScaler

minMaxScaler = MinMaxScaler(inputCol="features", outputCol="features_scaled")

# + [markdown] id="aqhILFfCEt06"
# **Question 20**
#
# Utiliser la classe `LogisticRegression` du module `pyspark.ml.classification` pour créer un Estimator avec un modèle de régression logistique destiné à prédire la classe `'match'` à partir des features contenues dans la colonne de sortie du `MinMaxScaler`. Cet Estimator sera utilisé dans un Pipeline ultérieurement.

# + id="wHwxh8nReBg6"
from pyspark.ml.classification import LogisticRegression

lr = LogisticRegression(featuresCol="features_scaled", labelCol="match")

# + [markdown] id="MMlrnjSt26g3"
# **Question 21**
#
# Créer un `Pipeline` (du module `pyspark.ml`) enchainant le `VectorAssembler`, le `MinMaxScaler` et l'estimateur `LogisticRegression`.

# + id="YVXDMB40d7ps"
from pyspark.ml import Pipeline

lrPipeline = Pipeline(stages=[vecAssembler, minMaxScaler, lr])

# + [markdown] id="0gFNoeK53ziv"
# **Question 22**
#
# Pour l'évaluation des modèles, créer un objet `bcEvaluator` de type `BinaryClassificationEvaluator` (module `pyspark.ml.evaluation`) avec la métrique `areaUnderROC` et deux objets `mcEvaluator_acc` et `mcEvaluator_f1` de type `MulticlassClassificationEvaluator` avec respectivement les métriques `accuracy` et `f1`. N'oubliez pas de spécifier `labelCol='match'`.

# + id="4LnnalMofsap"
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

bcEvaluator = BinaryClassificationEvaluator(labelCol="match", metricName="areaUnderROC")
mcEvaluator_acc = MulticlassClassificationEvaluator(labelCol="match", metricName="accuracy")
mcEvaluator_f1 = MulticlassClassificationEvaluator(labelCol="match", metricName="f1")

# + [markdown] id="TWr57P0A4On9"
# **Question 23**
#
# Créer des objets `CrossValidator` et `ParamGridBuilder` (module `pyspark.ml.tuning`) permettant de sélectionner par cross-validation 3-folds le meilleur hyperparamètre `regParam` pour l'estimateur `lr` parmi les valeurs `[0.1, 0.01, 0.001]`.

# + id="si4hPIXehg-d"
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

paramGrid_lr = ParamGridBuilder().addGrid(lr.regParam, [0.1, 0.01, 0.001]).build()
cv_lr = CrossValidator(estimator=lrPipeline, estimatorParamMaps=paramGrid_lr, evaluator=bcEvaluator, numFolds=3)

# + [markdown] id="md3Xf9ua_Trl"
# **Question 24**
#
# Entrainer et récupérer le meilleur modèle (méthode `fit()` du cross-validator) sur la DataFrame `trainDF` et récupérer les prédictions des `'matchs'` sur la DataFrame `testDF` (méthode `transform()` du modèle récupéré).
#
# Afficher les trois métriques d'évaluation sur ces prédictions (méthode `evaluate()` des évaluateurs).
#
# Expliquer pourquoi l'`accuracy` n'est pas une bonne métrique dans notre cas.
#
# Afficher le meilleur hyperparamètre `regParam` parmi les valeurs testées en utilisant la méthode `.bestModel.stages[-1]._java_obj.getRegParam()` sur le modèle renvoyé par le cross-validator.

# + id="EsKwhUM145GP"
cv_lr_model = cv_lr.fit(trainDF)
pred_lr = cv_lr_model.transform(testDF)

print("Binary auROC:", bcEvaluator.evaluate(pred_lr))
print("Accuracy:", mcEvaluator_acc.evaluate(pred_lr))
print("F1:", mcEvaluator_f1.evaluate(pred_lr))
print("Best regParam:", cv_lr_model.bestModel.stages[-1]._java_obj.getRegParam())

# + [markdown] id="56NYv1uAAccz"
# ## Importance des variables dans la prédiction des matchs
#
# Les modèles de forêt aléatoire permettent d'obtenir un classement de l'importance des variables utilisées pour faire la classification. Nous allons entrainer un modèle de ce type, évaluer ses performances de classification et visualiser l'importance des variables utilisées vis-à-vis de la prédiction des matchs.
#
# **Question 25**
#
# Refaire les même manipulations que précédemment (questions 20, 21, 23 et 24) pour un modèle `RandomForestClassifier` avec 100 arbres et en testant les valeurs `[1, 4, 8, 12]` pour l'hyperparamètre `minInstancesPerNode` par cross-validation 3-folds.

# + id="ovIXBb8avD3A"
from pyspark.ml.classification import RandomForestClassifier

rf = RandomForestClassifier(
    featuresCol="features_scaled",
    labelCol="match",
    numTrees=100,
    seed=24,
)

rfPipeline = Pipeline(stages=[vecAssembler, minMaxScaler, rf])
paramGrid_rf = (
    ParamGridBuilder()
    .addGrid(rf.minInstancesPerNode, [1, 4, 8, 12])
    .build()
)
cv_rf = CrossValidator(
    estimator=rfPipeline, estimatorParamMaps=paramGrid_rf, evaluator=bcEvaluator, numFolds=3
)

cv_rf_model = cv_rf.fit(trainDF)
pred_rf = cv_rf_model.transform(testDF)

print("RF Binary auROC:", bcEvaluator.evaluate(pred_rf))
print("RF Accuracy:", mcEvaluator_acc.evaluate(pred_rf))
print("RF F1:", mcEvaluator_f1.evaluate(pred_rf))
print("RF best minInstancesPerNode:", cv_rf_model.bestModel.stages[-1]._java_obj.getMinInstancesPerNode())

# + [markdown] id="ifLcZmIsBZ41"
# **Question 26**
#
# Récupérer le meilleur modèle de RandomForest en appelant la méthode `.bestModel.stages[-1]` sur le modèle récupéré du cross-validator et visualiser la propriété `featureImportances`de ce meilleur modèle RandomForest.
#

# + id="V_s_ddO0y5RQ"
rf_best = cv_rf_model.bestModel.stages[-1]
rf_best.featureImportances

# + [markdown] id="yDDyC7VkBA1w"
# **Question 27**
#
# Trier les valeurs d'importance par ordre décroissant en mettant en correspondance les noms des variables associées et analyser les résultats pour en déduire celles qui sont les plus pertinentes pour prédire la classe `'match'`.

# + id="2jnyfJb57U6o"
import pandas as pd

feat_importances = pd.Series(rf_best.featureImportances.toArray(), index=feat_col)
feat_importances.sort_values(ascending=False).head(20)

# + id="MhtTeTtT_9Q-"
spark.stop()
