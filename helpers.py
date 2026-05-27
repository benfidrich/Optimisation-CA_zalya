from datetime import datetime

def convertir_float(valeur):

    try:
        return float(valeur)

    except:
        return 0.0

# INSERTION SÉCURISÉE
def analyse_existe(

    collection,
    type_analyse,
    identifiant
):
    return collection.find_one({

        "type_analyse": type_analyse,

        "identifiant": identifiant
    })

# DATE ACTUELLE
def maintenant():

    return datetime.now()