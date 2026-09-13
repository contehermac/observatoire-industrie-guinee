# -*- coding: utf-8 -*-
"""
ETL de l'Observatoire national de l'industrie de Guinee (ONIG)
---------------------------------------------------------------
Alimente l'entrepot de donnees decrit en 4.1.2 du memoire :
schema en etoile, table de faits Fait_industrie au grain
region x secteur x annee, reliee aux dimensions Region, Secteur et Annee.

Les trois etapes correspondent aux couches 1 a 3 de l'architecture
presentee en 4.1.1 :
    E - Extraction    : lecture du fichier source brut
    T - Transformation: nettoyage et normalisation
    L - Chargement    : ecriture dans l'entrepot SQLite

Aucune valeur n'est creee : les mesures sont recopiees telles quelles,
seules les valeurs corrompues sont mises a vide.
"""

import datetime
import os
import sqlite3

import pandas as pd

FICHIER_SOURCE = "jeu_donnees_industrie_guinee_synthetique.xlsx"
ENTREPOT = "observatoire.db"

# Les 14 colonnes numeriques affectees par la corruption d'export
COLONNES_NUMERIQUES = [
    "indice_production_industrielle", "chiffre_affaires_milliards_gnf",
    "valeur_ajoutee_milliards_gnf", "exportations_milliards_gnf",
    "investissement_milliards_gnf", "consommation_energie_mwh",
    "consommation_eau_m3", "jours_arret_production",
    "coupures_electricite_heures", "taux_utilisation_capacite_pct",
    "part_femmes_emploi_pct", "emissions_co2_tonnes",
    "conformite_fiscale_pct", "maturite_numerique_score_100",
]

# Les 3 colonnes entieres non affectees
COLONNES_ENTIERES = [
    "nb_entreprises_actives", "emploi_direct", "accidents_travail_declares",
]

# Rattachement des 8 regions administratives aux 4 regions naturelles
REGIONS_NATURELLES = {
    "Conakry": "Basse-Guinée", "Boke": "Basse-Guinée", "Kindia": "Basse-Guinée",
    "Labe": "Moyenne-Guinée", "Mamou": "Moyenne-Guinée",
    "Kankan": "Haute-Guinée", "Faranah": "Haute-Guinée",
    "Nzerekore": "Guinée forestière",
}


def sans_accents(texte):
    """Cle de rapprochement insensible aux accents (Boke / Boké)."""
    import unicodedata
    return "".join(
        c for c in unicodedata.normalize("NFD", str(texte))
        if unicodedata.category(c) != "Mn"
    )


# ---------------------------------------------------------------- E
def extraire(chemin):
    """Lecture du fichier source brut, tel que recu du producteur."""
    df = pd.read_excel(chemin)
    print(f"[E] {len(df)} lignes extraites de {os.path.basename(chemin)}")
    return df


# ---------------------------------------------------------------- T
def valeur_numerique(v):
    """Convertit en reel ; met a vide toute valeur corrompue en date."""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def transformer(df):
    """Nettoyage, typage et controles de coherence."""
    f = df.copy()

    for col in COLONNES_NUMERIQUES:
        f[col] = f[col].apply(valeur_numerique)

    total = len(f) * len(COLONNES_NUMERIQUES)
    vides = int(f[COLONNES_NUMERIQUES].isna().sum().sum())
    print(f"[T] {vides} / {total} cellules mises à vide ({100 * vides / total:.1f}%)")

    doublons = int(f.duplicated(subset=["annee", "region", "secteur_industriel"]).sum())
    print(f"[T] doublons sur la clé région x secteur x année : {doublons}")

    for col in ["taux_utilisation_capacite_pct", "part_femmes_emploi_pct",
                "conformite_fiscale_pct"]:
        hors = int(f[(f[col] < 0) | (f[col] > 100)][col].count())
        if hors:
            print(f"[T] ATTENTION {col} : {hors} valeurs hors [0,100]")

    return f


# ---------------------------------------------------------------- L
def creer_schema(con):
    """Cree les tables du schema en etoile (4.1.2)."""
    con.executescript("""
    DROP TABLE IF EXISTS Fait_industrie;
    DROP TABLE IF EXISTS Dim_Region;
    DROP TABLE IF EXISTS Dim_Secteur;
    DROP TABLE IF EXISTS Dim_Annee;

    CREATE TABLE Dim_Region (
        id_region        INTEGER PRIMARY KEY,
        libelle_region   TEXT NOT NULL UNIQUE,
        region_naturelle TEXT NOT NULL
    );

    CREATE TABLE Dim_Secteur (
        id_secteur       INTEGER PRIMARY KEY,
        libelle_secteur  TEXT NOT NULL UNIQUE
    );

    CREATE TABLE Dim_Annee (
        id_annee         INTEGER PRIMARY KEY,
        annee            INTEGER NOT NULL UNIQUE
    );

    CREATE TABLE Fait_industrie (
        id_region                       INTEGER NOT NULL,
        id_secteur                      INTEGER NOT NULL,
        id_annee                        INTEGER NOT NULL,
        nb_entreprises_actives          INTEGER,
        emploi_direct                   INTEGER,
        accidents_travail_declares      INTEGER,
        indice_production_industrielle  REAL,
        chiffre_affaires_milliards_gnf  REAL,
        valeur_ajoutee_milliards_gnf    REAL,
        exportations_milliards_gnf      REAL,
        investissement_milliards_gnf    REAL,
        consommation_energie_mwh        REAL,
        consommation_eau_m3             REAL,
        jours_arret_production          REAL,
        coupures_electricite_heures     REAL,
        taux_utilisation_capacite_pct   REAL,
        part_femmes_emploi_pct          REAL,
        emissions_co2_tonnes            REAL,
        conformite_fiscale_pct          REAL,
        maturite_numerique_score_100    REAL,
        PRIMARY KEY (id_region, id_secteur, id_annee),
        FOREIGN KEY (id_region)  REFERENCES Dim_Region(id_region),
        FOREIGN KEY (id_secteur) REFERENCES Dim_Secteur(id_secteur),
        FOREIGN KEY (id_annee)   REFERENCES Dim_Annee(id_annee)
    );
    """)


def charger(f, chemin_entrepot):
    con = sqlite3.connect(chemin_entrepot)
    con.execute("PRAGMA foreign_keys = ON;")
    creer_schema(con)

    regions = sorted(f["region"].unique())
    dim_region = pd.DataFrame({
        "id_region": range(1, len(regions) + 1),
        "libelle_region": regions,
        "region_naturelle": [REGIONS_NATURELLES[sans_accents(r)] for r in regions],
    })

    secteurs = sorted(f["secteur_industriel"].unique())
    dim_secteur = pd.DataFrame({
        "id_secteur": range(1, len(secteurs) + 1),
        "libelle_secteur": secteurs,
    })

    annees = sorted(f["annee"].unique())
    dim_annee = pd.DataFrame({
        "id_annee": range(1, len(annees) + 1),
        "annee": annees,
    })

    dim_region.to_sql("Dim_Region", con, if_exists="append", index=False)
    dim_secteur.to_sql("Dim_Secteur", con, if_exists="append", index=False)
    dim_annee.to_sql("Dim_Annee", con, if_exists="append", index=False)

    faits = f.merge(dim_region[["id_region", "libelle_region"]],
                    left_on="region", right_on="libelle_region")
    faits = faits.merge(dim_secteur, left_on="secteur_industriel",
                        right_on="libelle_secteur")
    faits = faits.merge(dim_annee, left_on="annee", right_on="annee")

    colonnes = (["id_region", "id_secteur", "id_annee"]
                + COLONNES_ENTIERES + COLONNES_NUMERIQUES)
    faits = faits[colonnes]
    faits.to_sql("Fait_industrie", con, if_exists="append", index=False)

    con.commit()
    print(f"[L] {len(dim_region)} régions, {len(dim_secteur)} secteurs, "
          f"{len(dim_annee)} années, {len(faits)} faits chargés dans {chemin_entrepot}")
    return con


# ---------------------------------------------------------------- controle
def controler(con, f):
    """Vérifie que l'entrepôt restitue exactement les valeurs sources."""
    print("\n--- Contrôle de non-altération ---")
    req = """
        SELECT SUM(nb_entreprises_actives), SUM(emploi_direct),
               ROUND(SUM(chiffre_affaires_milliards_gnf))
        FROM Fait_industrie fi
        JOIN Dim_Annee da ON da.id_annee = fi.id_annee
        WHERE da.annee = 2025;
    """
    ent, emp, ca = con.execute(req).fetchone()
    src = f[f["annee"] == 2025]
    ok = (ent == src["nb_entreprises_actives"].sum()
          and emp == src["emploi_direct"].sum()
          and ca == round(src["chiffre_affaires_milliards_gnf"].sum()))
    print(f"2025 - entreprises : {ent} | emploi : {emp} | CA : {ca} Mds GNF")
    print("Entrepôt conforme au fichier source." if ok else "ÉCART DÉTECTÉ")
    return ok


if __name__ == "__main__":
    brut = extraire(FICHIER_SOURCE)
    propre = transformer(brut)
    connexion = charger(propre, ENTREPOT)
    controler(connexion, propre)
    connexion.close()
