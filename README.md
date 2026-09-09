# Observatoire National de l'Industrie de Guinée — portail décisionnel

Prototype du système d'information décisionnel (SID) de l'Observatoire National
de l'Industrie de Guinée.

Mémoire de Master 2 — Statistique et Informatique Décisionnelle
Ansoumane CONTÉ · Université Alioune Diop de Bambey
Directeur de mémoire : Pr Fodé CAMARA

---

## Ce que fait le portail

Huit pages couvrant la chaîne complète d'un observatoire industriel :

| Page | Contenu |
|---|---|
| Accueil | Indicateurs clés, chiffre d'affaires par région et par secteur, évolution |
| L'Observatoire | Mission, architecture en 4 couches, sources, conventions territoriales, règles d'accès |
| Analyse régionale & sectorielle | Comparaison des territoires et des branches, croisement région × secteur |
| Fiche régionale | Profil industriel d'un territoire, positionnement national |
| Dimensions complémentaires | Emploi, production, environnement, transformation numérique |
| Analyse avancée | Matrice de corrélation, segmentation des régions (k-means, 3 profils) |
| Qualité des données | Complétude par indicateur — volet gouvernance |
| Données & indicateurs | Table complète, export CSV, dictionnaire des variables |

Les analyses sont conduites à deux mailles territoriales : les 8 régions
administratives et les 4 régions naturelles.

## Accès différenciés

Le portail applique les trois niveaux d'accès décrits au chapitre 3.1.4 du mémoire.

| Profil | Accès | Périmètre |
|---|---|---|
| Grand public | Libre, sans connexion | 2 pages — données agrégées et présentation |
| Investisseurs et bailleurs (PTF) | Sur inscription | 5 pages — analyses détaillées |
| Pouvoirs publics | Authentifié | 8 pages — analyses avancées, qualité, export |

**Comptes de démonstration**

| Identifiant | Mot de passe | Profil |
|---|---|---|
| `investisseur` | `invest2025` | Investisseurs et bailleurs (PTF) |
| `bailleur` | `bailleur2025` | Investisseurs et bailleurs (PTF) |
| `autorite` | `autorite2025` | Pouvoirs publics |

Le mécanisme d'authentification a valeur de **démonstration** : il illustre la
logique d'accès différenciés de l'architecture, sans constituer un dispositif de
sécurité de niveau production.

## Note méthodologique

Les données de ce prototype sont issues d'un **jeu synthétique** construit pour
la démonstration (240 observations, 8 régions, 6 secteurs, 2021-2025). Elles ne
constituent pas des statistiques officielles.

Le portail est prêt à recevoir des données réelles : si les noms de colonnes sont
identiques, il suffit de remplacer le fichier Excel. Sinon, le dictionnaire
`LIBELLES` en tête de `app.py` est à adapter.

## Contenu du dépôt

```
app.py                                       application Streamlit
jeu_donnees_industrie_guinee_nettoye.xlsx    jeu de données
requirements.txt                             dépendances
.streamlit/config.toml                       thème de l'observatoire
simandou.jpg                                 visuel de bas de page (facultatif)
```

## Exécution en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Choix technique

Streamlit a été retenu pour la couche de diffusion : il couvre le cœur
décisionnel (interrogation des données, visualisations, analyses statistiques,
accès différenciés) avec une chaîne Python unique, de la préparation des données
à la publication. Un CMS institutionnel — actualités, forum, newsletter,
arborescence à plusieurs niveaux — relève d'une phase ultérieure et est traité
en perspective du mémoire.
