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

collection_services = db["services"]

collection_kpis = db["kpis"]

# DONNÉES

services = list(collection_services.find())

df_services = pd.DataFrame(services)

if df_services.empty:

    print("Aucun service.")

else:

    # COLONNES

    colonnes_numeriques = [
        "prix_reference",
        "cout_estime",
        "marge_estimee"
    ]

    for colonne in colonnes_numeriques:

        if colonne not in df_services.columns:

            df_services[colonne] = 0

        df_services[colonne] = pd.to_numeric(
            df_services[colonne],
            errors="coerce"
        ).fillna(0)

    if "actif" not in df_services.columns:

        df_services["actif"] = False

    if "categorie" not in df_services.columns:

        df_services["categorie"] = "Non définie"

    # KPI

    nombre_services = int(len(df_services))

    services_actifs = int(
        df_services["actif"].sum()
    )

    prix_moyen = round(
        float(df_services["prix_reference"].mean()),
        2
    )

    cout_moyen = round(
        float(df_services["cout_estime"].mean()),
        2
    )

    marge_moyenne = round(
        float(df_services["marge_estimee"].mean()),
        2
    )

    categorie_dominante = str(
        df_services["categorie"]
        .fillna("Non définie")
        .mode()[0]
    )

    # DOCUMENT KPI

    document = {

        "categorie_kpi": "services",

        "nom_kpi": "performance_services",

        "valeur": {

            "nombre_services": nombre_services,

            "services_actifs": services_actifs,

            "prix_moyen": prix_moyen,

            "cout_moyen": cout_moyen,

            "marge_moyenne": marge_moyenne,

            "categorie_dominante": categorie_dominante
        },

        "unite": "statistiques_services",

        "periode": {

            "annee": int(datetime.now().year)
        },

        "interpretation":
        "Indicateurs globaux de performance des services.",

        "source_donnees": [
            "services"
        ],

        "date_calcul": datetime.now(),

        "version_kpi": 1
    }

    # INSERTION

    collection_kpis.insert_one(document)

    print("KPI services calculé.")