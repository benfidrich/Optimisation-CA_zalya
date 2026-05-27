from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["crm_decisionnel"]
collection_regles = db["regles_analytiques"]

regle_pipeline = {
    "nom_regle":
    "blocage_pipeline_prospects",

    "description":
    "Détecte une concentration excessive des opportunités dans Prospect.",

    "categorie":
    "pipeline",

    "champ_analyse":
    "Etape",

    "condition": {

        "operateur": "superieur_pourcentage",

        "valeur": 60
    },

    "niveau_criticite":
    "moyen",

    "message_alerte":
    "Le pipeline commercial semble bloqué dans la phase Prospect.",

    "recommandation":
    "Renforcer le suivi commercial.",

    "actif": True,

    "date_creation": datetime.now()
}

regle_probabilite = {
                     
  "nom_regle":
  "faible_probabilite_conversion",

  "categorie":
  "probabilite",

  "champ_analyse":
  "Probabilite",

  "condition": {

      "operateur": "inferieur_nombre",

      "valeur": 10
  },

  "niveau_criticite":
  "eleve",

  "message_alerte":
  "Peu d'opportunités présentent une forte probabilité de conversion.",

  "recommandation":
  "Améliorer la qualification des prospects.",

  "actif": True,
  "date_creation": datetime.now()
}

regle_client = {
  "nom_regle":
  "dependance_client",

  "categorie":
  "client",

  "champ_analyse":
  "Client",

  "condition": {

      "operateur": "superieur_pourcentage",

      "valeur": 40
  },

  "niveau_criticite":
  "eleve",

  "message_alerte":
  "Une forte dépendance commerciale à un client est détectée.",

  "recommandation":
  "Diversifier le portefeuille clients.",

  "actif": True,
  "date_creation": datetime.now()
}

regle_revenu = {

    "nom_regle":
    "faible_potentiel_financier",

    "description":
    "Détecte un faible potentiel financier dans le pipeline commercial.",

    "categorie":
    "revenu",

    "champ_analyse":
    "Revenu_attendu",

    "condition": {

        "operateur": "inferieur_montant",

        "valeur": 1000000
    },

    "niveau_criticite":
    "eleve",

    "message_alerte":
    "Le potentiel financier du pipeline est faible.",

    "recommandation":
    "Augmenter les opportunités à forte valeur.",

    "actif": True,

    "date_creation": datetime.now()
}

regle_priorite = {

    "nom_regle":
    "volume_critique_eleve",

    "description":
    "Détecte un volume élevé d'opportunités critiques.",

    "categorie":
    "priorite",

    "champ_analyse":
    "Priorite",

    "condition": {

        "operateur": "superieur_nombre",

        "valeur": 15
    },

    "niveau_criticite":
    "moyen",

    "message_alerte":
    "Le volume d'opportunités critiques est élevé.",

    "recommandation":
    "Prioriser le traitement des dossiers critiques.",

    "actif": True,

    "date_creation": datetime.now()
}

regle_conversion = {

    "nom_regle":
    "faible_taux_conversion",

    "description":
    "Détecte un faible nombre d'opportunités gagnées.",

    "categorie":
    "conversion",

    "champ_analyse":
    "Gagnee_Perdue",

    "condition": {

        "operateur": "inferieur_pourcentage",

        "valeur": 20
    },

    "niveau_criticite":
    "eleve",

    "message_alerte":
    "Le taux de conversion commerciale est faible.",

    "recommandation":
    "Améliorer le suivi des opportunités commerciales.",

    "actif": True,

    "date_creation": datetime.now()
}

regle_vendeur = {

    "nom_regle":
    "dependance_vendeur",

    "description":
    "Détecte une concentration excessive des revenus sur un vendeur.",

    "categorie":
    "vendeur",

    "champ_analyse":
    "Vendeur",

    "condition": {

        "operateur": "superieur_pourcentage",

        "valeur": 50
    },

    "niveau_criticite":
    "moyen",

    "message_alerte":
    "Une forte dépendance commerciale à un vendeur est détectée.",

    "recommandation":
    "Rééquilibrer la répartition des opportunités.",

    "actif": True,

    "date_creation": datetime.now()
}


#INSERTIONS
collection_regles.insert_one(regle_pipeline)
collection_regles.insert_one(regle_probabilite)
collection_regles.insert_one(regle_client)
collection_regles.insert_many([
regle_revenu,
regle_priorite,
regle_conversion,
regle_vendeur
])

