# Wervingscockpit

Een tool voor intercedenten om effectief kandidaten te werven voor vacatures met
praktisch geschoold werk. Direct gebouwd op het marktonderzoek *"Kandidaten vinden
in een krappe markt"* (Olympia-franchisefilialen, juli 2026).

## De "edge"

De kern van het wervingsprobleem uit het rapport: **minder dan 10% van de doelgroep
zoekt actief** — vacaturebanken en LinkedIn vissen in de kleinste vijver. De ±50%
latente zoekers reageren wél op persoonlijke benadering. Concurrenten wachten tot
kandidaten reageren; deze tool draait het om:

1. **📡 Latente Kandidaat Radar** — een *uitlegbaar* scoringsalgoritme (0–100) dat de
   eigen database dagelijks rangschikt op reactiveringskans, op basis van vier
   componenten: timing sinds laatste contact (sweet spot 60–270 dagen),
   plaatsingshistorie, skills-match met **nu openstaande** vacatures (bellen met een
   concrete baan converteert) en beschikbaarheid. De intercedent ziet per kandidaat
   *waarom* die bovenaan staat en krijgt elke dag een kant-en-klare bellijst van 10.
2. **⚡ 1-uursnorm met live SLA-timer** — nieuwe aanmeldingen kleuren groen → oranje →
   rood; wie het eerst reageert, plaatst de kandidaat. WhatsApp-reactie met één klik
   (voorgeschreven persoonlijke tekst via `wa.me`-deeplink).
3. **🧩 Skills-based matching zonder diploma-filter** — naast directe matches toont de
   tool per vacature ook de "brede vijver": leerbereide kandidaten met gedeeltelijke
   skills-overlap, mits de vacature als opleidbaar is gemarkeerd.
4. **🤝 Referral-tracker** — het sterkst onderbouwde kanaal voor deze doelgroep.
   Bonusfasen (€100 bij plaatsing + €100 na 8 gewerkte weken), promotie-appjes met
   één klik, top-aanbrengers-lijst.
5. **📣 Contentstudio** — genereert per vacature drie Facebook/Instagram-posts in de
   toon die werkt voor deze doelgroep ("deze week starten", intercedent aan het
   woord, meeloopdag i.p.v. vacature), klaar om te kopiëren naar lokale werkgroepen.
6. **☕ Kennismakings-planner** — inloopdagen, meeloopdagen en rondleidingen (1 op de 3
   werkzoekenden staat hiervoor open).
7. **📊 KPI-dashboard** — precies de vier kengetallen uit het advies: reactietijd,
   gereactiveerde database-kandidaten, referral-aanmeldingen en plaatsingen per
   kanaal. Zo wordt binnen 6–8 weken zichtbaar welk kanaal per filiaal converteert.

## Mapping op het wervingsadvies

| Strategie uit het rapport                  | Onderdeel in de tool            |
|--------------------------------------------|---------------------------------|
| 1. Referral via eigen uitzendkrachten      | Referrals-tab + promo-appjes    |
| 2. Facebook/Instagram i.p.v. LinkedIn      | Contentstudio                   |
| 3. Laagdrempelig kennismaken               | Kennismaken-tab (events)        |
| 4. Actief benaderen & database reactiveren | Radar & bellijst                |
| 5. Breder werven en opleiden (skills-based)| Vacatures & matches             |
| 6. Snelheid en bereikbaarheid als wapen    | Aanmeldingen-tab met SLA-timer  |
| Meetbaar maken (4 kengetallen)             | Dashboard                       |

## Gebruik

Geen installatie of build nodig — open `index.html` in de browser:

```bash
# optioneel, via een lokale webserver:
cd wervingscockpit
python3 -m http.server 8080
# → http://localhost:8080
```

- Alle data staat lokaal in de browser (localStorage); er verlaat niets het apparaat.
- Bij eerste start wordt demodata geladen; via de voetregel is die te herstellen.
- Vul rechtsboven je voornaam in — die wordt gebruikt in alle WhatsApp-berichten en
  social posts (vast, benaderbaar contactpersoon: naam + nummer bij elke uiting).

## Techniek

Bewust dependency-vrij (HTML + CSS + vanilla JS), zodat elk filiaal het zonder
IT-afdeling kan draaien:

```
wervingscockpit/
├── index.html          # instap
├── css/style.css       # stijl
└── js/
    ├── data.js         # datalaag + demodata (localStorage)
    ├── score.js        # radar-score, matching, SLA, KPI's
    ├── templates.js    # WhatsApp- en social-berichtgenerator
    └── app.js          # UI
```

In productie zou de datalaag (`data.js`) vervangen worden door een koppeling met het
ATS/planningssysteem; de scoring-, matching- en templatelogica blijft gelijk.
