# Mettre le portail en ligne et l'envoyer au consultant

Objectif : votre consultant clique sur un lien et le portail s'ouvre dans son
navigateur — sur ordinateur comme sur téléphone, sans rien installer.

Hébergement : **Streamlit Community Cloud**, gratuit.
Temps : environ 30 minutes la première fois.

---

## Avant de commencer

Rassemblez dans un même dossier, sur votre ordinateur, les cinq éléments
suivants :

| Fichier | D'où il vient |
|---|---|
| `app.py` | votre dossier `Observatoire_Industrie` |
| `jeu_donnees_industrie_guinee_nettoye.xlsx` | le même dossier |
| `simandou.jpg` | le même dossier, **s'il existe** — sinon ignorez cette ligne |
| `requirements.txt` | fourni dans ce kit |
| `README.md` | fourni dans ce kit |
| `.streamlit/config.toml` | fourni dans ce kit — **gardez le dossier `.streamlit`** |
| `.gitignore` | fourni dans ce kit |

> **Pourquoi `.streamlit/config.toml` est important.** En local, `app.py` crée ce
> fichier tout seul au premier lancement. En ligne, l'application ne démarre
> qu'une fois : le fichier serait créé trop tard et le thème de l'observatoire ne
> s'appliquerait pas. En le déposant vous-même, les couleurs sont bonnes dès le
> premier affichage.

---

## Étape 1 — Créer un compte GitHub

1. Allez sur **github.com** et cliquez sur *Sign up*.
2. Utilisez votre adresse `ansoumanetecon@gmail.com`.
3. Confirmez le courriel de validation.

C'est gratuit et cela ne demande aucune carte bancaire.

## Étape 2 — Créer le dépôt

1. Une fois connecté, cliquez sur le **+** en haut à droite, puis
   *New repository*.
2. **Repository name** : `observatoire-industrie-guinee`
3. Laissez **Public** coché.
4. Ne cochez rien d'autre. Cliquez sur *Create repository*.

> **Public ou privé ?** Public est le plus simple et convient ici : le code est
> un prototype de mémoire, pas un système en production. Sachez seulement que
> les identifiants de démonstration (`autorite` / `autorite2025`, etc.) seront
> visibles dans `app.py`. C'est acceptable puisque le portail lui-même indique
> que l'authentification a valeur de démonstration — mais ne réutilisez jamais
> ces mots de passe ailleurs.

## Étape 3 — Déposer les fichiers

1. Sur la page du dépôt vide, cliquez sur *uploading an existing file*.
2. Faites glisser `app.py`, le fichier Excel, `requirements.txt`, `README.md`,
   `.gitignore` et, s'il existe, `simandou.jpg`.
3. Cliquez sur *Commit changes*.

Pour le dossier `.streamlit` :

1. Cliquez sur *Add file* → *Create new file*.
2. Dans la case du nom, tapez exactement : `.streamlit/config.toml`
   (la barre oblique crée le dossier automatiquement).
3. Collez le contenu du `config.toml` fourni dans ce kit.
4. Cliquez sur *Commit changes*.

## Étape 4 — Déployer

1. Allez sur **share.streamlit.io** et connectez-vous **avec GitHub**.
2. Cliquez sur *Create app*, puis *Yup, I have an app*.
3. Renseignez le formulaire :
   - **Repository** : `<votre-nom-github>/observatoire-industrie-guinee`
   - **Branch** : `main`
   - **Main file path** : `app.py`
   - **App URL** : choisissez `observatoire-industrie-guinee`
4. Cliquez sur *Deploy*.

Le premier démarrage prend quelques minutes, le temps d'installer les
dépendances. Vous obtenez une adresse du type :

```
https://observatoire-industrie-guinee.streamlit.app
```

## Étape 5 — Vérifier avant d'envoyer

Ouvrez le lien et contrôlez ces six points :

- [ ] Le fond est beige clair et la barre latérale gris anthracite
- [ ] Le filet rouge-jaune-vert apparaît sous l'en-tête
- [ ] Les graphiques s'affichent avec leurs étiquettes chiffrées
- [ ] La connexion `autorite` / `autorite2025` ouvre bien les 8 pages
- [ ] La page « Qualité des données » affiche les 4 indicateurs incomplets
- [ ] Le bouton de téléchargement CSV fonctionne

Ouvrez aussi le lien depuis votre téléphone : c'est probablement ainsi que votre
consultant le consultera en premier.

---

## Deux choses à savoir

**L'application se met en veille.** Sans visite pendant 12 heures, elle
s'endort. Le visiteur suivant voit un écran d'attente et un bouton pour la
réveiller ; le portail se rouvre en une minute. Prévenez votre consultant, sinon
il croira à une panne.

**Les mises à jour sont automatiques.** Pour corriger quelque chose, remplacez le
fichier concerné sur GitHub : le site en ligne se met à jour tout seul, sans
redéployer. Le lien envoyé au consultant reste valable.

---

## Message à envoyer

> Bonjour [Nom],
>
> Comme convenu, voici le portail web de l'Observatoire National de l'Industrie,
> développé sous Streamlit :
>
> **https://observatoire-industrie-guinee.streamlit.app**
>
> Il est accessible directement depuis un navigateur, sans installation. Trois
> niveaux d'accès sont implémentés, conformément à l'architecture décrite au
> chapitre 3 du mémoire :
>
> - **Grand public** — accès libre, sans connexion (2 pages)
> - **Investisseurs et bailleurs (PTF)** — identifiant `bailleur`, mot de passe
>   `bailleur2025` (5 pages)
> - **Pouvoirs publics** — identifiant `autorite`, mot de passe `autorite2025`
>   (8 pages, dont les analyses avancées et la page qualité des données)
>
> Deux précisions. Les données affichées sont issues du jeu synthétique de
> démonstration (240 observations, 8 régions, 6 secteurs, 2021-2025) : le portail
> est prêt à recevoir les données réelles dès qu'elles seront disponibles.
> L'authentification a valeur d'illustration de la logique d'accès différenciés,
> et non de dispositif de sécurité de production.
>
> Si l'application affiche un écran de mise en veille, un clic suffit à la
> réactiver.
>
> Je reste à votre disposition pour vos observations, en particulier sur les
> sections techniques que vous m'aviez demandées.
>
> Bien cordialement,
> Ansoumane CONTÉ
