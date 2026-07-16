/* =========================================================
   Wervingscockpit — berichtgenerator
   WhatsApp-teksten (wa.me deeplinks) en social posts per
   vacature, in de toon die het advies voorschrijft: kort,
   persoonlijk, concreet ("deze week te starten").
   ========================================================= */

const INTERCEDENT = {
  naam: localStorage.getItem('wc_intercedent') || 'Sanne',
  wijzig(naam) {
    this.naam = naam;
    localStorage.setItem('wc_intercedent', naam);
  }
};

function voornaam(volledigeNaam) {
  return volledigeNaam.split(' ')[0];
}

function waLink(telefoon, tekst) {
  const nr = '31' + telefoon.replace(/\D/g, '').replace(/^0/, '');
  return `https://wa.me/${nr}?text=${encodeURIComponent(tekst)}`;
}

/* ---------- WhatsApp: reactivering (bellijst) ---------- */

function reactiveringsBericht(kandidaat, vacature) {
  const vn = voornaam(kandidaat.naam);
  if (vacature) {
    return `Hoi ${vn}! ${INTERCEDENT.naam} hier van Olympia. Ik heb werk dat bij je past: ${vacature.titel} bij ${vacature.inlener} in ${vacature.plaats} (${vacature.salaris}, start ${vacature.start}). Zin om vandaag even te bellen? 😊`;
  }
  return `Hoi ${vn}! ${INTERCEDENT.naam} hier van Olympia. We hebben weer volop werk in de regio — zal ik je bellen om te kijken wat er nu bij je past?`;
}

/* ---------- WhatsApp: reactie op nieuwe aanmelding ---------- */

function aanmeldingsBericht(aanmelding, vacature) {
  const vn = voornaam(aanmelding.naam);
  return `Hoi ${vn}, bedankt voor je aanmelding voor ${vacature ? vacature.titel : 'de vacature'}! Ik ben ${INTERCEDENT.naam} van Olympia en ik bel je vandaag nog. Kun je alvast appen wanneer je zou kunnen starten?`;
}

/* ---------- WhatsApp: referral-promo ---------- */

function referralBericht(kandidaat, bonus = 200) {
  const vn = voornaam(kandidaat.naam);
  return `Hoi ${vn}! Ken jij iemand die werk zoekt? Voor elke aangebrachte collega die bij ons start krijg je €${bonus} (deels na 8 gewerkte weken). Stuur gewoon een naam + nummer door. Groet, ${INTERCEDENT.naam} — Olympia`;
}

/* ---------- Social posts (Facebook / Instagram) ---------- */

function socialPost(vacature, variant) {
  const basis = `📍 ${vacature.plaats} | 💶 ${vacature.salaris} | ⏰ ${vacature.uren}`;
  const cta = `App je naam + woonplaats naar ${INTERCEDENT.naam} en we bellen je VANDAAG. Geen cv nodig.`;

  switch (variant) {
    case 'direct-starten':
      return `🚀 DEZE WEEK NOG STARTEN?\n\nWe zoeken per direct een ${vacature.titel.toLowerCase()} bij ${vacature.inlener}.\n${basis}\n\n${vacature.opleidbaar ? '✅ Geen diploma nodig — wij leren het je on-the-job.\n' : ''}👉 ${cta}\n\n#werk #${vacature.plaats.toLowerCase()} #vacature`;
    case 'intercedent':
      return `Hoi! Ik ben ${INTERCEDENT.naam} van Olympia 👋\n\nIk zoek deze week een ${vacature.titel.toLowerCase()} voor ${vacature.inlener} in ${vacature.plaats}. Leuk team, ${vacature.salaris}, start ${vacature.start}.\n\nKen je iemand (of ben je het zelf)? Stuur me een appje — ik reageer binnen een uur. 📱`;
    case 'meeloopdag':
      return `☕ EERST KIJKEN, DAN BESLISSEN\n\nTwijfel je of werken bij ${vacature.inlener} iets voor je is? Loop een dagje mee — geen sollicitatie, geen cv, gewoon kijken.\n${basis}\n\n👉 App ${INTERCEDENT.naam} van Olympia voor een datum.`;
    default:
      return `${vacature.titel} — ${vacature.inlener}\n${basis}\n${cta}`;
  }
}
