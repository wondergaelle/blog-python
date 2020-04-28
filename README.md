# Activer l'environnement virtuel
. venv/bin/activate

# installer Flask dans l'environnement virtuel
pip3 install flask

# lancer l'application
export FLASK_APP=index.py

# Automatisation mise à jour 
export FLASK_ENV=development
set FLASK_ENV=development

# lancer le run
flask run

# base de données 
from index import db
db.create_all()

