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

collection_kpis = db["kpis"]

# DONNÉES

ventes = list(collection_ventes.find())

df_ventes = pd.DataFrame(ventes)

if df_ventes.empty:

    print("Aucune vente.")

else:

    # KPI 1 — CA TOTAL

    ca_total = df_ventes["montant_ttc"].sum()


    # KPI 2 — PANIER MOYEN


    panier_moyen = df_ventes["montant_ttc"].mean()

    # KPI 3 — TAUX FACTURES PAYÉES


    factures_payees = len(

        df_ventes[
            df_ventes["statut"] == "Payé"
        ]
    )

    taux_paiement = (

        factures_payees / len(df_ventes)
    ) * 100


    # KPI 4 — REVENU HT


    revenu_ht = df_ventes["montant_ht"].sum()


    # KPI 5 — REVENU TTC


    revenu_ttc = df_ventes["montant_ttc"].sum()

    # LISTE KPI


    liste_kpis = [

        {

            "categorie_kpi":
            "ventes",

            "nom_kpi":
            "ca_total",

            "valeur":
            float(ca_total),

            "unite":
            "FCFA",

            "interpretation":
            "Chiffre d'affaires global.",

            "source_donnees":
            ["ventes"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "ventes",

            "nom_kpi":
            "panier_moyen",

            "valeur":
            float(panier_moyen),

            "unite":
            "FCFA",

            "interpretation":
            "Valeur moyenne des ventes.",

            "source_donnees":
            ["ventes"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "ventes",

            "nom_kpi":
            "taux_factures_payees",

            "valeur":
            float(taux_paiement),

            "unite":
            "%",

            "interpretation":
            "Pourcentage des factures payées.",

            "source_donnees":
            ["ventes"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "ventes",

            "nom_kpi":
            "revenu_ht",

            "valeur":
            float(revenu_ht),

            "unite":
            "FCFA",

            "interpretation":
            "Total revenus hors taxes.",

            "source_donnees":
            ["ventes"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "ventes",

            "nom_kpi":
            "revenu_ttc",

            "valeur":
            float(revenu_ttc),

            "unite":
            "FCFA",

            "interpretation":
            "Total revenus TTC.",

            "source_donnees":
            ["ventes"],

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

    print("KPI ventes calculés.")