import pandas as pd
import numpy as np
from datetime import datetime

#connexion mongodb
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["crm_decisionnel"]
collection_kpis = db["kpis"]

df_crm = pd.read_csv("C:/Users/testa/Documents/Zalya_Stage/DATA/Analyse_prépa1 (1).csv")
#Nombre total d'opportunités
total_opportunites = len(df_crm)
print("Nombre total d'opportunités",total_opportunites)

#Opportunité à forte probablité*
fortes_prob = df_crm[df_crm["Probabilite"] >= 70]
nombre_fortes = len(fortes_prob)
print("Opportunité à forte probablité", nombre_fortes)

#Revenu attendu total
revenu_total = df_crm["Revenu_attendu"].sum()
print("Revenu attendu total", revenu_total)

#Valeur moyenne des opportunités
valeur_moyenne_op = df_crm["Revenu_attendu"].mean()
print("Valeur moyenne des opportunités", valeur_moyenne_op)

#Opportunité par étapes
kpi_etapes = df_crm["Etape"].value_counts()
print("Opportunité par étapes",kpi_etapes)

#Revenu par étape*
revenu_etape = df_crm.groupby("Etape")["Revenu_attendu"].sum()
print("Revenu par étape",revenu_etape)

#Performance par vendeur*
perf_vendeur = df_crm.groupby("Vendeur")["Revenu_attendu"].sum()
print("Performance par vendeur", perf_vendeur)

#Performance par client*
clients = df_crm.groupby("Client")["Revenu_attendu"].sum().sort_values(ascending=False)
print("Performance par client",clients.sort_values(ascending=False))

#Opportunités critiques/non critiques/moyennes
critiques = df_crm[df_crm["Priorite"] == "Haute"]
print("Opportunités critiques",len(critiques))
non_critique = df_crm[df_crm["Priorite"] =="Basse"]
print("Opportunités non critiques",len(non_critique))
moyenne = df_crm[df_crm["Priorite"] =="Moyenne"]
print("Opportunités critiques",len(moyenne))

#Taux d'opportunité gagnée/perdue
taux_gp = df_crm["Gagnee_Perdue"].value_counts(normalize=True) * 100
print("Taux d'opportunité gagnée/perdue",taux_gp)

#Taux de conversion
op_gagnees = len(df_crm[df_crm["Gagnee_Perdue"] == "Gagné"])
taux_conversion = (op_gagnees / total_opportunites) * 100
print("Taux de conversion :", taux_conversion)

kpi_document = {

    "date_calul": datetime.now(),

    "total_opportunites": total_opportunites,

    "revenu_attendu_total": float(revenu_total),

    "valeur_moyenne_opportunite": float(valeur_moyenne_op),

    "opportunites_fortes_probabilites": nombre_fortes,

    "opportunites_critiques": len(critiques),

    "opportunites_non_critiques": len(non_critique),

    "opportunites_moyennes": len(moyenne),

    "Opportunité_par _étapes": kpi_etapes.to_dict(),

    "Revenu_par_étape": revenu_etape.to_dict(),

    "Performance_par _vendeur": perf_vendeur.to_dict(),

    "Performance_par_client": clients.to_dict(),

    "Taux d'opportunité gagnée/perdue": taux_gp.to_dict(),

    "Taux de conversion": taux_conversion
}

#Insertion dans mongodb
collection_kpis.insert_one(kpi_document)