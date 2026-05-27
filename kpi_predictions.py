import sys
import os

sys.path.append(

    os.path.abspath(

        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import pandas as pd

import numpy as np

from datetime import datetime

from config.mongodb import db

# COLLECTIONS

collection_ventes = db["ventes"]

collection_kpis = db["kpis"]

# DONNÉES

ventes = list(collection_ventes.find())

df_ventes = pd.DataFrame(ventes)

if df_ventes.empty:

    print("Aucune donnée ventes.")

else:

    # AGRÉGATION MENSUELLE

    ventes_mensuelles = (

        df_ventes

        .groupby("mois")["montant_ttc"]

        .sum()

        .sort_index()
    )

    # TABLEAU NUMPY

    y = ventes_mensuelles.values

    x = np.arange(len(y))

    # RÉGRESSION LINÉAIRE

    coefficients = np.polyfit(x, y, 1)

    tendance = coefficients[0]

    intercept = coefficients[1]

    # PRÉVISION MOIS SUIVANT

    prochain_mois = len(y)

    prediction_ca = (

        tendance * prochain_mois
        + intercept
    )

    # INTERPRÉTATION

    if tendance > 0:

        interpretation = (

            "Croissance positive du chiffre d'affaires."
        )

    else:

        interpretation = (

            "Tendance baissière du chiffre d'affaires."
        )

    # KPI DOCUMENT

    document = {

        "categorie_kpi":
        "prediction",

        "nom_kpi":
        "prevision_chiffre_affaires",

        "valeur":
        float(prediction_ca),

        "unite":
        "FCFA",

        "periode": {

            "annee":
            int(datetime.now().year)
        },

        "interpretation":
        interpretation,

        "details_prediction": {

            "tendance":
            float(tendance),

            "nombre_mois_analyse":
            int(len(y))
        },

        "source_donnees": [

            "ventes"
        ],

        "date_calcul":
        datetime.now(),

        "version_kpi":
        1
    }

    # INSERTION

    existe = collection_kpis.find_one({

        "nom_kpi":
        "prevision_chiffre_affaires"
    })

    if not existe:

        collection_kpis.insert_one(document)

    print("KPI prédictif calculé.")