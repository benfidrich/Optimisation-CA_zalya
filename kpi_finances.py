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

collection_ventes = db["ventes"]

collection_operations = db["operations"]

collection_kpis = db["kpis"]

# DONNÉES

ventes = list(collection_ventes.find())

operations = list(collection_operations.find())

df_ventes = pd.DataFrame(ventes)

df_operations = pd.DataFrame(operations)

if df_ventes.empty or df_operations.empty:

    print("Données insuffisantes.")

else:

    # KPI 1 — REVENU TOTAL


    revenu_total = (

        df_ventes["montant_ttc"]

        .sum()
    )

    # KPI 2 — COÛTS OPÉRATIONNELS
  

    cout_total = (

        df_operations["montant_ttc"]

        .sum()
    )

    # KPI 3 — MARGE BRUTE


    marge_brute = (

        revenu_total - cout_total
    )

    # KPI 4 — RATIO DÉPENSES / REVENUS


    ratio_depenses = (

        cout_total / revenu_total
    ) * 100

    # KPI 5 — COÛT MOYEN OPÉRATION


    cout_moyen = (

        df_operations["montant_ttc"]

        .mean()
    )

    # KPI 6 — RENTABILITÉ GLOBALE


    rentabilite = (

        marge_brute / revenu_total
    ) * 100

    # KPI LISTE


    liste_kpis = [

        {

            "categorie_kpi":
            "finance",

            "nom_kpi":
            "revenu_total",

            "valeur":
            float(revenu_total),

            "unite":
            "FCFA",

            "interpretation":
            "Revenus globaux de l'entreprise.",

            "source_donnees":
            ["ventes"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "finance",

            "nom_kpi":
            "couts_operationnels",

            "valeur":
            float(cout_total),

            "unite":
            "FCFA",

            "interpretation":
            "Total des dépenses opérationnelles.",

            "source_donnees":
            ["operations"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "finance",

            "nom_kpi":
            "marge_brute",

            "valeur":
            float(marge_brute),

            "unite":
            "FCFA",

            "interpretation":
            "Bénéfice brut après déduction des coûts.",

            "source_donnees":
            ["ventes", "operations"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "finance",

            "nom_kpi":
            "ratio_depenses_revenus",

            "valeur":
            float(ratio_depenses),

            "unite":
            "%",

            "interpretation":
            "Pourcentage des dépenses par rapport aux revenus.",

            "source_donnees":
            ["ventes", "operations"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "finance",

            "nom_kpi":
            "cout_moyen_operation",

            "valeur":
            float(cout_moyen),

            "unite":
            "FCFA",

            "interpretation":
            "Coût moyen des opérations.",

            "source_donnees":
            ["operations"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "finance",

            "nom_kpi":
            "rentabilite_globale",

            "valeur":
            float(rentabilite),

            "unite":
            "%",

            "interpretation":
            "Rentabilité générale de l'entreprise.",

            "source_donnees":
            ["ventes", "operations"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        }
    ]


    # INSERTION MONGODB
  

    for kpi in liste_kpis:

        existe = collection_kpis.find_one({

            "nom_kpi":
            kpi["nom_kpi"]
        })

        if not existe:

            collection_kpis.insert_one(kpi)

    print("KPI financiers calculés.")