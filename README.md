# abelio-test-tech
Mini-projet Data Science pour @Abelio

## 1. Paramétrage

### Prérequis

- Python 3.9+
- Git 
- Jupyter Notebook ou JupyterLab

### Clonage du projet git 

```bash
git clone https://github.com/samulational/abelio-test-tech.git
cd abelio-test-tech
```

### Dataset

Pour des questions de confidentialité, les données utilisées **ne sont pas inculses dans le repository git**. 

Avant de lancer les notebooks, créer un dossier *data/* à la racine du projet, puis mettez-y les données du mini-projet.


> **Important:** Le dossier `data/` sera ignoré par git, si vous souhaitez changer ça, supprimer la ligne *data/* du fichier *.gitignore*.

### Environnement Python

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

### Kernel Jupyter

Le Kernel Jupyter utilisé dans ce projet représente l'environnement commun entre les notebooks, créer un kernel du même nom, il englobera toutes les dépendences installées récemment.

```bash
python -m ipykernel install --user --name=abelio-test-tech --display-name "Python (abelio-test-tech)"
```

Le kernel sera :

```text
Python (abelio-test-tech)
```