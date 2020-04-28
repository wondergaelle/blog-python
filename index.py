# Import de fonctions depuis le Framework Flask
from flask import Flask
# Import de la lib "os" qui permet d'interagir avec notre système d'exploitation
import os
# Import de la gestion de BDD à l'aide du framework SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# Import d'une fonction flask pour terminer une requête avec un code d'erreur
from flask import abort
# Import de la lib requests pour exécuter des requêtes HTTP(S)
import requests


# Création de notre application Flask
app = Flask(__name__)
# Specification du chemin de notre fichier de Base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Création de l'instance de notre base de données
db = SQLAlchemy(app)

from post import Post
from user import User

# Récupération du chemin du fichier de la base de données
dbPath = os.path.join(app.root_path, 'data.db')
# Si le fichier n'existe pas
if not os.path.exists(dbPath):
    # Je créer ma base de données
    db.create_all()
    print("Base de données créée")

# Tableau pour stocker nos posts
posts = []


# Association de la route "/" à notre fonction hello_world()
@app.route('/')
def hello_world():
    # On renvoi à notre navigateur du texte
    return 'Hello, World!'