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

from datetime import datetime

from config.mongodb import db

# COLLECTIONS

collection_devis = db["devis"]

collection_kpis = db["kpis"]

# DONNÉES

devis = list(collection_devis.find())

df_devis = pd.DataFrame(devis)

if df_devis.empty:

    print("Aucun devis.")

else:

    # KPI 1 — NOMBRE TOTAL DEVIS

    total_devis = len(df_devis)


    # KPI 2 — DEVIS TRANSFORMÉS


    devis_transformes = len(

        df_devis[
            df_devis["conversion"] == "true"
        ]
    )

    # KPI 3 — DEVIS PERDUS


    devis_perdus = len(

        df_devis[
            df_devis["conversion"] == "false"
        ]
    )

    # KPI 4 — TAUX TRANSFORMATION

    taux_transformation = (

        devis_transformes / total_devis
    ) * 100

    # KPI 5 — VALEUR TOTALE DEVIS

    valeur_devis = (

        df_devis["montant"].sum()
    )

    # KPI 6 — PANIER MOYEN DEVIS

    panier_moyen = (

        df_devis["montant"].mean()
    )

    # KPI 7 — MEILLEUR VENDEUR

    vendeur_perf = (

        df_devis

        .groupby("vendeur")["montant"]

        .sum()
    )

    meilleur_vendeur = vendeur_perf.idxmax()

    meilleur_ca = vendeur_perf.max()

    # KPI LISTE

    liste_kpis = [

        {

            "categorie_kpi":
            "devis",

            "nom_kpi":
            "nombre_total_devis",

            "valeur":
            int(total_devis),

            "unite":
            "devis",

            "interpretation":
            "Volume total des devis.",

            "source_donnees":
            ["devis"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "devis",

            "nom_kpi":
            "devis_transformes",

            "valeur":
            int(devis_transformes),

            "unite":
            "devis",

            "interpretation":
            "Nombre de devis convertis.",

            "source_donnees":
            ["devis"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "devis",

            "nom_kpi":
            "devis_perdus",

            "valeur":
            int(devis_perdus),

            "unite":
            "devis",

            "interpretation":
            "Nombre de devis perdus.",

            "source_donnees":
            ["devis"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "devis",

            "nom_kpi":
            "taux_transformation_devis",

            "valeur":
            float(taux_transformation),

            "unite":
            "%",

            "interpretation":
            "Taux de conversion des devis.",

            "source_donnees":
            ["devis"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "devis",

            "nom_kpi":
            "valeur_totale_devis",

            "valeur":
            float(valeur_devis),

            "unite":
            "FCFA",

            "interpretation":
            "Valeur totale des devis.",

            "source_donnees":
            ["devis"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "devis",

            "nom_kpi":
            "panier_moyen_devis",

            "valeur":
            float(panier_moyen),

            "unite":
            "FCFA",

            "interpretation":
            "Valeur moyenne des devis.",

            "source_donnees":
            ["devis"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "devis",

            "nom_kpi":
            "meilleur_vendeur_devis",

            "valeur":
            float(meilleur_ca),

            "unite":
            "FCFA",

            "interpretation":
            f"Meilleur vendeur : {meilleur_vendeur}",

            "source_donnees":
            ["devis"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        }
    ]

    # INSERTION

    for kpi in liste_kpis:

        existe = collection_kpis.find_one({

            "nom_kpi":
            kpi["nom_kpi"]
        })

        if not existe:

            collection_kpis.insert_one(kpi)

    print("KPI devis calculés.")