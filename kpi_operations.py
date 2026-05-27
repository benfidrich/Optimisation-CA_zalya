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

collection_operations = db["operations"]

collection_kpis = db["kpis"]

# DONNÉES

operations = list(collection_operations.find())

df_operations = pd.DataFrame(operations)

if df_operations.empty:

    print("Aucune opération.")

else:

    # COLONNES

    colonnes_numeriques = [
        "montant_ttc",
        "tva"
    ]

    for colonne in colonnes_numeriques:

        if colonne not in df_operations.columns:

            df_operations[colonne] = 0

        df_operations[colonne] = pd.to_numeric(
            df_operations[colonne],
            errors="coerce"
        ).fillna(0)

    if "categorie_depense" not in df_operations.columns:

        df_operations["categorie_depense"] = "Non définie"

    if "mois" not in df_operations.columns:

        df_operations["mois"] = "Inconnu"

    # KPI

    couts_totaux = round(
        float(df_operations["montant_ttc"].sum()),
        2
    )

    cout_moyen = round(
        float(df_operations["montant_ttc"].mean()),
        2
    )

    tva_totale = round(
        float(df_operations["tva"].sum()),
        2
    )

    depenses_par_categorie = (

        df_operations

        .groupby("categorie_depense")[
            "montant_ttc"
        ]

        .sum()
    )

    if depenses_par_categorie.empty:

        categorie_dominante = "Non définie"

    else:

        categorie_dominante = str(
            depenses_par_categorie.idxmax()
        )

    cout_mensuel = round(

        float(

            df_operations

            .groupby("mois")[
                "montant_ttc"
            ]

            .sum()

            .mean()
        ),

        2
    )

    # DOCUMENT KPI

    document = {

        "categorie_kpi": "operations",

        "nom_kpi": "performance_operations",

        "valeur": {

            "couts_totaux": couts_totaux,

            "cout_moyen": cout_moyen,

            "tva_totale": tva_totale,

            "categorie_depense_dominante":
            categorie_dominante,

            "cout_mensuel_moyen":
            cout_mensuel
        },

        "unite": "fcfa",

        "periode": {

            "annee": int(datetime.now().year)
        },

        "interpretation":
        "Analyse globale des dépenses et opérations.",

        "source_donnees": [
            "operations"
        ],

        "date_calcul": datetime.now(),

        "version_kpi": 1
    }

    collection_kpis.insert_one(document)

    print("KPI opérations calculé.")