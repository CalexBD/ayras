#!/usr/bin/env python3
"""Génère site/index.html (FR), site/en/index.html, site/nl/index.html à partir d'un seul gabarit."""
import html, json, os

ROOT = os.path.join(os.path.dirname(__file__), "docs")
DOMAIN = "https://www.maison-ayras.com"
EMAIL = "contact@maison-ayras.com"  # à confirmer
LISTING_ID = "51479937"
AIRBNB = {"fr": f"https://www.airbnb.fr/rooms/{LISTING_ID}",
          "en": f"https://www.airbnb.com/rooms/{LISTING_ID}",
          "nl": f"https://www.airbnb.nl/rooms/{LISTING_ID}"}
PATHS = {"fr": "", "en": "en/", "nl": "nl/"}

# Photos : (fichier, légende FR, EN, NL, classe de mise en page dans la galerie)
PHOTOS = [
    ("exterieur-1", "La maison, côté cour", "The house from the courtyard", "Het huis vanaf de binnenplaats", "wide"),
    ("piscine", "La piscine clôturée", "The fenced pool", "Het omheinde zwembad", ""),
    ("jardin", "Le jardin", "The garden", "De tuin", ""),
    ("exterieur-2", "La maison et la cour", "The house and courtyard", "Het huis en de binnenplaats", ""),
    ("repas-1", "La salle à manger", "The dining room", "De eetkamer", ""),
    ("salon-1", "Le salon et le billard", "The living room and pool table", "De woonkamer met biljart", "wide"),
    ("cuisine-1", "La cuisine", "The kitchen", "De keuken", ""),
    ("cuisine-2", "La cuisine", "The kitchen", "De keuken", ""),
    ("salon-2", "Le salon", "The living room", "De woonkamer", ""),
    ("extra-1", "Le salon", "The living room", "De woonkamer", ""),
    ("ch1-1", "Chambre 1", "Bedroom 1", "Slaapkamer 1", ""),
    ("ch1-2", "Chambre 1", "Bedroom 1", "Slaapkamer 1", ""),
    ("ch2-1", "Chambre 2", "Bedroom 2", "Slaapkamer 2", ""),
    ("ch2-2", "Chambre 2", "Bedroom 2", "Slaapkamer 2", ""),
    ("ch3-1", "Chambre 3", "Bedroom 3", "Slaapkamer 3", ""),
    ("ch3-2", "Chambre 3", "Bedroom 3", "Slaapkamer 3", ""),
    ("ch4-1", "Chambre 4", "Bedroom 4", "Slaapkamer 4", ""),
    ("ch4-2", "Chambre 4", "Bedroom 4", "Slaapkamer 4", ""),
    ("sdb-ch4", "Salle d'eau de la chambre 4", "Bedroom 4 en-suite", "Badkamer van slaapkamer 4", "tall"),
    ("sdb-etage", "Salle de bain de l'étage", "Upstairs bathroom", "Badkamer boven", ""),
    ("sdb-rdc", "Salle d'eau du rez-de-chaussée", "Ground-floor shower room", "Doucheruimte beneden", "tall"),
    ("repas-2", "L'entrée", "The entrance", "De hal", "tall"),
    ("cellier", "Le cellier", "The utility room", "De bijkeuken", "tall"),
]
LANG_IDX = {"fr": 1, "en": 2, "nl": 3}

# Chambres : (photo, [largeurs de lits en cm], couchages, clé des notes)
ROOMS_UP = [("ch1-1", [140, 90], 3, "r1"), ("ch2-1", [120, 90, 90], 3, "r2"),
            ("ch3-1", [140], 2, "r3"), ("ch4-1", [160], 2, "r4")]
ROOM_DOWN = ("salon-1", [140], 2, "r5")

# Données structurées (schema.org VacationRental)
# Point approximatif (centre de Cosnac), pas l'emplacement exact de la maison.
GEO = (45.13471, 1.58461)
BED_TYPES = {90: "Single", 120: "SemiDouble", 140: "Double", 160: "Queen"}


def beds_jsonld():
    counts = {}
    for r in ROOMS_UP + [ROOM_DOWN]:
        for w in r[1]:
            counts[BED_TYPES[w]] = counts.get(BED_TYPES[w], 0) + 1
    return [{"@type": "BedDetails", "typeOfBed": k, "numberOfBeds": n} for k, n in counts.items()]

T = {
"fr": {
  "html_lang": "fr", "locale": "fr_FR",
  "title": "Maison d'Ayras · Maison de campagne avec piscine pour 12, près de Brive",
  "desc": "Maison de pierre à Cosnac (Corrèze), à 10 minutes de Brive-la-Gaillarde : 4 chambres, 12 voyageurs, piscine clôturée, billard, grand jardin. Location de mi-mai à fin septembre.",
  "nav": [("maison", "La maison"), ("couchages", "Qui dort où"), ("photos", "Photos"), ("avis", "Avis"), ("autour", "Autour"), ("infos", "Infos pratiques")],
  "menu": "Menu", "book": "Réserver",
  "h1": "Une maison de caractère.",
  "hero_sub": "Une maison de pierre avec piscine pour 12 personnes, à Cosnac en Corrèze, à 10 minutes de Brive-la-Gaillarde. Ouverte de mi-mai à fin septembre.",
  "rating": "sur 5, d'après 51 avis Airbnb",
  "cta_dispo": "Voir les disponibilités", "cta_discover": "Découvrir la maison",
  "facts": [("12", "voyageurs"), ("4", "chambres"), ("3", "salles de bain"), ("1", "piscine clôturée"), ("1", "billard"), ("Wifi", "par la fibre")],
  "house_h2": "Une vraie maison de famille",
  "house_p": ["Une maison de campagne au calme, en pierre, avec un grand jardin et une piscine privée. Elle est pensée pour réunir une famille ou une bande d'amis : de grandes chambres, une grande table et de quoi occuper tout le monde.",
              "Au rez-de-chaussée, la cuisine équipée et son cellier, une salle à manger aux murs de pierre et un salon avec billard. À l'étage, quatre grandes chambres. Les chambres à l'arrière de la maison sont de plain-pied avec le jardin et y ouvrent directement."],
  "reasons": [("La piscine, en toute tranquillité", "Privée, clôturée et fermée à clé. Ouverte de juin à septembre."),
              ("Un grand jardin", "De la place pour les jeux, les siestes et les dîners dehors."),
              ("Les soirées aussi", "Billard, télévision et jeux de société dans un salon séparé."),
              ("Le télétravail possible", "Wifi par la fibre et un bureau dans trois des chambres.")],
  "alt_house": ["La piscine clôturée et le jardin", "La salle à manger aux murs de pierre", "Le salon avec billard"],
  "sleep_h2": "Qui dort où",
  "sleep_p": "Quatre chambres à l'étage et un canapé-lit au salon. Chaque lit est dessiné à sa largeur réelle.",
  "total": "couchages au total",
  "floor_up": "À l'étage", "floor_down": "Au rez-de-chaussée",
  "room_names": {"r1": "Chambre 1", "r2": "Chambre 2", "r3": "Chambre 3", "r4": "Chambre 4", "r5": "Salon"},
  "room_notes": {"r1": ["Bureau"], "r2": [], "r3": ["Bureau"], "r4": ["Bureau", "Salle d'eau privée (douche et WC)"], "r5": ["Canapé convertible", "Billard et télévision"]},
  "sleeps": "{n} couchages",
  "bed": "lit {w}", "sofa": "canapé {w}",
  "bath_note": "Trois salles de bain : une salle d'eau privée dans la chambre 4, une salle de bain à l'étage (baignoire, WC et bidet) et une salle d'eau au rez-de-chaussée (douche à l'italienne et WC). Draps et serviettes de bain sont fournis.",
  "living_h2": "Les pièces à vivre",
  "living": [("cuisine-1", "La cuisine", "Gazinière, four, hotte, lave-vaisselle, micro-ondes, réfrigérateur-congélateur, machine Nespresso, bouilloire et grille-pain. Un cellier juste à côté, avec le lave-linge."),
             ("repas-1", "La salle à manger", "Une grande table sous les poutres, entre les murs de pierre. Assez de place pour tout le monde."),
             ("salon-2", "Le salon", "Un salon séparé avec billard, télévision, canapé et jeux de société, qui ouvre sur l'extérieur.")],
  "photos_h2": "Toutes les photos", "photos_p": "Touchez une photo pour l'agrandir.",
  "lb_close": "Fermer", "lb_prev": "Photo précédente", "lb_next": "Photo suivante",
  "reviews_h2": "Ce qu'en disent les voyageurs",
  "reviews_badge": "Coup de cœur voyageurs sur Airbnb, d'après 51 avis",
  "scores": [("Propreté", "4,9"), ("Précision", "4,9"), ("Arrivée", "5,0"), ("Communication", "5,0"), ("Emplacement", "4,8"), ("Qualité-prix", "4,8")],
  "score": "4,98",
  "quotes": [
    ("Logement idéal pour les familles ! L'environnement est paisible. Nous avons vécu une semaine à 7 dans ce gîte très agréable, profité du calme, de la piscine et de tout le confort proposé.", "Mathieu, août 2026, séjour d'une semaine"),
    ("Le logement était en parfait état ! Mieux que sur les photos. Les chambres sont spacieuses et le ménage impeccable. La piscine est fermée à clef, ce qui assure aussi la sécurité des enfants !", "Emilie, juillet 2026, séjour entre amis"),
    ("Jolie maison bien entretenue, avec un grand espace extérieur et de grandes chambres. Il y a tout ce dont on a besoin. Nous avons profité de la piscine, et le billard nous a beaucoup plu également.", "Charlotte, août 2026, séjour d'une semaine"),
    ("On a passé un super week-end qui nous a permis de réunir toute la famille ! On y retournera certainement pour continuer à visiter cette magnifique région.", "Eric, août 2026, week-end en famille")],
  "translated": "",
  "reviews_more": "Lire les 51 avis sur Airbnb",
  "around_h2": "Autour de la maison",
  "around_p": "La maison est à la rencontre de la Corrèze, du Lot et de la Dordogne. La plupart des grands sites de la région sont à moins d'une heure de route.",
  "places": [("Brive-la-Gaillarde", "Centre ancien, marchés, commerces", "10 min"),
             ("Turenne", "Village perché et son château", "20 min"),
             ("Collonges-la-Rouge", "Village de grès rouge, parmi les plus beaux de France", "25 min"),
             ("Lac du Causse", "Baignade surveillée l'été, activités nautiques", "30 min"),
             ("Gouffre de Padirac", "Rivière souterraine en barque", "50 min"),
             ("Rocamadour", "Cité sanctuaire à flanc de falaise", "50 min"),
             ("Sarlat-la-Canéda", "Cité médiévale du Périgord noir", "1 h")],
  "places_note": "Temps de trajet indicatifs en voiture.",
  "getting_h3": "Venir à la maison",
  "getting_p": "En voiture par l'A20 ou l'A89, sortie Brive. En train jusqu'à la gare de Brive-la-Gaillarde, ou en avion jusqu'à l'aéroport Brive–Vallée de la Dordogne, tous deux à environ 15 minutes. Une voiture reste indispensable sur place.",
  "faq_h2": "Infos pratiques",
  "faq": [("Comment réserver ?", "Les réservations, le paiement et les conditions d'annulation passent par Airbnb. Le bouton « Voir les disponibilités » vous y emmène directement, avec les tarifs à jour pour vos dates."),
          ("Quelles sont les dates d'ouverture ?", "La maison se loue de mi-mai à fin septembre."),
          ("Comment se passe l'arrivée ?", "Arrivée à partir de 17 h, en autonomie grâce à une boîte à clés sécurisée : vous arrivez à l'heure qui vous convient. Départ avant 10 h."),
          ("La piscine est-elle sécurisée ?", "Oui. Elle est privée, entourée d'une clôture et fermée à clé. Elle est ouverte de juin à septembre : pour un séjour en mai, elle n'est pas encore en service."),
          ("Où se garer ?", "Dans la grande cour devant la maison, où plusieurs voitures tiennent sans difficulté."),
          ("Le linge est-il fourni ?", "Oui, les draps et les serviettes de bain sont inclus."),
          ("Peut-on organiser une fête ?", "La maison accueille les séjours en famille ou entre amis, mais les soirées et les fêtes ne sont pas autorisées."),
          ("Peut-on y travailler ?", "Oui : le wifi passe par la fibre, et trois chambres ont un bureau."),
          ("Et pour les courses ?", "Les supermarchés de Brive sont à une dizaine de minutes en voiture.")],
  "book_h2": "Vos dates, en quelques clics",
  "book_p": "Les disponibilités et les tarifs sont tenus à jour sur Airbnb, où se font la réservation et le paiement sécurisé.",
  "book_btn": "Voir les disponibilités sur Airbnb",
  "contact": "Une question avant de réserver ? Écrivez-nous à",
  "footer": "Maison de campagne avec piscine à Cosnac, en Corrèze. Location saisonnière de mi-mai à fin septembre.",
},
"en": {
  "html_lang": "en", "locale": "en_GB",
  "title": "Maison d'Ayras · Stone country house with pool for 12, near Brive, France",
  "desc": "Stone country house in Cosnac (Corrèze, south-west France), 10 minutes from Brive-la-Gaillarde: 4 bedrooms, sleeps 12, fenced private pool, pool table, large garden. Available mid-May to end of September.",
  "nav": [("maison", "The house"), ("couchages", "Sleeping"), ("photos", "Photos"), ("avis", "Reviews"), ("autour", "Nearby"), ("infos", "Good to know")],
  "menu": "Menu", "book": "Book",
  "h1": "A house with character.",
  "hero_sub": "A stone house with a private pool for 12 guests in Cosnac, Corrèze, 10 minutes from Brive-la-Gaillarde in south-west France. Open from mid-May to the end of September.",
  "rating": "out of 5, from 51 Airbnb reviews",
  "cta_dispo": "Check availability", "cta_discover": "See the house",
  "facts": [("12", "guests"), ("4", "bedrooms"), ("3", "bathrooms"), ("1", "fenced pool"), ("1", "pool table"), ("Wi-Fi", "via fibre")],
  "house_h2": "A proper family house",
  "house_p": ["A quiet stone country house with a large garden and a private pool. It's made for bringing a family or a group of friends together: big bedrooms, a big table, and plenty to keep everyone busy.",
              "Downstairs, the fitted kitchen with its utility room, a stone-walled dining room and a living room with a pool table. Upstairs, four large bedrooms. The bedrooms at the back of the house are level with the garden and open straight onto it."],
  "reasons": [("A pool you can relax around", "Private, fenced and locked. Open from June to September."),
              ("A big garden", "Room for games, naps and dinners outside."),
              ("Evenings sorted too", "Pool table, TV and board games in a separate living room."),
              ("Remote work welcome", "Fibre Wi-Fi and a desk in three of the bedrooms.")],
  "alt_house": ["The fenced pool and garden", "The stone-walled dining room", "The living room with pool table"],
  "sleep_h2": "Who sleeps where",
  "sleep_p": "Four bedrooms upstairs and a sofa bed in the living room. Each bed is drawn to its real width.",
  "total": "places to sleep",
  "floor_up": "Upstairs", "floor_down": "Ground floor",
  "room_names": {"r1": "Bedroom 1", "r2": "Bedroom 2", "r3": "Bedroom 3", "r4": "Bedroom 4", "r5": "Living room"},
  "room_notes": {"r1": ["Desk"], "r2": [], "r3": ["Desk"], "r4": ["Desk", "Private shower room with WC"], "r5": ["Sofa bed", "Pool table and TV"]},
  "sleeps": "sleeps {n}",
  "bed": "{w} cm bed", "sofa": "{w} cm sofa",
  "bath_note": "Three bathrooms: a private shower room in bedroom 4, an upstairs bathroom (bath, WC and bidet) and a ground-floor shower room (walk-in shower and WC). Bed linen and bath towels are provided.",
  "living_h2": "Living spaces",
  "living": [("cuisine-1", "The kitchen", "Gas hob, oven, extractor hood, dishwasher, microwave, fridge-freezer, Nespresso machine, kettle and toaster. A utility room next door with the washing machine."),
             ("repas-1", "The dining room", "A big table under the beams, between old stone walls. Room for everyone."),
             ("salon-2", "The living room", "A separate living room with pool table, TV, sofa and board games, opening onto the outside.")],
  "photos_h2": "All photos", "photos_p": "Tap a photo to enlarge it.",
  "lb_close": "Close", "lb_prev": "Previous photo", "lb_next": "Next photo",
  "reviews_h2": "What guests say",
  "reviews_badge": "Airbnb Guest Favourite, based on 51 reviews",
  "scores": [("Cleanliness", "4.9"), ("Accuracy", "4.9"), ("Check-in", "5.0"), ("Communication", "5.0"), ("Location", "4.8"), ("Value", "4.8")],
  "score": "4.98",
  "quotes": [
    ("Ideal for families! The surroundings are peaceful. Seven of us spent a week in this lovely house, enjoying the quiet, the pool and all the comforts on offer.", "Mathieu, August 2026, one-week stay"),
    ("The house was in perfect condition, even better than the photos. The bedrooms are spacious and the cleaning spotless. The pool is locked, which also keeps children safe!", "Emilie, July 2026, stay with friends"),
    ("A pretty, well-kept house with a large outdoor space and big bedrooms. It has everything you need. We made the most of the pool, and we loved the pool table too.", "Charlotte, August 2026, one-week stay"),
    ("We had a great weekend that brought the whole family together! We'll certainly be back to keep exploring this beautiful area.", "Eric, August 2026, family weekend")],
  "translated": "Reviews translated from French.",
  "reviews_more": "Read all 51 reviews on Airbnb",
  "around_h2": "Around the house",
  "around_p": "The house sits where Corrèze, the Lot and the Dordogne meet. Most of the region's highlights are less than an hour's drive away.",
  "places": [("Brive-la-Gaillarde", "Old town, markets and shops", "10 min"),
             ("Turenne", "Hilltop village and castle", "20 min"),
             ("Collonges-la-Rouge", "Red sandstone village, one of France's most beautiful", "25 min"),
             ("Lac du Causse", "Lifeguarded swimming in summer, water sports", "30 min"),
             ("Gouffre de Padirac", "Underground river by boat", "50 min"),
             ("Rocamadour", "Pilgrimage town clinging to a cliff", "50 min"),
             ("Sarlat-la-Canéda", "Medieval town in the Périgord Noir", "1 h")],
  "places_note": "Approximate driving times.",
  "getting_h3": "Getting here",
  "getting_p": "By car via the A20 or A89 motorways, Brive exit. By train to Brive-la-Gaillarde station, or by plane to Brive–Vallée de la Dordogne airport, both about 15 minutes away. You'll need a car once you're here.",
  "faq_h2": "Good to know",
  "faq": [("How do I book?", "Bookings, payment and cancellation terms are handled by Airbnb. The “Check availability” button takes you straight there, with up-to-date prices for your dates."),
          ("When is the house available?", "The house is let from mid-May to the end of September."),
          ("How does check-in work?", "Check-in from 5 pm, on your own with a secure key box, so you can arrive whenever suits you. Check-out by 10 am."),
          ("Is the pool safe for children?", "Yes. It's private, fenced and locked. It's open from June to September, so it isn't running yet for stays in May."),
          ("Where do we park?", "In the large courtyard in front of the house, which easily takes several cars."),
          ("Is linen provided?", "Yes, bed linen and bath towels are included."),
          ("Can we hold a party?", "The house welcomes families and groups of friends, but parties and events aren't allowed."),
          ("Can I work from the house?", "Yes: the Wi-Fi runs on fibre, and three bedrooms have a desk."),
          ("Where can we shop?", "Supermarkets in Brive are about ten minutes away by car.")],
  "book_h2": "Your dates, in a few clicks",
  "book_p": "Availability and prices are kept up to date on Airbnb, where you book and pay securely.",
  "book_btn": "Check availability on Airbnb",
  "contact": "A question before you book? Email us at",
  "footer": "Country house with pool in Cosnac, Corrèze, France. Holiday let from mid-May to the end of September.",
},
"nl": {
  "html_lang": "nl", "locale": "nl_NL",
  "title": "Maison d'Ayras · Stenen landhuis met zwembad voor 12 personen, bij Brive (Frankrijk)",
  "desc": "Stenen landhuis in Cosnac (Corrèze), op 10 minuten van Brive-la-Gaillarde: 4 slaapkamers, 12 personen, omheind privézwembad, biljart, grote tuin. Te huur van half mei tot eind september.",
  "nav": [("maison", "Het huis"), ("couchages", "Slapen"), ("photos", "Foto's"), ("avis", "Reviews"), ("autour", "Omgeving"), ("infos", "Praktisch")],
  "menu": "Menu", "book": "Boeken",
  "h1": "Een huis met karakter.",
  "hero_sub": "Een stenen huis met eigen zwembad voor 12 personen in Cosnac, in de Corrèze, op 10 minuten van Brive-la-Gaillarde. Te huur van half mei tot eind september.",
  "rating": "van 5, op basis van 51 Airbnb-reviews",
  "cta_dispo": "Bekijk beschikbaarheid", "cta_discover": "Ontdek het huis",
  "facts": [("12", "gasten"), ("4", "slaapkamers"), ("3", "badkamers"), ("1", "omheind zwembad"), ("1", "biljart"), ("Wifi", "via glasvezel")],
  "house_h2": "Een echt familiehuis",
  "house_p": ["Een rustig gelegen stenen landhuis met een grote tuin en een eigen zwembad. Gemaakt om familie of vrienden samen te brengen: grote slaapkamers, een grote tafel en genoeg te doen voor iedereen.",
              "Beneden de ingerichte keuken met bijkeuken, een eetkamer met stenen muren en een woonkamer met biljart. Boven vier grote slaapkamers. De slaapkamers aan de achterkant liggen gelijkvloers met de tuin en komen er direct op uit."],
  "reasons": [("Zorgeloos zwemmen", "Privé, omheind en afgesloten. Open van juni tot en met september."),
              ("Een grote tuin", "Ruimte voor spelletjes, middagdutjes en buiten eten."),
              ("Ook 's avonds vermaak", "Biljart, televisie en gezelschapsspellen in een aparte woonkamer."),
              ("Thuiswerken kan", "Glasvezel-wifi en een bureau in drie van de slaapkamers.")],
  "alt_house": ["Het omheinde zwembad en de tuin", "De eetkamer met stenen muren", "De woonkamer met biljart"],
  "sleep_h2": "Wie slaapt waar",
  "sleep_p": "Vier slaapkamers boven en een slaapbank in de woonkamer. Elk bed is op ware breedte getekend.",
  "total": "slaapplaatsen in totaal",
  "floor_up": "Boven", "floor_down": "Begane grond",
  "room_names": {"r1": "Slaapkamer 1", "r2": "Slaapkamer 2", "r3": "Slaapkamer 3", "r4": "Slaapkamer 4", "r5": "Woonkamer"},
  "room_notes": {"r1": ["Bureau"], "r2": [], "r3": ["Bureau"], "r4": ["Bureau", "Eigen doucheruimte met toilet"], "r5": ["Slaapbank", "Biljart en televisie"]},
  "sleeps": "{n} slaapplaatsen",
  "bed": "bed {w} cm", "sofa": "bank {w} cm",
  "bath_note": "Drie badkamers: een eigen doucheruimte bij slaapkamer 4, een badkamer boven (bad, toilet en bidet) en een doucheruimte beneden (inloopdouche en toilet). Beddengoed en handdoeken zijn inbegrepen.",
  "living_h2": "Leefruimtes",
  "living": [("cuisine-1", "De keuken", "Gasfornuis, oven, afzuigkap, vaatwasser, magnetron, koel-vriescombinatie, Nespresso-apparaat, waterkoker en broodrooster. Ernaast een bijkeuken met wasmachine."),
             ("repas-1", "De eetkamer", "Een grote tafel onder de balken, tussen oude stenen muren. Plek voor iedereen."),
             ("salon-2", "De woonkamer", "Een aparte woonkamer met biljart, televisie, bank en gezelschapsspellen, met deuren naar buiten.")],
  "photos_h2": "Alle foto's", "photos_p": "Tik op een foto om hem te vergroten.",
  "lb_close": "Sluiten", "lb_prev": "Vorige foto", "lb_next": "Volgende foto",
  "reviews_h2": "Wat gasten zeggen",
  "reviews_badge": "Favoriet bij gasten op Airbnb, op basis van 51 reviews",
  "scores": [("Netheid", "4,9"), ("Nauwkeurigheid", "4,9"), ("Inchecken", "5,0"), ("Communicatie", "5,0"), ("Locatie", "4,8"), ("Prijs-kwaliteit", "4,8")],
  "score": "4,98",
  "quotes": [
    ("Ideaal voor gezinnen! De omgeving is rustig. We hebben met z'n zevenen een week in dit fijne huis gezeten en genoten van de rust, het zwembad en al het comfort.", "Mathieu, augustus 2026, verblijf van een week"),
    ("Het huis was in perfecte staat, nog mooier dan op de foto's. De slaapkamers zijn ruim en alles was brandschoon. Het zwembad is afgesloten, dus ook veilig voor kinderen!", "Emilie, juli 2026, met vrienden"),
    ("Mooi, goed onderhouden huis met een grote buitenruimte en grote slaapkamers. Er is alles wat je nodig hebt. We hebben genoten van het zwembad, en het biljart viel ook erg in de smaak.", "Charlotte, augustus 2026, verblijf van een week"),
    ("We hadden een geweldig weekend waarin de hele familie samen was! We komen zeker terug om deze prachtige streek verder te ontdekken.", "Eric, augustus 2026, familieweekend")],
  "translated": "Reviews vertaald uit het Frans.",
  "reviews_more": "Lees alle 51 reviews op Airbnb",
  "around_h2": "In de omgeving",
  "around_p": "Het huis ligt waar de Corrèze, de Lot en de Dordogne samenkomen. De meeste bezienswaardigheden van de streek liggen op minder dan een uur rijden.",
  "places": [("Brive-la-Gaillarde", "Oude centrum, markten en winkels", "10 min"),
             ("Turenne", "Dorp op een heuvel met kasteel", "20 min"),
             ("Collonges-la-Rouge", "Dorp van rode zandsteen, een van de mooiste van Frankrijk", "25 min"),
             ("Lac du Causse", "Bewaakt zwemmen in de zomer, watersport", "30 min"),
             ("Gouffre de Padirac", "Ondergrondse rivier per boot", "50 min"),
             ("Rocamadour", "Bedevaartsoord tegen een rotswand", "50 min"),
             ("Sarlat-la-Canéda", "Middeleeuws stadje in de Périgord Noir", "1 u")],
  "places_note": "Reistijden met de auto, bij benadering.",
  "getting_h3": "Hoe kom je er",
  "getting_p": "Met de auto via de A20 of A89, afrit Brive. Met de trein naar station Brive-la-Gaillarde, of met het vliegtuig naar luchthaven Brive–Vallée de la Dordogne, beide op ongeveer 15 minuten. Ter plaatse heb je een auto nodig.",
  "faq_h2": "Praktische informatie",
  "faq": [("Hoe boek ik?", "Boeken, betalen en de annuleringsvoorwaarden lopen via Airbnb. De knop „Bekijk beschikbaarheid” brengt je er direct naartoe, met actuele prijzen voor jouw data."),
          ("Wanneer is het huis te huur?", "Het huis wordt verhuurd van half mei tot eind september."),
          ("Hoe gaat het inchecken?", "Inchecken vanaf 17.00 uur, zelfstandig met een beveiligd sleutelkastje, dus je komt aan wanneer het jou uitkomt. Uitchecken vóór 10.00 uur."),
          ("Is het zwembad veilig voor kinderen?", "Ja. Het is privé, omheind en afgesloten. Het is open van juni tot en met september; bij een verblijf in mei is het nog niet in gebruik."),
          ("Waar kunnen we parkeren?", "Op de grote binnenplaats voor het huis, waar makkelijk meerdere auto's staan."),
          ("Is beddengoed inbegrepen?", "Ja, beddengoed en badhanddoeken zijn inbegrepen."),
          ("Mogen we een feest geven?", "Het huis is er voor families en vriendengroepen, maar feesten en evenementen zijn niet toegestaan."),
          ("Kan ik er werken?", "Ja: de wifi loopt via glasvezel en drie slaapkamers hebben een bureau."),
          ("Waar doen we boodschappen?", "De supermarkten van Brive liggen op ongeveer tien minuten rijden.")],
  "book_h2": "Jouw data, in een paar klikken",
  "book_p": "Beschikbaarheid en prijzen staan altijd actueel op Airbnb, waar je ook boekt en veilig betaalt.",
  "book_btn": "Bekijk beschikbaarheid op Airbnb",
  "contact": "Een vraag voordat je boekt? Mail ons op",
  "footer": "Landhuis met zwembad in Cosnac, Corrèze, Frankrijk. Vakantieverhuur van half mei tot eind september.",
},
}

E = html.escape
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>'


def beds_html(widths, t, sofa=False):
    out = []
    for w in widths:
        px = round(w * 0.62)  # échelle : 1 cm = 0,62 px
        label = (t["sofa"] if sofa else t["bed"]).format(w=w)
        out.append(f'<div class="bed{" sofa" if sofa else ""}" style="width:{px}px" role="img" aria-label="{E(label)}"><span>{w}</span></div>')
    return '<div class="beds">' + "".join(out) + "</div>"


def room_html(room, t, pfx):
    img, widths, n, key = room
    notes = "".join(f"<li>{E(x)}</li>" for x in t["room_notes"][key])
    name = t["room_names"][key]
    return f'''<article class="room">
  <img src="{pfx}img/{img}-s.webp" alt="{E(name)}" loading="lazy" width="720" height="480">
  <div class="room-body">
    <div class="room-title"><h3>{E(name)}</h3><span class="sleeps">{E(t["sleeps"].format(n=n))}</span></div>
    {beds_html(widths, t, sofa=(key == "r5"))}
    {"<ul class='room-notes'>" + notes + "</ul>" if notes else ""}
  </div>
</article>'''


def page(lang):
    t = T[lang]
    pfx = "" if lang == "fr" else "../"
    air = AIRBNB[lang]
    total = sum(r[2] for r in ROOMS_UP) + ROOM_DOWN[2]
    nav = "".join(f'<a href="#{a}">{E(l)}</a>' for a, l in t["nav"])
    langs = "".join(
        f'<a href="{pfx}{PATHS[l]}" hreflang="{l}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>'
        for l in ("fr", "en", "nl"))
    hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="{DOMAIN}/{PATHS[l]}">' for l in ("fr", "en", "nl"))
    hreflang += f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/">'
    facts = "".join(f"<li><b>{E(n)}</b>{E(l)}</li>" if n else f"<li><b>{E(l)}</b></li>" for n, l in t["facts"])
    reasons = "".join(f"<li><h3>{E(h)}</h3><p>{E(p)}</p></li>" for h, p in t["reasons"])
    house_p = "".join(f"<p>{E(p)}</p>" for p in t["house_p"])
    rooms_up = "".join(room_html(r, t, pfx) for r in ROOMS_UP)
    room_down = room_html(ROOM_DOWN, t, pfx)
    living = "".join(f'<figure><img src="{pfx}img/{i}-s.webp" alt="{E(h)}" loading="lazy" width="720" height="480"><h3>{E(h)}</h3><p>{E(p)}</p></figure>' for i, h, p in t["living"])
    li = LANG_IDX[lang]
    gallery = "".join(
        f'<button type="button" class="{p[4]}" data-full="{pfx}img/{p[0]}.webp" data-caption="{E(p[li])}"><img src="{pfx}img/{p[0]}-s.webp" alt="{E(p[li])}" loading="lazy"></button>'
        for p in PHOTOS)
    scores = "".join(f"<li>{E(k)} <b>{E(v)}</b></li>" for k, v in t["scores"])
    quotes = "".join(f"<blockquote><p>{E(q)}</p><footer>{E(w)}</footer></blockquote>" for q, w in t["quotes"])
    translated = f'<span class="translated">{E(t["translated"])}</span>' if t["translated"] else ""
    places = "".join(f"<li><b>{E(n)}</b><span>{E(d)}</span><time>{E(m)}</time></li>" for n, d, m in t["places"])
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in t["faq"])
    jsonld = {
        "@context": "https://schema.org", "@type": "VacationRental", "name": "Maison d'Ayras",
        # Identifiant stable, identique dans les trois langues (exigé par Google)
        "identifier": "maison-ayras",
        "additionalType": "House",
        "description": t["desc"], "url": f"{DOMAIN}/{PATHS[lang]}",
        # Google exige au moins 8 photos, dont chambre, salle de bain et pièce commune
        "image": [f"{DOMAIN}/img/{p[0]}.webp" for p in PHOTOS],
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "address": {"@type": "PostalAddress", "addressLocality": "Cosnac", "postalCode": "19360", "addressRegion": "Corrèze", "addressCountry": "FR"},
        "checkinTime": "17:00:00+02:00", "checkoutTime": "10:00:00+02:00",
        "knowsLanguage": ["fr", "en"],
        "containsPlace": {"@type": "Accommodation", "additionalType": "EntirePlace",
                          "numberOfBedrooms": 4, "numberOfBathroomsTotal": 3,
                          "occupancy": {"@type": "QuantitativeValue", "value": total},
                          "floorSize": {"@type": "QuantitativeValue", "value": 220, "unitCode": "MTK"},
                          "bed": beds_jsonld(),
                          "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True}
                                             for n in ("pool", "wifi", "tv", "kitchen", "ovenStove", "microwave", "washerDryer", "selfCheckinCheckout")]
                                            + [{"@type": "LocationFeatureSpecification", "name": "parkingType", "value": "Free"}]},
    }
    ext = 'rel="noopener" target="_blank"'
    return f'''<!DOCTYPE html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(t["title"])}</title>
<meta name="description" content="{E(t["desc"])}">
<link rel="canonical" href="{DOMAIN}/{PATHS[lang]}">
{hreflang}
<meta property="og:type" content="website">
<meta property="og:locale" content="{t["locale"]}">
<meta property="og:title" content="{E(t["title"])}">
<meta property="og:description" content="{E(t["desc"])}">
<meta property="og:image" content="{DOMAIN}/img/exterieur-1.webp">
<meta property="og:url" content="{DOMAIN}/{PATHS[lang]}">
<meta name="theme-color" content="#36424A">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%2336424A'/%3E%3Ctext x='16' y='23' font-family='Georgia' font-size='20' fill='%23fff' text-anchor='middle'%3EA%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap">
<link rel="stylesheet" href="{pfx}css/style.css">
<link rel="preload" as="image" href="{pfx}img/exterieur-1.webp">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="#top">Maison d'Ayras</a>
    <nav class="nav" id="nav" aria-label="Menu">{nav}</nav>
    <div class="langs">{langs}</div>
    <a class="btn btn-primary btn-small header-cta" href="{air}" {ext}>{E(t["book"])}</a>
    <button class="menu-toggle" type="button" aria-controls="nav" aria-expanded="false" aria-label="{E(t["menu"])}"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>

<main id="top">
<section class="hero">
  <img src="{pfx}img/exterieur-1.webp" alt="" fetchpriority="high">
  <div class="wrap">
    <p class="rating">{STAR}<strong>{E(t["score"])}</strong> {E(t["rating"])}</p>
    <h1>{E(t["h1"])}</h1>
    <p class="hero-sub">{E(t["hero_sub"])}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{air}" {ext}>{E(t["cta_dispo"])} {ARROW}</a>
      <a class="btn btn-ghost" href="#maison">{E(t["cta_discover"])}</a>
    </div>
  </div>
</section>

<div class="facts"><ul>{facts}</ul></div>

<section class="section" id="maison">
  <div class="wrap house-grid">
    <div>
      <h2>{E(t["house_h2"])}</h2>
      <div class="lede" style="margin-top:20px">{house_p}</div>
      <ul class="reasons">{reasons}</ul>
    </div>
    <div class="photos">
      <img src="{pfx}img/piscine.webp" alt="{E(t["alt_house"][0])}" loading="lazy" width="1600" height="1067">
      <img src="{pfx}img/repas-1-s.webp" alt="{E(t["alt_house"][1])}" loading="lazy" width="720" height="480">
      <img src="{pfx}img/salon-1-s.webp" alt="{E(t["alt_house"][2])}" loading="lazy" width="720" height="480">
    </div>
  </div>
</section>

<section class="section sleep" id="couchages">
  <div class="wrap">
    <div class="sleep-head">
      <div><h2>{E(t["sleep_h2"])}</h2><p class="lede" style="margin-top:14px">{E(t["sleep_p"])}</p></div>
      <p class="total"><span>{total}</span><small>{E(t["total"])}</small></p>
    </div>
    <div class="floor"><p class="floor-label">{E(t["floor_up"])}</p><div class="rooms">{rooms_up}</div></div>
    <div class="floor"><p class="floor-label">{E(t["floor_down"])}</p><div class="rooms one">{room_down}<p class="bath-note">{E(t["bath_note"])}</p></div></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2>{E(t["living_h2"])}</h2>
    <div class="living">{living}</div>
  </div>
</section>

<section class="section" id="photos" style="padding-top:0">
  <div class="wrap">
    <h2>{E(t["photos_h2"])}</h2>
    <p class="lede" style="margin-top:10px">{E(t["photos_p"])}</p>
    <div class="gallery">{gallery}</div>
  </div>
</section>

<section class="section reviews" id="avis">
  <div class="wrap">
    <div class="reviews-head">
      <div><h2>{E(t["reviews_h2"])}</h2><ul class="scores">{scores}</ul></div>
      <p class="score">{E(t["score"])}<small>{E(t["reviews_badge"])}</small></p>
    </div>
    <div class="quotes">{quotes}</div>
    <div class="more"><a href="{air}#reviews" {ext}>{E(t["reviews_more"])}</a>{translated}</div>
  </div>
</section>

<section class="section" id="autour">
  <div class="wrap around-grid">
    <div>
      <h2>{E(t["around_h2"])}</h2>
      <p class="lede" style="margin-top:20px">{E(t["around_p"])}</p>
      <div class="getting"><h3>{E(t["getting_h3"])}</h3><p>{E(t["getting_p"])}</p></div>
    </div>
    <div><ul class="places">{places}</ul><p class="note">{E(t["places_note"])}</p></div>
  </div>
</section>

<section class="section" id="infos" style="padding-top:0">
  <div class="wrap">
    <h2 style="margin-bottom:28px">{E(t["faq_h2"])}</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="section book">
  <div class="wrap">
    <div>
      <h2>{E(t["book_h2"])}</h2>
      <p>{E(t["book_p"])}</p>
      <p class="contact">{E(t["contact"])} <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <a class="btn btn-primary" href="{air}" {ext}>{E(t["book_btn"])} {ARROW}</a>
  </div>
</section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div><span class="brand">Maison d'Ayras</span>{E(t["footer"])}</div>
    <div class="langs">{langs}</div>
  </div>
</footer>

<div class="mobile-cta"><a class="btn btn-primary" href="{air}" {ext}>{E(t["cta_dispo"])} {ARROW}</a></div>

<dialog class="lightbox" aria-label="{E(t["photos_h2"])}">
  <figure><img src="" alt=""><figcaption></figcaption></figure>
  <button type="button" class="lb-btn lb-close" aria-label="{E(t["lb_close"])}">&times;</button>
  <button type="button" class="lb-btn lb-prev" aria-label="{E(t["lb_prev"])}">&#8249;</button>
  <button type="button" class="lb-btn lb-next" aria-label="{E(t["lb_next"])}">&#8250;</button>
</dialog>
<script src="{pfx}js/main.js" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    for lang in ("fr", "en", "nl"):
        d = os.path.join(ROOT, PATHS[lang])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(lang))
        print("ok", lang)
