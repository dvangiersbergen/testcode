/* =========================================================
   Wervingscockpit — datalaag
   Persistentie via localStorage; eerste start seedt demodata.
   ========================================================= */

const DB_KEY = 'wervingscockpit_v1';

function dagenGeleden(n) {
  const d = new Date();
  d.setDate(d.getDate() - n);
  return d.toISOString();
}

function minutenGeleden(n) {
  return new Date(Date.now() - n * 60000).toISOString();
}

function overDagen(n) {
  const d = new Date();
  d.setDate(d.getDate() + n);
  return d.toISOString().slice(0, 10);
}

/* ---------- Demodata (eerste start) ---------- */

function seedData() {
  return {
    filialen: ['Filiaal Noord', 'Filiaal Centrum', 'Filiaal Zuid'],

    kandidaten: [
      { id: 'k1',  naam: 'Mo el Idrissi',     telefoon: '0612345601', woonplaats: 'Tilburg',    skills: ['heftruck', 'magazijn', 'orderpicken'], functie: 'Magazijnmedewerker', beschikbaar: 'direct',      laatstContact: dagenGeleden(124), plaatsingen: 3, bron: 'referral',  wilLeren: true,  status: 'inactief' },
      { id: 'k2',  naam: 'Sandra Vermeulen',  telefoon: '0612345602', woonplaats: 'Breda',      skills: ['schoonmaak', 'hotel'],                 functie: 'Schoonmaakmedewerker', beschikbaar: 'direct',    laatstContact: dagenGeleden(210), plaatsingen: 2, bron: 'facebook',  wilLeren: false, status: 'inactief' },
      { id: 'k3',  naam: 'Kevin de Boer',     telefoon: '0612345603', woonplaats: 'Tilburg',    skills: ['productie', 'techniek', 'vorkheftruck'], functie: 'Productiemedewerker', beschikbaar: 'per 1e van de maand', laatstContact: dagenGeleden(95), plaatsingen: 4, bron: 'database', wilLeren: true, status: 'inactief' },
      { id: 'k4',  naam: 'Fatima Yilmaz',     telefoon: '0612345604', woonplaats: 'Waalwijk',   skills: ['orderpicken', 'inpakken'],             functie: 'Orderpicker', beschikbaar: 'direct',             laatstContact: dagenGeleden(45),  plaatsingen: 1, bron: 'instagram', wilLeren: true,  status: 'inactief' },
      { id: 'k5',  naam: 'Piotr Kowalski',    telefoon: '0612345605', woonplaats: 'Tilburg',    skills: ['bouw', 'timmeren', 'rijbewijs-b'],     functie: 'Bouwhulp', beschikbaar: 'in overleg',            laatstContact: dagenGeleden(300), plaatsingen: 5, bron: 'referral',  wilLeren: false, status: 'inactief' },
      { id: 'k6',  naam: 'Anouk Peters',      telefoon: '0612345606', woonplaats: 'Breda',      skills: ['horeca', 'kassa', 'klantcontact'],     functie: 'Horecamedewerker', beschikbaar: 'weekend',       laatstContact: dagenGeleden(160), plaatsingen: 2, bron: 'inloopdag', wilLeren: true,  status: 'inactief' },
      { id: 'k7',  naam: 'Dennis Bakker',     telefoon: '0612345607', woonplaats: 'Oosterhout', skills: ['heftruck', 'reachtruck', 'magazijn'],  functie: 'Heftruckchauffeur', beschikbaar: 'direct',       laatstContact: dagenGeleden(75),  plaatsingen: 6, bron: 'database',  wilLeren: false, status: 'inactief' },
      { id: 'k8',  naam: 'Layla Hassan',      telefoon: '0612345608', woonplaats: 'Tilburg',    skills: ['schoonmaak', 'zorg-assistentie'],      functie: 'Schoonmaakmedewerker', beschikbaar: 'direct',    laatstContact: dagenGeleden(30),  plaatsingen: 0, bron: 'facebook',  wilLeren: true,  status: 'inactief' },
      { id: 'k9',  naam: 'Ruud Janssen',      telefoon: '0612345609', woonplaats: 'Dongen',     skills: ['productie', 'kwaliteitscontrole'],     functie: 'Productiemedewerker', beschikbaar: 'per direct', laatstContact: dagenGeleden(400), plaatsingen: 7, bron: 'database',  wilLeren: false, status: 'inactief' },
      { id: 'k10', naam: 'Esra Demir',        telefoon: '0612345610', woonplaats: 'Tilburg',    skills: ['orderpicken', 'scanner', 'magazijn'],  functie: 'Orderpicker', beschikbaar: 'direct',             laatstContact: dagenGeleden(9),   plaatsingen: 1, bron: 'referral',  wilLeren: true,  status: 'actief' },
      { id: 'k11', naam: 'Tom Willems',       telefoon: '0612345611', woonplaats: 'Rijen',      skills: ['logistiek', 'rijbewijs-b', 'bezorgen'], functie: 'Bezorger', beschikbaar: 'direct',               laatstContact: dagenGeleden(180), plaatsingen: 2, bron: 'instagram', wilLeren: true,  status: 'inactief' },
      { id: 'k12', naam: 'Grace Okafor',      telefoon: '0612345612', woonplaats: 'Breda',      skills: ['zorg-assistentie', 'schoonmaak'],      functie: 'Huishoudelijke hulp', beschikbaar: 'deeltijd',   laatstContact: dagenGeleden(140), plaatsingen: 1, bron: 'inloopdag', wilLeren: true,  status: 'inactief' },
      { id: 'k13', naam: 'Bram Hendriks',     telefoon: '0612345613', woonplaats: 'Tilburg',    skills: ['techniek', 'montage', 'productie'],    functie: 'Monteur', beschikbaar: 'per 15e',                laatstContact: dagenGeleden(60),  plaatsingen: 3, bron: 'database',  wilLeren: false, status: 'inactief' },
      { id: 'k14', naam: 'Yasmin Boukhari',   telefoon: '0612345614', woonplaats: 'Waalwijk',   skills: ['inpakken', 'productie'],               functie: 'Inpakker', beschikbaar: 'direct',                laatstContact: dagenGeleden(240), plaatsingen: 1, bron: 'facebook',  wilLeren: true,  status: 'inactief' },
      { id: 'k15', naam: 'Henk van Dijk',     telefoon: '0612345615', woonplaats: 'Oosterhout', skills: ['beveiliging', 'receptie'],             functie: 'Beveiliger', beschikbaar: 'in overleg',           laatstContact: dagenGeleden(85),  plaatsingen: 4, bron: 'database',  wilLeren: false, status: 'inactief' }
    ],

    vacatures: [
      { id: 'v1', titel: 'Heftruckchauffeur',    inlener: 'LogiPart DC',        plaats: 'Tilburg',    filiaal: 'Filiaal Noord',   skills: ['heftruck', 'magazijn'],        uren: '38 u/wk', salaris: '€15,20/u', start: overDagen(4),  opleidbaar: true,  status: 'open' },
      { id: 'v2', titel: 'Orderpicker (avond)',  inlener: 'FreshBox Fulfilment', plaats: 'Waalwijk',  filiaal: 'Filiaal Noord',   skills: ['orderpicken', 'scanner'],      uren: '32 u/wk', salaris: '€14,10/u', start: overDagen(2),  opleidbaar: true,  status: 'open' },
      { id: 'v3', titel: 'Schoonmaakmedewerker', inlener: 'CleanCare Hotels',   plaats: 'Breda',      filiaal: 'Filiaal Centrum', skills: ['schoonmaak', 'hotel'],         uren: '24 u/wk', salaris: '€13,80/u', start: overDagen(7),  opleidbaar: true,  status: 'open' },
      { id: 'v4', titel: 'Productiemedewerker',  inlener: 'Verpak-Plus BV',     plaats: 'Tilburg',    filiaal: 'Filiaal Zuid',    skills: ['productie', 'inpakken'],       uren: '40 u/wk', salaris: '€14,50/u', start: overDagen(10), opleidbaar: true,  status: 'open' },
      { id: 'v5', titel: 'Beveiliger (object)',  inlener: 'SecuriTeam',         plaats: 'Breda',      filiaal: 'Filiaal Centrum', skills: ['beveiliging'],                 uren: '36 u/wk', salaris: '€16,00/u', start: overDagen(14), opleidbaar: false, status: 'open' },
      { id: 'v6', titel: 'Monteur assemblage',   inlener: 'TechniFab',          plaats: 'Oosterhout', filiaal: 'Filiaal Zuid',    skills: ['montage', 'techniek'],         uren: '40 u/wk', salaris: '€16,40/u', start: overDagen(21), opleidbaar: true,  status: 'open' }
    ],

    aanmeldingen: [
      { id: 'a1', naam: 'Jordy Smits',    telefoon: '0612345620', vacatureId: 'v2', kanaal: 'whatsapp',  binnen: minutenGeleden(24),   eersteReactie: null,               plaatsing: false },
      { id: 'a2', naam: 'Nadia Charif',   telefoon: '0612345621', vacatureId: 'v1', kanaal: 'facebook',  binnen: minutenGeleden(51),   eersteReactie: null,               plaatsing: false },
      { id: 'a3', naam: 'Wesley Vos',     telefoon: '0612345622', vacatureId: 'v4', kanaal: 'referral',  binnen: minutenGeleden(190),  eersteReactie: minutenGeleden(160), plaatsing: true },
      { id: 'a4', naam: 'Iris de Groot',  telefoon: '0612345623', vacatureId: 'v3', kanaal: 'instagram', binnen: minutenGeleden(2900), eersteReactie: minutenGeleden(2860), plaatsing: false },
      { id: 'a5', naam: 'Samir Amrani',   telefoon: '0612345624', vacatureId: 'v1', kanaal: 'whatsapp',  binnen: minutenGeleden(4300), eersteReactie: minutenGeleden(4280), plaatsing: true },
      { id: 'a6', naam: 'Kim Verhoeven',  telefoon: '0612345625', vacatureId: 'v6', kanaal: 'inloopdag', binnen: minutenGeleden(6100), eersteReactie: minutenGeleden(6090), plaatsing: false }
    ],

    referrals: [
      { id: 'r1', aanbrengerId: 'k7',  naamNieuw: 'Wesley Vos',    datum: dagenGeleden(12), status: 'geplaatst',  bonus: 200, weken: 3 },
      { id: 'r2', aanbrengerId: 'k1',  naamNieuw: 'Sofia Mendes',  datum: dagenGeleden(30), status: '8weken',     bonus: 200, weken: 9 },
      { id: 'r3', aanbrengerId: 'k10', naamNieuw: 'Danny Peters',  datum: dagenGeleden(4),  status: 'aangemeld',  bonus: 200, weken: 0 },
      { id: 'r4', aanbrengerId: 'k7',  naamNieuw: 'Alex Novak',    datum: dagenGeleden(55), status: 'uitbetaald', bonus: 200, weken: 12 }
    ],

    events: [
      { id: 'e1', type: 'Inloopdag',   titel: 'Koffie & werk — cv niet nodig', locatie: 'Filiaal Noord',            datum: overDagen(6),  aanmeldingen: 4 },
      { id: 'e2', type: 'Meeloopdag',  titel: 'Kijkje in het DC van LogiPart', locatie: 'LogiPart DC, Tilburg',     datum: overDagen(11), aanmeldingen: 7 },
      { id: 'e3', type: 'Rondleiding', titel: 'Achter de schermen bij FreshBox', locatie: 'FreshBox, Waalwijk',     datum: overDagen(18), aanmeldingen: 2 }
    ],

    // logboek van belacties (kandidaatId -> laatste uitkomst)
    belLog: []
  };
}

/* ---------- Storage ---------- */

function loadDB() {
  try {
    const raw = localStorage.getItem(DB_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) { /* corrupt of geblokkeerd: val terug op seed */ }
  const db = seedData();
  saveDB(db);
  return db;
}

function saveDB(db) {
  try { localStorage.setItem(DB_KEY, JSON.stringify(db)); } catch (e) { /* privémodus: sessie-only */ }
}

function resetDB() {
  localStorage.removeItem(DB_KEY);
  return loadDB();
}
