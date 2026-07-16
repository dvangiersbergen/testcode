/* =========================================================
   Wervingscockpit — UI
   Vanilla JS, geen dependencies. Eén render per tab.
   ========================================================= */

let db = loadDB();
let actieveTab = 'dashboard';

const $ = sel => document.querySelector(sel);
const el = (tag, cls, html) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html !== undefined) n.innerHTML = html;
  return n;
};

function esc(s) {
  return String(s).replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function vacatureVan(id) {
  return db.vacatures.find(v => v.id === id);
}

function kandidaatVan(id) {
  return db.kandidaten.find(k => k.id === id);
}

/* ---------- Navigatie ---------- */

const TABS = [
  { id: 'dashboard',    label: '📊 Dashboard' },
  { id: 'radar',        label: '📡 Radar & bellijst' },
  { id: 'aanmeldingen', label: '⚡ Aanmeldingen (SLA)' },
  { id: 'vacatures',    label: '🧩 Vacatures & matches' },
  { id: 'referrals',    label: '🤝 Referrals' },
  { id: 'content',      label: '📣 Contentstudio' },
  { id: 'events',       label: '☕ Kennismaken' }
];

function renderNav() {
  const nav = $('#nav');
  nav.innerHTML = '';
  for (const t of TABS) {
    const b = el('button', 'tab' + (t.id === actieveTab ? ' actief' : ''), t.label);
    b.onclick = () => { actieveTab = t.id; render(); };
    nav.appendChild(b);
  }
}

/* ---------- Dashboard ---------- */

const KANAAL_LABELS = {
  whatsapp: 'WhatsApp', facebook: 'Facebook', instagram: 'Instagram',
  referral: 'Referral', inloopdag: 'Inloopdag', database: 'Database', vacaturebank: 'Vacaturebank'
};

function renderDashboard(root) {
  const kpi = berekenKpis(db);
  const open = db.aanmeldingen.filter(a => !a.eersteReactie).length;
  const overSla = db.aanmeldingen.filter(a => !a.eersteReactie && slaStatus(a).fase === 'rood').length;

  const grid = el('div', 'kpi-grid');
  const kaart = (waarde, label, sub, toon) => {
    const k = el('div', 'kpi ' + (toon || ''));
    k.append(el('div', 'kpi-waarde', waarde), el('div', 'kpi-label', label));
    if (sub) k.append(el('div', 'kpi-sub', sub));
    return k;
  };

  grid.append(
    kaart(kpi.gemiddeldeReactie !== null ? kpi.gemiddeldeReactie + ' min' : '—',
      'Gem. reactietijd', 'norm: < 60 min',
      kpi.gemiddeldeReactie !== null && kpi.gemiddeldeReactie <= 60 ? 'goed' : 'slecht'),
    kaart(String(kpi.gereactiveerd), 'Gereactiveerd deze week', 'database-belactie', kpi.gereactiveerd >= 5 ? 'goed' : ''),
    kaart(String(kpi.referralsNieuw), 'Referrals (30 dgn)', 'sterkste kanaal voor deze doelgroep', kpi.referralsNieuw >= 2 ? 'goed' : ''),
    kaart(String(open), 'Onbeantwoorde aanmeldingen', overSla ? `${overSla} over de 1-uursnorm!` : 'alles binnen de norm', overSla ? 'slecht' : 'goed')
  );
  root.append(el('h2', null, 'De vier kengetallen'), grid);

  // Plaatsingen per kanaal — laat zien waar de winst zit
  root.append(el('h2', null, 'Plaatsingen per kanaal'));
  const staafBlok = el('div', 'staven');
  const max = Math.max(1, ...Object.values(kpi.perKanaal));
  const kanalen = Object.entries(kpi.perKanaal).sort((a, b) => b[1] - a[1]);
  if (!kanalen.length) staafBlok.append(el('p', 'leeg', 'Nog geen plaatsingen geregistreerd.'));
  for (const [kanaal, n] of kanalen) {
    const rij = el('div', 'staaf-rij');
    rij.append(el('div', 'staaf-label', esc(KANAAL_LABELS[kanaal] || kanaal)));
    const baan = el('div', 'staaf-baan');
    const vulling = el('div', 'staaf-vulling');
    vulling.style.width = (n / max * 100) + '%';
    vulling.textContent = n;
    baan.append(vulling);
    rij.append(baan);
    staafBlok.append(rij);
  }
  root.append(staafBlok);

  root.append(el('p', 'uitleg',
    '💡 Het advies: stuur wekelijks per filiaal op deze vier cijfers. Binnen 6–8 weken zie je welk kanaal het best converteert — en LinkedIn/vacaturebanken zullen het vrijwel nooit zijn.'));
}

/* ---------- Radar & bellijst ---------- */

function renderRadar(root) {
  root.append(el('h2', null, '📡 Latente Kandidaat Radar — bellijst van vandaag'));
  root.append(el('p', 'uitleg',
    'Minder dan 10% van de doelgroep zoekt actief; ±50% is latent zoeker en reageert wél op persoonlijke benadering. ' +
    'De radar rangschikt de eigen database op reactiveringskans — met concrete vacature als belreden. Doel: 10 belletjes per dag per intercedent.'));

  const lijst = bouwBellijst(db, 10);
  if (!lijst.length) {
    root.append(el('p', 'leeg', '🎉 Alle kansrijke kandidaten zijn vandaag al gebeld. Morgen staat er een nieuwe lijst klaar.'));
    return;
  }

  lijst.forEach((item, i) => {
    const k = item.kandidaat;
    const kaart = el('div', 'kaart');
    const kop = el('div', 'kaart-kop');
    kop.append(
      el('div', 'rangnr', String(i + 1)),
      el('div', null, `<strong>${esc(k.naam)}</strong> — ${esc(k.functie)}, ${esc(k.woonplaats)}<br>` +
        `<span class="klein">skills: ${k.skills.map(esc).join(', ')} · beschikbaar: ${esc(k.beschikbaar)}</span>`),
      el('div', 'score score-' + (item.score >= 70 ? 'hoog' : item.score >= 45 ? 'mid' : 'laag'), item.score + '')
    );
    kaart.append(kop);

    // Uitlegbare score: waarom staat deze kandidaat hier?
    const redenen = el('ul', 'redenen');
    for (const r of item.redenen) {
      redenen.append(el('li', null, `${esc(r.label)} <span class="punten">+${r.punten}/${r.max}</span>`));
    }
    kaart.append(redenen);

    const acties = el('div', 'acties');
    const bericht = reactiveringsBericht(k, item.besteMatch);
    const wa = el('a', 'knop knop-wa', '💬 WhatsApp');
    wa.href = waLink(k.telefoon, bericht);
    wa.target = '_blank';
    const bel = el('a', 'knop', '📞 Bel ' + esc(k.telefoon));
    bel.href = 'tel:' + k.telefoon;

    const uitkomst = el('select', 'uitkomst');
    uitkomst.innerHTML = '<option value="">— uitkomst vastleggen —</option>' +
      '<option value="interesse">✅ Interesse / intake gepland</option>' +
      '<option value="later">🕐 Later terugbellen</option>' +
      '<option value="geen-interesse">❌ Geen interesse</option>' +
      '<option value="onbereikbaar">📵 Onbereikbaar</option>';
    uitkomst.onchange = () => {
      if (!uitkomst.value) return;
      db.belLog.push({ kandidaatId: k.id, datum: new Date().toISOString(), uitkomst: uitkomst.value });
      const kk = kandidaatVan(k.id);
      kk.laatstContact = new Date().toISOString();
      if (uitkomst.value === 'interesse') kk.status = 'actief';
      saveDB(db);
      render();
    };
    acties.append(wa, bel, uitkomst);
    kaart.append(acties);
    root.append(kaart);
  });

  const vandaag = new Date().toISOString().slice(0, 10);
  const gebeld = db.belLog.filter(l => l.datum.slice(0, 10) === vandaag).length;
  root.append(el('p', 'uitleg', `Vandaag afgehandeld: <strong>${gebeld}/10</strong>`));
}

/* ---------- Aanmeldingen (SLA) ---------- */

function renderAanmeldingen(root) {
  root.append(el('h2', null, '⚡ Nieuwe aanmeldingen — de 1-uursnorm'));
  root.append(el('p', 'uitleg',
    'De kandidaat die vandaag reageert, is morgen bij de concurrent geplaatst. Norm: eerste reactie binnen 1 uur, intake binnen 24 uur — WhatsApp is een volwaardig sollicitatiekanaal.'));

  const form = el('div', 'formulier');
  form.innerHTML = `
    <input id="am-naam" placeholder="Naam kandidaat">
    <input id="am-tel" placeholder="06-nummer">
    <select id="am-vac">${db.vacatures.filter(v => v.status === 'open').map(v =>
      `<option value="${v.id}">${esc(v.titel)} — ${esc(v.inlener)}</option>`).join('')}</select>
    <select id="am-kanaal">
      <option value="whatsapp">WhatsApp</option><option value="facebook">Facebook</option>
      <option value="instagram">Instagram</option><option value="referral">Referral</option>
      <option value="inloopdag">Inloopdag</option><option value="vacaturebank">Vacaturebank</option>
    </select>
    <button class="knop knop-primair" id="am-toevoegen">+ Aanmelding</button>`;
  root.append(form);
  form.querySelector('#am-toevoegen').onclick = () => {
    const naam = form.querySelector('#am-naam').value.trim();
    const tel = form.querySelector('#am-tel').value.trim();
    if (!naam || !tel) return alert('Vul naam en telefoonnummer in.');
    db.aanmeldingen.unshift({
      id: 'a' + Date.now(), naam, telefoon: tel,
      vacatureId: form.querySelector('#am-vac').value,
      kanaal: form.querySelector('#am-kanaal').value,
      binnen: new Date().toISOString(), eersteReactie: null, plaatsing: false
    });
    saveDB(db); render();
  };

  const sorteer = a => slaStatus(a).fase === 'rood' ? 0 : a.eersteReactie ? 2 : 1;
  const lijst = [...db.aanmeldingen].sort((a, b) => sorteer(a) - sorteer(b) || new Date(b.binnen) - new Date(a.binnen));

  for (const a of lijst) {
    const v = vacatureVan(a.vacatureId);
    const s = slaStatus(a);
    const kaart = el('div', 'kaart sla-' + s.fase);

    let statusTekst;
    if (s.fase === 'gehaald') statusTekst = `✅ beantwoord in ${s.minuten} min`;
    else if (s.fase === 'gemist') statusTekst = `⚠️ beantwoord in ${s.minuten} min (norm gemist)`;
    else statusTekst = `⏱️ wacht al ${s.minuten} min` + (s.fase === 'rood' ? ' — NORM OVERSCHREDEN' : '');

    kaart.append(el('div', null,
      `<strong>${esc(a.naam)}</strong> · ${esc(a.telefoon)} — ${v ? esc(v.titel) + ' (' + esc(v.inlener) + ')' : 'onbekende vacature'}<br>` +
      `<span class="klein">via ${esc(KANAAL_LABELS[a.kanaal] || a.kanaal)} · ${statusTekst}${a.plaatsing ? ' · 🎯 geplaatst' : ''}</span>`));

    const acties = el('div', 'acties');
    if (!a.eersteReactie) {
      const wa = el('a', 'knop knop-wa', '💬 Reageer via WhatsApp');
      wa.href = waLink(a.telefoon, aanmeldingsBericht(a, v));
      wa.target = '_blank';
      wa.onclick = () => { a.eersteReactie = new Date().toISOString(); saveDB(db); setTimeout(render, 300); };
      const klaar = el('button', 'knop', '✔ Gereageerd (gebeld)');
      klaar.onclick = () => { a.eersteReactie = new Date().toISOString(); saveDB(db); render(); };
      acties.append(wa, klaar);
    } else if (!a.plaatsing) {
      const p = el('button', 'knop knop-primair', '🎯 Markeer als plaatsing');
      p.onclick = () => { a.plaatsing = true; saveDB(db); render(); };
      acties.append(p);
    }
    kaart.append(acties);
    root.append(kaart);
  }
}

/* ---------- Vacatures & matches ---------- */

function renderVacatures(root) {
  root.append(el('h2', null, '🧩 Vacatures — skills-based matching'));
  root.append(el('p', 'uitleg',
    'Matching op skills, niet op diploma. Bij vacatures die als opleidbaar zijn gemarkeerd toont de tool ook leerbereide kandidaten met gedeeltelijke overlap — de "brede vijver" die concurrenten laten liggen.'));

  for (const v of db.vacatures.filter(v => v.status === 'open')) {
    const m = matchesVoorVacature(db, v);
    const kaart = el('div', 'kaart');
    kaart.append(el('div', null,
      `<strong>${esc(v.titel)}</strong> — ${esc(v.inlener)}, ${esc(v.plaats)} · ${esc(v.uren)} · ${esc(v.salaris)} · start ${esc(v.start)}<br>` +
      `<span class="klein">skills: ${v.skills.map(esc).join(', ')} · ${v.opleidbaar ? '✅ opleidbaar (geen diploma-eis)' : '⛔ diploma/certificaat vereist'} · ${esc(v.filiaal)}</span>`));

    const blok = el('div', 'match-blok');
    const kolom = (titel, items, leeg) => {
      const kol = el('div', 'match-kolom');
      kol.append(el('h4', null, titel));
      if (!items.length) kol.append(el('p', 'leeg', leeg));
      for (const { kandidaat: k, overlap } of items.slice(0, 4)) {
        const rij = el('div', 'match-rij');
        rij.append(el('span', null,
          `${esc(k.naam)} <span class="klein">(${esc(k.woonplaats)}, ${overlap} skill${overlap === 1 ? '' : 's'} match, beschikbaar: ${esc(k.beschikbaar)})</span>`));
        const wa = el('a', 'knop knop-klein knop-wa', '💬');
        wa.href = waLink(k.telefoon, reactiveringsBericht(k, v));
        wa.target = '_blank';
        rij.append(wa);
        kol.append(rij);
      }
      return kol;
    };
    blok.append(
      kolom('Directe matches', m.direct, 'Geen directe matches in de database.'),
      kolom('Opleidbaar (brede vijver)', m.opleidbaar, v.opleidbaar ? 'Geen leerbereide kandidaten gevonden.' : 'Vacature vereist diploma — bespreek met de inlener of die eis kan vervallen.')
    );
    kaart.append(blok);
    root.append(kaart);
  }
}

/* ---------- Referrals ---------- */

const REFERRAL_STATUS = {
  aangemeld:  { label: 'Aangemeld',            volgende: 'geplaatst',  knop: '→ Geplaatst' },
  geplaatst:  { label: 'Geplaatst (deel 1: €100)', volgende: '8weken', knop: '→ 8 weken gewerkt' },
  '8weken':   { label: '8 weken gewerkt (deel 2: €100)', volgende: 'uitbetaald', knop: '→ Uitbetaald' },
  uitbetaald: { label: 'Volledig uitbetaald ✅', volgende: null }
};

function renderReferrals(root) {
  root.append(el('h2', null, '🤝 Referral-programma'));
  root.append(el('p', 'uitleg',
    'Het sterkst onderbouwde kanaal voor praktisch geschoold werk: één magazijnmedewerker kent meerdere beschikbare kandidaten. ' +
    'Bonus €200 per plaatsing, gesplitst: €100 bij start, €100 na 8 gewerkte weken (no-cure-no-pay).'));

  const form = el('div', 'formulier');
  form.innerHTML = `
    <select id="rf-aanbrenger">${db.kandidaten.map(k => `<option value="${k.id}">${esc(k.naam)}</option>`).join('')}</select>
    <input id="rf-naam" placeholder="Naam aangebrachte kandidaat">
    <button class="knop knop-primair" id="rf-toevoegen">+ Referral registreren</button>`;
  root.append(form);
  form.querySelector('#rf-toevoegen').onclick = () => {
    const naam = form.querySelector('#rf-naam').value.trim();
    if (!naam) return alert('Vul de naam van de aangebrachte kandidaat in.');
    db.referrals.unshift({
      id: 'r' + Date.now(), aanbrengerId: form.querySelector('#rf-aanbrenger').value,
      naamNieuw: naam, datum: new Date().toISOString(), status: 'aangemeld', bonus: 200, weken: 0
    });
    saveDB(db); render();
  };

  for (const r of db.referrals) {
    const aanbrenger = kandidaatVan(r.aanbrengerId);
    const st = REFERRAL_STATUS[r.status];
    const kaart = el('div', 'kaart');
    kaart.append(el('div', null,
      `<strong>${esc(r.naamNieuw)}</strong> — aangebracht door ${aanbrenger ? esc(aanbrenger.naam) : '?'}<br>` +
      `<span class="klein">${new Date(r.datum).toLocaleDateString('nl-NL')} · status: ${st.label}</span>`));
    const acties = el('div', 'acties');
    if (st.volgende) {
      const knop = el('button', 'knop', st.knop);
      knop.onclick = () => { r.status = st.volgende; saveDB(db); render(); };
      acties.append(knop);
    }
    if (aanbrenger) {
      const promo = el('a', 'knop knop-wa', '💬 Promoot regeling bij ' + esc(aanbrenger.naam.split(' ')[0]));
      promo.href = waLink(aanbrenger.telefoon, referralBericht(aanbrenger));
      promo.target = '_blank';
      acties.append(promo);
    }
    kaart.append(acties);
    root.append(kaart);
  }

  // Top-aanbrengers
  const telling = {};
  for (const r of db.referrals) telling[r.aanbrengerId] = (telling[r.aanbrengerId] || 0) + 1;
  const top = Object.entries(telling).sort((a, b) => b[1] - a[1]).slice(0, 3);
  if (top.length) {
    root.append(el('h3', null, '🏆 Top-aanbrengers'));
    const ol = el('ol', 'toplijst');
    for (const [id, n] of top) {
      const k = kandidaatVan(id);
      ol.append(el('li', null, `${k ? esc(k.naam) : id} — ${n} referral(s)`));
    }
    root.append(ol);
  }
}

/* ---------- Contentstudio ---------- */

function renderContent(root) {
  root.append(el('h2', null, '📣 Contentstudio — Facebook & Instagram'));
  root.append(el('p', 'uitleg',
    'Voor deze doelgroep werkt Facebook/Instagram beter dan LinkedIn, en korte authentieke content beter dan vacatureteksten. ' +
    'Genereer per vacature drie varianten; plaats ze ook gratis in lokale "Werk gezocht/aangeboden"-groepen.'));

  const kies = el('div', 'formulier');
  kies.innerHTML = `
    <select id="ct-vac">${db.vacatures.filter(v => v.status === 'open').map(v =>
      `<option value="${v.id}">${esc(v.titel)} — ${esc(v.inlener)}</option>`).join('')}</select>`;
  root.append(kies);

  const uitvoer = el('div');
  root.append(uitvoer);

  const toon = () => {
    uitvoer.innerHTML = '';
    const v = vacatureVan(kies.querySelector('#ct-vac').value);
    if (!v) return;
    const varianten = [
      ['direct-starten', '🚀 "Deze week starten"-post'],
      ['intercedent', '👋 Intercedent aan het woord'],
      ['meeloopdag', '☕ Meeloopdag i.p.v. vacature']
    ];
    for (const [variant, titel] of varianten) {
      const tekst = socialPost(v, variant);
      const kaart = el('div', 'kaart');
      kaart.append(el('h4', null, titel));
      const pre = el('pre', 'post-tekst');
      pre.textContent = tekst;
      kaart.append(pre);
      const kopieer = el('button', 'knop', '📋 Kopieer');
      kopieer.onclick = async () => {
        try { await navigator.clipboard.writeText(tekst); kopieer.textContent = '✅ Gekopieerd'; }
        catch (e) { kopieer.textContent = '⚠️ Selecteer en kopieer handmatig'; }
        setTimeout(() => { kopieer.textContent = '📋 Kopieer'; }, 1500);
      };
      kaart.append(kopieer);
      uitvoer.append(kaart);
    }
  };
  kies.querySelector('#ct-vac').onchange = toon;
  toon();
}

/* ---------- Kennismaken (events) ---------- */

function renderEvents(root) {
  root.append(el('h2', null, '☕ Laagdrempelig kennismaken'));
  root.append(el('p', 'uitleg',
    'Ruim 1 op de 3 werkzoekenden staat open voor meeloopdagen, open dagen en informele gesprekken — zonder sollicitatiedruk. ' +
    'Plan een vast maandelijks inloopmoment per filiaal en adverteer de meeloopdag in plaats van de vacature.'));

  const form = el('div', 'formulier');
  form.innerHTML = `
    <select id="ev-type"><option>Inloopdag</option><option>Meeloopdag</option><option>Rondleiding</option><option>Workshop</option></select>
    <input id="ev-titel" placeholder="Titel (bijv. Koffie & werk)">
    <input id="ev-locatie" placeholder="Locatie">
    <input id="ev-datum" type="date">
    <button class="knop knop-primair" id="ev-toevoegen">+ Plan event</button>`;
  root.append(form);
  form.querySelector('#ev-toevoegen').onclick = () => {
    const titel = form.querySelector('#ev-titel').value.trim();
    const locatie = form.querySelector('#ev-locatie').value.trim();
    const datum = form.querySelector('#ev-datum').value;
    if (!titel || !locatie || !datum) return alert('Vul titel, locatie en datum in.');
    db.events.push({ id: 'e' + Date.now(), type: form.querySelector('#ev-type').value, titel, locatie, datum, aanmeldingen: 0 });
    saveDB(db); render();
  };

  for (const e of [...db.events].sort((a, b) => a.datum.localeCompare(b.datum))) {
    const kaart = el('div', 'kaart');
    kaart.append(el('div', null,
      `<strong>${esc(e.type)}: ${esc(e.titel)}</strong><br>` +
      `<span class="klein">📍 ${esc(e.locatie)} · 📅 ${new Date(e.datum).toLocaleDateString('nl-NL', { weekday: 'long', day: 'numeric', month: 'long' })} · ${e.aanmeldingen} aanmelding(en)</span>`));
    const acties = el('div', 'acties');
    const plus = el('button', 'knop', '+1 aanmelding');
    plus.onclick = () => { e.aanmeldingen++; saveDB(db); render(); };
    acties.append(plus);
    kaart.append(acties);
    root.append(kaart);
  }
}

/* ---------- Hoofd-render ---------- */

const RENDERERS = {
  dashboard: renderDashboard,
  radar: renderRadar,
  aanmeldingen: renderAanmeldingen,
  vacatures: renderVacatures,
  referrals: renderReferrals,
  content: renderContent,
  events: renderEvents
};

function render() {
  renderNav();
  const root = $('#inhoud');
  root.innerHTML = '';
  RENDERERS[actieveTab](root);
  $('#wie').value = INTERCEDENT.naam;
}

document.addEventListener('DOMContentLoaded', () => {
  $('#wie').onchange = e => { INTERCEDENT.wijzig(e.target.value.trim() || 'collega'); render(); };
  $('#reset').onclick = () => {
    if (confirm('Alle lokale data wissen en demodata opnieuw laden?')) { db = resetDB(); render(); }
  };
  render();
  // SLA-timers live houden
  setInterval(() => { if (actieveTab === 'aanmeldingen' || actieveTab === 'dashboard') render(); }, 30000);
});
