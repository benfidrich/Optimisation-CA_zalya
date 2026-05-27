from pymongo import MongoClient
from datetime import datetime
import pandas as pd

# CONNEXION MONGODB

client = MongoClient("mongodb://localhost:27017/")

db = client["crm_decisionnel"]

collection_opportunites = db["opportunites"]
collection_regles = db["regles_analytiques"]
collection_insights = db["insights"]

# LECTURE DES DONNÉES


df_crm = pd.read_csv("C:/Users/testa/Documents/Zalya_Stage/DATA/Analyse_prépa1 (1).csv")
df_crm.columns = df_crm.columns.str.strip()
print(df_crm.dtypes)
print(df_crm.head())
print(df_crm.columns)

regles = list(collection_regles.find())

# FONCTION INSERTION INSIGHT

def inserer_insight(insight):

    existing = collection_insights.find_one({

        "regle_associee": insight["regle_associee"],

        "description": insight["description"]
    })

    if not existing:

        collection_insights.insert_one(insight)

        print(f"Insight ajouté : {insight['regle_associee']}")

    else:

        print(f"Insight déjà existant : {insight['regle_associee']}")


df_crm["Probabilite"] = pd.to_numeric(

    df_crm["Probabilite"],

    errors="coerce"
)

df_crm["Revenu_attendu"] = pd.to_numeric(

    df_crm["Revenu_attendu"],

    errors="coerce"
)

# BLOCAGE PIPELINE

for regle in regles:

    if regle["nom_regle"] == "blocage_pipeline_prospects":

        nb_prospects = len(df_crm[df_crm["Etape"] == "Prospects"])

        pourcentage = (nb_prospects / len(df_crm)) * 100

        if pourcentage > regle["condition"]["valeur"]:

            insight = {

                "type_insight": "pipeline",

                "regle_associee":
                regle["nom_regle"],

                "description":
                f"{pourcentage:.2f}% des opportunités sont dans Prospect.",

                "niveau_criticite":
                regle["niveau_criticite"],

                "valeur_detectee":
                float(pourcentage),

                "recommandation":
                regle["recommandation"],

                "date_detection":
                datetime.now()
            }

            inserer_insight(insight)

# FAIBLE POTENTIEL FINANCIER

for regle in regles:

    if regle["nom_regle"] == "faible_potentiel_financier":

        revenu_total = df_crm["Revenu_attendu"].sum()

        if revenu_total < regle["condition"]["valeur"]:

            insight = {

                "type_insight": "revenu",

                "regle_associee":
                regle["nom_regle"],

                "description":
                f"Le revenu total est faible : {revenu_total:.2f}",

                "niveau_criticite":
                regle["niveau_criticite"],

                "valeur_detectee":
                float(revenu_total),

                "recommandation":
                regle["recommandation"],

                "date_detection":
                datetime.now()
            }

            inserer_insight(insight)

# VOLUME CRITIQUE ÉLEVÉ

for regle in regles:

    if regle["nom_regle"] == "volume_critique_eleve":

        nb_critiques = len(df_crm[df_crm["Priorite"] == "Haute"])

        if nb_critiques > regle["condition"]["valeur"]:

            insight = {

                "type_insight": "priorite",

                "regle_associee":
                regle["nom_regle"],

                "description":
                f"{nb_critiques} opportunités critiques détectées.",

                "niveau_criticite":
                regle["niveau_criticite"],

                "valeur_detectee":
                int(nb_critiques),

                "recommandation":
                regle["recommandation"],

                "date_detection":
                datetime.now()
            }

            inserer_insight(insight)

# FAIBLE TAUX DE CONVERSION

for regle in regles:

    if regle["nom_regle"] == "faible_taux_conversion":

        op_gagnees = len( df_crm[df_crm["Gagnee_Perdue"] == "Gagné"] )

        taux_conversion = (op_gagnees / len(df_crm)) * 100

        if taux_conversion < regle["condition"]["valeur"]:

            insight = {

                "type_insight": "conversion",

                "regle_associee":
                regle["nom_regle"],

                "description":
                f"Le taux de conversion est faible : {taux_conversion:.2f}%",

                "niveau_criticite":
                regle["niveau_criticite"],

                "valeur_detectee":
                float(taux_conversion),

                "recommandation":
                regle["recommandation"],

                "date_detection":
                datetime.now()
            }

            inserer_insight(insight)

# DÉPENDANCE VENDEUR

for regle in regles:

    if regle["nom_regle"] == "dependance_vendeur":

        vendeurs = df_crm.groupby(
            "Vendeur"
        )["Revenu_attendu"].sum()

        max_vendeur = vendeurs.max()

        revenu_total = vendeurs.sum()

        pourcentage = (

            max_vendeur / revenu_total
        ) * 100

        if pourcentage > regle["condition"]["valeur"]:

            vendeur_top = vendeurs.idxmax()

            insight = {

                "type_insight": "vendeur",

                "regle_associee":
                regle["nom_regle"],

                "description":
                f"{vendeur_top} représente {pourcentage:.2f}% des revenus.",

                "niveau_criticite":
                regle["niveau_criticite"],

                "valeur_detectee":
                float(pourcentage),

                "recommandation":
                regle["recommandation"],

                "date_detection":
                datetime.now()
            }

            inserer_insight(insight)

# RÈGLE 6 — FAIBLE PROBABILITÉ DE CONVERSION

for regle in regles:

    if regle["nom_regle"] == "faible_probabilite_conversion":

        fortes_prob = len(

            df_crm[df_crm["Probabilite"] >= 70]
        )

        pourcentage = (

            fortes_prob / len(df_crm)
        ) * 100

        if pourcentage < regle["condition"]["valeur"]:

            insight = {

                "type_insight": "probabilite",

                "regle_associee":
                regle["nom_regle"],

                "description":
                f"Seulement {pourcentage:.2f}% des opportunités ont une forte probabilité de conversion.",

                "niveau_criticite":
                regle["niveau_criticite"],

                "valeur_detectee":
                float(pourcentage),

                "recommandation":
                regle["recommandation"],

                "date_detection":
                datetime.now()
            }

            inserer_insight(insight)

# RÈGLE 7 — DÉPENDANCE CLIENT

for regle in regles:

    if regle["nom_regle"] == "dependance_client":

        clients = df_crm.groupby(
            "Client"
        )["Revenu_attendu"].sum()

        client_max = clients.max()

        revenu_total = clients.sum()

        pourcentage = (

            client_max / revenu_total
        ) * 100

        if pourcentage > regle["condition"]["valeur"]:

            client_dominant = clients.idxmax()

            insight = {

                "type_insight": "client",

                "regle_associee":
                regle["nom_regle"],

                "description":
                f"{client_dominant} représente {pourcentage:.2f}% du revenu total.",

                "niveau_criticite":
                regle["niveau_criticite"],

                "valeur_detectee":
                float(pourcentage),

                "recommandation":
                regle["recommandation"],

                "date_detection":
                datetime.now()
            }

            inserer_insight(insight)

print("Analyse terminée.")