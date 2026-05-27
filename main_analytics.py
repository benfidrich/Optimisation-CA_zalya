import os
import sys
import subprocess

# AJOUT RACINE PROJET

sys.path.append(

    os.path.dirname(
        os.path.abspath(__file__)
    )
)


scripts = [

    "analyses/analyse_rentabilite_clients.py",
    "analyses/analyse_rentabilite_services.py",
    "analyses/analyse_performance_commerciale.py",
    "analyses/analyse_conversion.py",
    "analyses/analyse_tendances.py",
    "analyses/analyse_dependance_business.py",
    "analyses/analyse_depenses.py",
    "analyses/analyse_probabilite.py",

    "kpis/kpi_services.py",
    "kpis/kpi_operations.py",
    "kpis/kpi_clients.py",
    "kpis/kpi_devis.py",
    "kpis/kpi_finances.py",
    "kpis/kpi_ventes.py",
    "kpis/kpi_predictions.py"
]

for script in scripts:

    print(f"Exécution : {script}")

    subprocess.run(

        ["python", script],

        cwd="C:/Users/testa/Documents/Zalya_Stage/Scripts"
    )

print("Pipeline analytique terminé.")