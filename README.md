# maison-ayras.com

Site vitrine statique (FR / EN / NL) de la Maison d'Ayras, maison de campagne avec piscine à Cosnac (Corrèze). Toutes les réservations passent par Airbnb.

- `build.py` : tous les textes (dictionnaire `T`, une entrée par langue). Il génère `docs/index.html`, `docs/en/index.html` et `docs/nl/index.html`. Après une modification de texte : `python3 build.py`.
- `docs/` : le site publié par GitHub Pages (branche `main`, dossier `/docs`).
- `docs/img/` : photos en WebP (versions `-s` pour les vignettes).
- `docs/CNAME` : domaine personnalisé `www.maison-ayras.com`.
- À confirmer : l'adresse e-mail (constante `EMAIL` dans `build.py`).
