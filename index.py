# Import de fonctions depuis le Framework Flask
from flask import Flask
# Import d'une fonction pour convertir un template HTML en y injectant des variables python
from flask import render_template
# Import de la variable request de Flask
from flask import request
# Import d'une fonction pour rediriger la réponse,
# et url_for une méthode pour récupérer l'url avec son nom de fonction
from flask import redirect, url_for
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

# Depuis notre fichier post.py on importe la classe Post
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


# Association de la route "/post" à notre fonction display_posts()
@app.route('/posts')
def display_posts():
    # récupération des posts de la BDD.
    allPosts = Post.query.all()
    # Conversion du template "posts.html" en lui injectant notre tableau de posts récupérés de la BDD
    return render_template('posts.html', posts=allPosts)

# Association de la route "/users" à notre fonction display_users()
@app.route('/users')
def display_users():
    # récupération des utilisateur de la BDD.
    allUsers = User.query.all()
    # Conversion du template "posts.html" en lui injectant notre tableau de posts récupérés de la BDD
    return render_template('users.html', users=allUsers)

# Association de la route "/posts/<identifiant d'un utilisateur>" à notre fonction display_author_posts()
# exemple de route : /posts/1 ; l'entier "1" sera donnée en paramètre de notre fonction
@app.route('/posts/<int:user_id>')
def display_author_posts(user_id):
    # Récupération de l'utilisateur avec son identifiant
    user = User.query.filter_by(id=user_id).first()
    # Si l'utilisateur n'existe pas
    if user == None:
        # On renvoie une page 404 Not Found
        abort(404)
    # Récupération des posts en utilisant la relation définie dans le modèle
    authorPosts = user.posts
    # Réutilisation du template "posts.html" en y injectant notre tableau 
    # qui contient les posts d'un auteur
    return render_template('posts.html', posts=authorPosts)