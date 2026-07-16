/* =========================================================
   Wervingscockpit — Latente Kandidaat Radar & skills-matching

   De "edge": in plaats van wachten op actieve zoekers (<10% van
   de doelgroep) rangschikt de radar de eigen database op de kans
   dat reactivering NU lukt. Elke score is uitlegbaar: de
   intercedent ziet per kandidaat wáárom die bovenaan staat.
   ========================================================= */

/* ---------- Hulpfuncties ---------- */

function dagenSinds(iso) {
  return Math.floor((Date.now() - new Date(iso).getTime()) / 86400000);
}

function skillOverlap(kandidaatSkills, vacatureSkills) {
  const set = new Set(kandidaatSkills.map(s => s.toLowerCase()));
  return vacatureSkills.filter(s => set.has(s.toLowerCase())).length;
}

/* ---------- Reactiveringsscore (0–100) ----------
   Vier uitlegbare componenten:
   1. Timing      (0–30) — sweet spot 60–270 dagen sinds laatste contact:
                    lang genoeg dat de situatie veranderd kan zijn, kort
                    genoeg dat het bureau nog "warm" is.
   2. Historie    (0–25) — eerdere succesvolle plaatsingen voorspellen
                    plaatsbaarheid én vertrouwen in het bureau.
   3. Vraag       (0–30) — skills-overlap met NU openstaande vacatures:
                    bellen met concreet werk converteert, bellen "om bij
                    te praten" niet.
   4. Direct      (0–15) — beschikbaarheid: 'direct' scoort maximaal.
--------------------------------------------------- */

function reactiveringsScore(kandidaat, openVacatures) {
  const redenen = [];
  let score = 0;

  // 1. Timing
  const dagen = dagenSinds(kandidaat.laatstContact);
  let timing;
  if (dagen < 21)        timing = 5;   // net gesproken, weinig nieuws
  else if (dagen <= 60)  timing = 18;
  else if (dagen <= 270) timing = 30;  // sweet spot
  else if (dagen <= 420) timing = 20;
  else                   timing = 10;  // koud, maar niet kansloos
  score += timing;
  redenen.push({ label: `Laatste contact ${dagen} dagen geleden`, punten: timing, max: 30 });

  // 2. Historie
  const historie = Math.min(25, kandidaat.plaatsingen * 6);
  score += historie;
  redenen.push({ label: `${kandidaat.plaatsingen} eerdere plaatsing(en) via ons`, punten: historie, max: 25 });

  // 3. Vraag: beste match met openstaande vacatures
  let besteMatch = null;
  let besteOverlap = 0;
  for (const v of openVacatures) {
    const o = skillOverlap(kandidaat.skills, v.skills);
    if (o > besteOverlap) { besteOverlap = o; besteMatch = v; }
  }
  const vraag = besteMatch ? Math.min(30, 12 + besteOverlap * 9) : 0;
  score += vraag;
  redenen.push({
    label: besteMatch
      ? `Skills passen op openstaande vacature: ${besteMatch.titel} (${besteMatch.inlener})`
      : 'Geen openstaande vacature die past — alleen bellen voor talentpool',
    punten: vraag, max: 30
  });

  // 4. Beschikbaarheid
  const b = (kandidaat.beschikbaar || '').toLowerCase();
  const direct = b.includes('direct') ? 15 : b.includes('overleg') ? 8 : 10;
  score += direct;
  redenen.push({ label: `Beschikbaarheid: ${kandidaat.beschikbaar}`, punten: direct, max: 15 });

  return { score, redenen, besteMatch };
}

/* Dagelijkse bellijst: top-N inactieve kandidaten op reactiveringsscore.
   Kandidaten die vandaag al gebeld zijn (belLog) worden overgeslagen. */
function bouwBellijst(db, n = 10) {
  const open = db.vacatures.filter(v => v.status === 'open');
  const vandaag = new Date().toISOString().slice(0, 10);
  const vandaagGebeld = new Set(
    db.belLog.filter(l => l.datum.slice(0, 10) === vandaag).map(l => l.kandidaatId)
  );

  return db.kandidaten
    .filter(k => k.status !== 'actief' && !vandaagGebeld.has(k.id))
    .map(k => ({ kandidaat: k, ...reactiveringsScore(k, open) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, n);
}

/* ---------- Skills-based matching per vacature ----------
   Twee lagen, conform "breder werven en opleiden":
   - directe matches: voldoende skills-overlap
   - opleidbare matches: gedeeltelijke overlap + wil leren,
     alleen als de vacature 'opleidbaar' is gemarkeerd.
--------------------------------------------------------- */

function matchesVoorVacature(db, vacature) {
  const direct = [];
  const opleidbaar = [];

  for (const k of db.kandidaten) {
    const overlap = skillOverlap(k.skills, vacature.skills);
    if (overlap >= Math.min(2, vacature.skills.length)) {
      direct.push({ kandidaat: k, overlap });
    } else if (vacature.opleidbaar && overlap >= 1 && k.wilLeren) {
      opleidbaar.push({ kandidaat: k, overlap });
    } else if (vacature.opleidbaar && overlap === 0 && k.wilLeren && k.beschikbaar.toLowerCase().includes('direct')) {
      // brede vijver: direct beschikbaar én leerbereid — zichtbaar maken, laag gerangschikt
      opleidbaar.push({ kandidaat: k, overlap: 0 });
    }
  }

  direct.sort((a, b) => b.overlap - a.overlap || b.kandidaat.plaatsingen - a.kandidaat.plaatsingen);
  opleidbaar.sort((a, b) => b.overlap - a.overlap);
  return { direct, opleidbaar };
}

/* ---------- SLA (snelheid als wapen) ---------- */

const SLA_MINUTEN = 60; // norm: eerste reactie binnen 1 uur

function slaStatus(aanmelding) {
  if (aanmelding.eersteReactie) {
    const min = Math.round((new Date(aanmelding.eersteReactie) - new Date(aanmelding.binnen)) / 60000);
    return { fase: min <= SLA_MINUTEN ? 'gehaald' : 'gemist', minuten: min };
  }
  const min = Math.round((Date.now() - new Date(aanmelding.binnen)) / 60000);
  if (min <= 30) return { fase: 'groen', minuten: min };
  if (min <= SLA_MINUTEN) return { fase: 'oranje', minuten: min };
  return { fase: 'rood', minuten: min };
}

/* ---------- KPI's (de vier kengetallen uit het advies) ---------- */

function berekenKpis(db) {
  const beantwoord = db.aanmeldingen.filter(a => a.eersteReactie);
  const reactieMinuten = beantwoord.map(a =>
    Math.round((new Date(a.eersteReactie) - new Date(a.binnen)) / 60000));
  const gemiddeldeReactie = reactieMinuten.length
    ? Math.round(reactieMinuten.reduce((s, m) => s + m, 0) / reactieMinuten.length)
    : null;

  const dezeWeek = Date.now() - 7 * 86400000;
  const gereactiveerd = db.belLog.filter(l =>
    new Date(l.datum).getTime() >= dezeWeek && l.uitkomst === 'interesse').length;

  const referralsNieuw = db.referrals.filter(r =>
    new Date(r.datum).getTime() >= Date.now() - 30 * 86400000).length;

  const perKanaal = {};
  for (const a of db.aanmeldingen.filter(a => a.plaatsing)) {
    perKanaal[a.kanaal] = (perKanaal[a.kanaal] || 0) + 1;
  }

  return { gemiddeldeReactie, gereactiveerd, referralsNieuw, perKanaal };
}
