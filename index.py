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
# import de la variable secret pour crypter les sessions
from variables import session_secret
# Import de la variable de session de Flask
from flask import session


# Création de notre application Flask
app = Flask(__name__)
# On donne un tableau de bytes aléatoire pour crypter nos sessions
app.secret_key = session_secret
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
#@app.route('/')
#def hello_world():
    #return redirect(url_for('display_posts'))


# Association de la route "/post" à notre fonction display_posts()
@app.route('/')
def display_posts():
    # récupération des posts de la BDD.
    allPosts = Post.query.all()
    # Conversion du template "posts.html" en lui injectant notre tableau de posts récupérés de la BDD
    return render_template('posts.html', posts=allPosts)


@app.route('/users/create', methods=['POST', 'GET'])
def create_user():
    # Si la méthode est de type "GET"
    if request.method == 'GET':
        # On affiche notre formulaire de création
        return render_template('create_user.html')
    else:
        # Sinon, notre méthode HTTP est POST
        # on va donc créer un nouvel utilisateur
        # récupération du nom de l'utilisateur depuis le corps de la requête
        name = request.form['name']
        # récupération de l'email depuis le corps de la requête
        email = request.form['email']
        # récupération du mot de passe depuis le corps de la requête
        password = request.form['password']
        # Création d'un utilisateur à l'aide du constructeur généré par SQLAlchemy 
        user = User(name=name, email=email, password=password)
        # Insertion de notre utilisateur dans session de base de données
        # Attention, celui-ci n'est pas encore présent dans la base de données
        db.session.add(user)
        # Sauvegarde de notre session dans la base de données
        db.session.commit()
        # Redirection vers la liste de nos tweets
        return redirect(url_for('display_users'))

# Association de la route "/posts/create" à notre fonction display_create_post()
# Celle ci accepte 2 méthode HTTP : GET & POST
@app.route('/posts/create', methods=['POST', 'GET'])
def display_create_post():
    # On autorise la création de post qu'aux utilisateurs enregistrés
    # Si user_id n'est pas dans notre variable session
    if not 'user_id' in session :
        # on redirige vers la page de login
        return redirect(url_for('login'))
    # Si la méthode est de type "GET"
    if request.method == 'GET':
        #Récupération de la liste des utilisateurs pour la relation post<->user
        users = User.query.all()
        # On affiche notre formulaire de création en lui donnant la liste des utilisateurs
        return render_template('create_post.html', users=users)
    else:
        # Sinon, notre méthode HTTP est POST
        # on va donc créer un nouveau post
        # récupération de l'identifiant de l'utilisateur depuis la variable de session
        user_id = session['user_id']
        # récupération du titre depuis le corps de la requête
        titre = request.form['titre']
        # récupération du titre depuis le corps de la requête
        resume = request.form['resume']
        # récupération du contenu depuis le corps de la requête
        content = request.form['content']
        # Création d'un post à l'aide du constructeur généré par SQLAlchemy 
        post = Post(user_id=user_id, titre=titre, resume=resume, content=content)
        # Insertion de notre post dans session de base de données
        # Attention, celui-ci n'est pas encore présent dans la base de données
        db.session.add(post)
        # Sauvegarde de notre session dans la base de données
        db.session.commit()
        # Redirection vers la liste de nos tweets
        return redirect(url_for('display_posts'))

# Association de la route "/posts/<identifiant d'un post/edit" à notre fonction edit_post()
# Celle ci accepte 2 méthode HTTP : GET & POST
@app.route('/posts/<int:post_id>/edit', methods=['POST', 'GET'])
def edit_post(post_id):
    # On récupère le post que l'on veut éditer dans notre base de données
    post = Post.query.filter_by(id=post_id).first()
    # Si on ne trouve pas le post
    if post == None:
        # On émet une erreur 404 Not Found
        abort(404)
    #Si notre méthode HTTP est GET
    if request.method == 'GET':
        # récupération de nos utilisateurs depuis la base de données
        users = User.query.all()
        # On affiche notre formulaire d'édition prérempli avec notre post
        # On donne également la liste des utilisateurs pour les afficher dans le select
        return render_template('edit_post.html', post=post, users=users)
    else:
        # Sinon nous avons une méthode HTTP POST, nous modifions donc notre tweet.
        # modification de l'auteur avec son identifiant depuis le corps de la requête
        post.user_id = request.form['user_id']
        # modification du contenu depuis le corps de la requête
        post.titre = request.form['titre']
        # modification du contenu depuis le corps de la requête
        post.resume = request.form['resume']
        # modification du contenu depuis le corps de la requête
        post.content = request.form['content']
        # Sauvegarde de notre session dans la base de données
        db.session.commit()
        # redirection vers l'affichage de nos tweets.
        return redirect(url_for('display_posts'))


# Association de la route "/users/<identifiant d'un utilisateur/edit" à notre fonction edit_user()
# Celle ci accepte 2 méthode HTTP : GET & POST
@app.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
def edit_user(user_id):
    # On récupère l'utilisateur que l'on veut éditer dans notre base de données
    user = User.query.filter_by(id=user_id).first()
    # Si on ne trouve pas l'utilisateur
    if user == None:
        # On émet une erreur 404 Not Found
        abort(404)
    #Si notre méthode HTTP est GET
    if request.method == 'GET':
        # On affiche notre formulaire d'édition prérempli avec notre utilisateur
        return render_template('edit_user.html', user=user)
    else:
        # Sinon nous avons une méthode HTTP POST, nous modifions donc notre utilisateur.
        # modification du nom de l'utilisateur depuis le corps de la requête
        user.name = request.form['name']
        # modification de l'email depuis le corps de la requête
        user.email = request.form['email']
        # Sauvegarde de notre session dans la base de données
        db.session.commit()
        # redirection vers l'affichage de nos utilisateurs.
        return redirect(url_for('display_users'))


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

# Association de la route "/login" à notre fonction login()
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si on est dans une requête GET
    if request.method == 'GET':
        # On affiche simplement le formulaire de Login
        return render_template('login.html')
    else:
        # Sinon cela veut dire qu'on est dans une méthode POST
        # On récupère l'utilisateur avec son email
        user = User.query.filter_by(email=request.form['email']).first()
        # Si notre utilisteur existe et 
        # Si le mot de passe présent dans le formulaire est le même que celui de la base de données
        if user != None and user.password == request.form['password'] :
            # On a réussi notre login, on inscrit donc le l'identifiant de l'utilisateur dans la variable de session
            session['user_id'] = user.id
            # on redirige l'utilisateur vers la liste des posts
            return redirect(url_for('display_posts'))
        else:
            # Si l'utilisateur n'existe pas ou que les mots de passes ne correspondent pas
            # on renvoie l'utilisateur vers le formulaire de login.
            return render_template('login.html', error="Email et/ou mot de passe incorrect")

# Association de la route "/logout" à notre fonction logout()
@app.route('/logout')
def logout():
    # Pour déconnecter l'utilisateur on enlève user_id de la variable session
    session.pop('user_id', None)
    return redirect(url_for('display_posts'))