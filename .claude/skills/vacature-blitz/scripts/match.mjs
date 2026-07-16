#!/usr/bin/env node
/**
 * vacature-blitz match.mjs — radar-scoring & skills-matching vanaf de CLI.
 *
 * Gebruik:
 *   node match.mjs --vacature vacature.json --kandidaten kandidaten.json [--top 15] [--json]
 *
 * Invoer:
 *   vacature.json   — zie templates/vacature.schema.json
 *   kandidaten.json — array van kandidaten (zie templates/kandidaten.voorbeeld.json)
 *   kandidaten.csv  — zelfde velden als kolommen; skills gescheiden met ';'
 *
 * Uitvoer: markdown-rapport op stdout (of JSON met --json).
 * Scoringsspecificatie: ../references/scoring.md
 */

import { readFileSync } from 'node:fs';

/* ---------- argumenten ---------- */

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const val = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
      args[key] = val;
    }
  }
  return args;
}

const args = parseArgs(process.argv);
if (!args.vacature || !args.kandidaten) {
  console.error('Gebruik: node match.mjs --vacature <json> --kandidaten <json|csv> [--top N] [--json]');
  process.exit(2);
}

/* ---------- inlezen ---------- */

function leesKandidaten(pad) {
  const raw = readFileSync(pad, 'utf8');
  if (pad.toLowerCase().endsWith('.csv')) return parseCsv(raw);
  const data = JSON.parse(raw);
  return Array.isArray(data) ? data : data.kandidaten;
}

// kolomkoppen (lowercase, zonder underscores) -> canonieke veldnamen
const CSV_VELDEN = {
  naam: 'naam', telefoon: 'telefoon', woonplaats: 'woonplaats', functie: 'functie',
  skills: 'skills', beschikbaar: 'beschikbaar', laatstcontact: 'laatstContact',
  plaatsingen: 'plaatsingen', willeren: 'wilLeren', bron: 'bron'
};

function parseCsv(raw) {
  const regels = raw.trim().split(/\r?\n/);
  const kop = splitsCsvRegel(regels[0]).map(h => {
    const sleutel = h.trim().toLowerCase().replace(/[_\s-]/g, '');
    return CSV_VELDEN[sleutel] || h.trim();
  });
  return regels.slice(1).filter(r => r.trim()).map(regel => {
    const velden = splitsCsvRegel(regel);
    const k = {};
    kop.forEach((h, i) => { k[h] = (velden[i] || '').trim(); });
    k.skills = (k.skills || '').split(';').map(s => s.trim()).filter(Boolean);
    k.plaatsingen = parseInt(k.plaatsingen, 10) || 0;
    k.wilLeren = /^(true|ja|1|x)$/i.test(String(k.wilLeren || ''));
    return k;
  });
}

function splitsCsvRegel(regel) {
  const velden = [];
  let huidig = '', inQuotes = false;
  for (let i = 0; i < regel.length; i++) {
    const c = regel[i];
    if (c === '"') {
      if (inQuotes && regel[i + 1] === '"') { huidig += '"'; i++; }
      else inQuotes = !inQuotes;
    } else if (c === ',' && !inQuotes) { velden.push(huidig); huidig = ''; }
    else huidig += c;
  }
  velden.push(huidig);
  return velden;
}

let vacature, kandidaten;
try {
  vacature = JSON.parse(readFileSync(args.vacature, 'utf8'));
  kandidaten = leesKandidaten(args.kandidaten);
} catch (e) {
  console.error('Kan invoer niet lezen: ' + e.message);
  process.exit(2);
}
if (!Array.isArray(kandidaten) || !kandidaten.length) {
  console.error('Geen kandidaten gevonden in ' + args.kandidaten);
  process.exit(2);
}

/* ---------- scoring (spec: references/scoring.md) ---------- */

const dagenSinds = iso => iso ? Math.floor((Date.now() - new Date(iso).getTime()) / 86400000) : null;

function skillOverlap(kandidaatSkills, vacatureSkills) {
  const set = new Set((kandidaatSkills || []).map(s => s.toLowerCase()));
  return (vacatureSkills || []).filter(s => set.has(s.toLowerCase())).length;
}

function radarScore(k, vac) {
  const redenen = [];
  let score = 0;

  const dagen = dagenSinds(k.laatstContact);
  let timing;
  if (dagen === null)     timing = 15; // onbekend: neutraal
  else if (dagen < 21)    timing = 5;
  else if (dagen <= 60)   timing = 18;
  else if (dagen <= 270)  timing = 30;
  else if (dagen <= 420)  timing = 20;
  else                    timing = 10;
  score += timing;
  redenen.push(`timing ${dagen === null ? 'onbekend' : dagen + ' dgn sinds contact'}: +${timing}/30`);

  const historie = Math.min(25, (k.plaatsingen || 0) * 6);
  score += historie;
  redenen.push(`${k.plaatsingen || 0} eerdere plaatsing(en): +${historie}/25`);

  const overlap = skillOverlap(k.skills, vacature.skills);
  const vraag = overlap ? Math.min(30, 12 + overlap * 9) : 0;
  score += vraag;
  redenen.push(`${overlap} skill(s) match op ${vac.functietitel}: +${vraag}/30`);

  const b = String(k.beschikbaar || '').toLowerCase();
  const beschikbaar = !b ? 10 : b.includes('direct') ? 15 : b.includes('overleg') ? 8 : 10;
  score += beschikbaar;
  redenen.push(`beschikbaar (${k.beschikbaar || 'onbekend'}): +${beschikbaar}/15`);

  return { score, overlap, redenen };
}

/* ---------- matching-lagen ---------- */

const vereist = Math.min(2, (vacature.skills || []).length);
const direct = [];
const opleidbaar = [];

for (const k of kandidaten) {
  const r = radarScore(k, vacature);
  const item = { kandidaat: k, ...r };
  if (r.overlap >= vereist && vereist > 0) direct.push(item);
  else if (vacature.opleidbaar && r.overlap >= 1 && k.wilLeren) opleidbaar.push(item);
  else if (vacature.opleidbaar && k.wilLeren &&
           String(k.beschikbaar || '').toLowerCase().includes('direct')) opleidbaar.push(item);
}

const sorteer = lijst => lijst.sort((a, b) => b.score - a.score || b.overlap - a.overlap);
sorteer(direct);
sorteer(opleidbaar);

const top = parseInt(args.top, 10) || 15;

/* ---------- uitvoer ---------- */

if (args.json) {
  console.log(JSON.stringify({
    vacature: vacature.functietitel,
    direct: direct.slice(0, top),
    opleidbaar: opleidbaar.slice(0, top)
  }, null, 2));
  process.exit(0);
}

const advies = s => s >= 70 ? '🔥 vandaag bellen' : s >= 45 ? '📅 deze week' : '🗂 talentpool';

console.log(`# Radar-rapport: ${vacature.functietitel} — ${vacature.inlener || '?'} (${vacature.plaats || '?'})`);
console.log(`\nGevraagde skills: ${(vacature.skills || []).join(', ')} · opleidbaar: ${vacature.opleidbaar ? 'ja' : 'nee'}`);
console.log(`Doorzocht: ${kandidaten.length} kandidaten · directe matches: ${direct.length} · opleidbaar: ${opleidbaar.length}\n`);

function printLijst(titel, lijst) {
  console.log(`## ${titel}\n`);
  if (!lijst.length) { console.log('_geen_\n'); return; }
  lijst.slice(0, top).forEach((m, i) => {
    const k = m.kandidaat;
    console.log(`${i + 1}. **${k.naam}** — score ${m.score}/100 (${advies(m.score)})`);
    console.log(`   ${k.functie || '?'} · ${k.woonplaats || '?'} · ${k.telefoon || 'geen nummer'} · skills: ${(k.skills || []).join(', ') || '—'}`);
    console.log(`   _${m.redenen.join(' · ')}_\n`);
  });
}

printLijst('Directe matches', direct);
printLijst('Opleidbare matches (brede vijver)', opleidbaar);

if (!vacature.opleidbaar) {
  console.log('> ⚠️ Vacature is niet als opleidbaar gemarkeerd — de "brede vijver" blijft dicht.');
  console.log('> Bespreek met de inlener welke eis kan vervallen bij instructie on-the-job.');
}
