# abelio-test-tech
Mini-projet Data Science pour @Abelio

## 1. Paramétrage

### 1.0. Prérequis

- Python 3.9+
- Git 
- Jupyter Notebook ou JupyterLab

### 1.1. Clonage du projet git 

```bash
git clone https://github.com/samulational/abelio-test-tech.git
cd abelio-test-tech
```

### 1.2. Dataset

Pour des questions de confidentialité, les données utilisées **ne sont pas inculses dans le repository git**. 

Avant de lancer les notebooks, créer un dossier *data/* à la racine du projet, puis mettez-y les données du mini-projet.


> **Important:** Le dossier `data/` sera ignoré par git, si vous souhaitez changer ça, supprimer la ligne *data/* du fichier *.gitignore*.

### 1.3. Environnement Python

Vous pouvez créer un environnement virtuel pour y installer les dépendences requises dans le fichier *requirements.txt*.

Sur Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Sur Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Installation des dépendences:

```bash
pip install -r requirements.txt
```

### 1.4. Kernel Jupyter

Le Kernel Jupyter utilisé dans ce projet représente l'environnement commun entre les notebooks, créer un kernel du même nom, il englobera toutes les dépendences installées récemment.

```bash
python -m ipykernel install --user --name=abelio-test-tech --display-name "Python (abelio-test-tech)"
```

Le kernel sera :

```text
Python (abelio-test-tech)
```

## 2. Approche méthodologique du projet

Après étude de l'énoncé (non inclus dans le repo pour des raisons de confidentialité), je détaille ici les étapes majeures de ma réflexion. Le fichier *synthèse.pdf* aborde, pour chaque étape, les choix et leur justification ainsi que les ressources utilisées pour y arriver (docs, Assistant IA, etc.).

Pour chaque étape est fourni, si nécessaire, un notebook *.ipynb* qui pourra être exécuté pour la reproductibilité. Les parties du code re-adaptées d'anciers codes de mes travaux INRAE ou à partir de prototypes de code générés par un LLM seront explicités directement dans les commentaires du code. 

### 2.0. Analyse du besoin

On cherche à estimer la Masse Sèche (MS) de maïs ensilage à partir de données météo, et imagerie satellite. L'énoncé propose un modèle déterministe dit de Maizy qui se base sur le cumul de degrés-jours (accumulation de la chaleur). Outre le fait que ce modèle n'exploite pas les données satelittaires, des limites sont relevées sur l'utilisation de la température comme seul facteur de prédiction (détaillées sur le fichier de synthèse).

On proposera donc un modèle intégrant les autres facteurs disponibles (densité de la végétation, précipitations, ensoleillement, humidité, etc.) à la varaible *cumul de degrés-jours* utilisée dans la formule de Maizy (température).

Cependant, il faudra qu'on soit attentif sur le nombre de variables (features) qu'on choisit, les données fournies pour entraîner notre modèle présente moins de 200 échantillons venant du même bassin de plantation, utiliser toutes les variables sans réduction de dimensionalité peut contraindre la généralisabilité du modèle (curse of dimensionality, overfitting des modèles ML simples) car beaucoup de dimensions et pas assez de diversité des échantillons (variance petite). 

On utilisera le modèle fourni (Maizy) comme baseline pour vérifier si notre proposition améliore la prédiction de la MS.

### 2.1 Préparation des données

> **Code:** Le notebook *data_preprocessing.ipynb* contient le code concernant cette partie.

Les données utilisées sont de 4 types : numériques, catégorielles (récolte précoce, semi-précoce, etc.), temporelles (dates) et multi-spectrales (images satelittes).

Pour pouvoir agréger les variables en features et réduire la dimensionalité, il faudrait convertir les types non numériques en données numériques, ceci permettra de créer des features qui agrégent 2 ou plus de nos variables de base. plus le nombre de features est petit et représentatif des autres features (qu'ils les prennent en compte dans leur formule), plus ça nous permettra d'entraîner un modèle simple, évitant ainsi le overfitting.

> **Important:** La variable catégorielle précocité contient des champs vides "UNKNOWN" qu'il faudrait combler en fonction de l'usage qu'on décide de faire de la variable dans notre modèle.

On effectue la transformation en données numériques :

- Des données catégorielles : En attribuant à chaque précocité un entier selon son degré de "précoce" à "tardif".
- Des données satellites : En calculant une valeur qui traduit la densité de la végétation (indice de végétation).
- Des données temporelles : En transformant la date en valeur numérique traduisant le jour de l'année de 1 à 366.

Pour la gestion des données manquantes, vu qu'on utilisera la variable de précocité uniquement pour trouver les facteurs a et b dans la formule de Maizy en les utilisants comme des flags, on attribuera aux précocités inconnues la valeur *-1* pour utiliser une moyenne des facteurs et éviter debruiter les valeurs de Maizy calculées.  

### 2.2 EDA : Analyse exploratoire des données

> **Code:** Le notebook *eda.ipynb* contient le code concernant cette partie.

### 2.3 Feature Selection & Scaling

> **Code:** Le notebook *feature_engineering.ipynb* contient le code concernant cette partie.

### 2.4 Feature Engineering

> **Code:** Le notebook *feature_engineering.ipynb* contient le code concernant cette partie.

### 2.5 Model Selection & Training

> **Code:** Le notebook *model_training.ipynb* contient le code concernant cette partie.

### 2.6 Model Evaluation

> **Code:** Le notebook *model_evaluation.ipynb* contient le code concernant cette partie.

### 2.7 Synthèse & Conclusions
