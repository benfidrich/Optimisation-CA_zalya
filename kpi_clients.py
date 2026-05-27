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

    print("Aucune donnée ventes.")

else:


    # KPI 1 — CA PAR CLIENT

    ca_clients = (

        df_ventes

        .groupby("client")["montant_ttc"]

        .sum()
    )

    # KPI 2 — FRÉQUENCE D’ACHAT

    frequence_achat = (

        df_ventes

        .groupby("client")

        .size()
    )


    # KPI 3 — CLIENTS RÉCURRENTS

    clients_recurrents = (

        frequence_achat[

            frequence_achat > 1
        ]
    )

    nombre_recurrents = len(clients_recurrents)

  
    # KPI 4 — CLIENTS FORTE VALEUR

    seuil = ca_clients.mean()

    clients_forte_valeur = (

        ca_clients[
            ca_clients > seuil
        ]
    )

    nombre_forte_valeur = len(

        clients_forte_valeur
    )


    # KPI 5 — CLIENT LE PLUS RENTABLE

    meilleur_client = ca_clients.idxmax()

    meilleur_ca = ca_clients.max()

    # KPI LISTE

    liste_kpis = [

        {

            "categorie_kpi":
            "clients",

            "nom_kpi":
            "nombre_clients_recurrents",

            "valeur":
            int(nombre_recurrents),

            "unite":
            "clients",

            "interpretation":
            "Nombre de clients ayant acheté plusieurs fois.",

            "source_donnees":
            ["ventes"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "clients",

            "nom_kpi":
            "nombre_clients_forte_valeur",

            "valeur":
            int(nombre_forte_valeur),

            "unite":
            "clients",

            "interpretation":
            "Clients avec CA supérieur à la moyenne.",

            "source_donnees":
            ["ventes"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        },

        {

            "categorie_kpi":
            "clients",

            "nom_kpi":
            "meilleur_client_ca",

            "valeur":
            float(meilleur_ca),

            "unite":
            "FCFA",

            "interpretation":
            f"Client le plus rentable : {meilleur_client}",

            "source_donnees":
            ["ventes"],

            "date_calcul":
            datetime.now(),

            "version_kpi":
            1
        }
    ]

    # INSERTION KPI

    for kpi in liste_kpis:

        existe = collection_kpis.find_one({

            "nom_kpi":
            kpi["nom_kpi"]
        })

        if not existe:

            collection_kpis.insert_one(kpi)

    print("KPI clients calculés.")