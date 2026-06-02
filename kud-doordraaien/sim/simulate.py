#!/usr/bin/env python3
"""
simulate.py — speelbare regelengine + playtest-simulatie van KUD: DOORDRAAIEN (Kijkcijfers-modus).

Abstractie: het bord wordt gemodelleerd als een verzameling OPEN VERHAALLIJNEN (kleur + lengte).
Dat vangt de strategische kern (poort-economie, dumpen, cappen, verstikken) zonder de exacte 2D-
vertakkingsgeometrie. Vier speelstijl-profielen (de beta-testers) sturen een heuristische AI.

Draait een round-robin (alle 6 paren), meerdere potjes per paar, en schrijft:
  results.md       — geaggregeerde statistieken + balans-signalen
  sample_game.md   — één becommentarieerd potje, beurt voor beurt
"""
from __future__ import annotations
import random, statistics as st
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = ["G", "R", "B", "Y"]

# ---------------------------------------------------------------- deck
def make_deck(seed):
    rng = random.Random(seed)
    deck = []
    def col(): return rng.choice(COLORS)
    for _ in range(52):
        c = col()
        if rng.random() < 0.6: deck.append(("splice", c, c))
        else: deck.append(("splice", c, col()))
    for _ in range(10): deck.append(("branch", col(), None))
    for _ in range(8):  deck.append(("merge", col(), None))
    for _ in range(12): deck.append(("einde", col(), None))
    for _ in range(4):  deck.append(("pilon", "*", None))
    acts = ["knip","knip","cliffhanger","cliffhanger","cliffhanger",
            "voorvertoning","voorvertoning","herschrijven","archief","archief"]
    for a in acts: deck.append(("action", a, None))
    rng.shuffle(deck)
    return deck

# ---------------------------------------------------------------- profiles (de testers)
PROFILES = {
    "Sven":  dict(branch=2.2, cap_thresh=1, cap_w=1.0, steal=0.3, merge=0.2,
                  aggression=0.8, max_chain=6, noise=0.4, speed=True),
    "Marit": dict(branch=1.0, cap_thresh=4, cap_w=1.8, steal=1.4, merge=0.9,
                  aggression=0.2, max_chain=4, noise=0.15, speed=False),
    "Joost": dict(branch=1.2, cap_thresh=2, cap_w=1.0, steal=0.5, merge=0.5,
                  aggression=0.35, max_chain=4, noise=0.9, speed=False),
    "Eline": dict(branch=1.3, cap_thresh=3, cap_w=1.5, steal=1.2, merge=1.1,
                  aggression=0.7, max_chain=5, noise=0.1, speed=True),
}

# ---------------------------------------------------------------- game state
class Game:
    def __init__(self, seed, a, b):
        self.rng = random.Random(seed)
        self.deck = make_deck(seed)
        self.lines = [{"color": c, "length": 1} for c in COLORS]   # Leader: 4 open draden
        self.players = [a, b]
        self.hands = {a: [self.deck.pop() for _ in range(7)],
                      b: [self.deck.pop() for _ in range(7)]}
        self.score = {a: 0, b: 0}
        self.emptied = None
        self.stats = defaultdict(Counter)     # per player kind-counter
        self.draw_pen = {a: 0, b: 0}
        self.turns = 0
        self.log = []

    def draw(self, p, n):
        for _ in range(n):
            if self.deck: self.hands[p].append(self.deck.pop())

    # candidate single plays for a card
    def playable_targets(self, card):
        kind, c, c2 = card
        idxs = []
        if kind in ("splice","branch","einde"):
            idxs = [i for i,l in enumerate(self.lines) if l["color"]==c]
        elif kind == "pilon":
            idxs = list(range(len(self.lines)))
        elif kind == "merge":
            same = [i for i,l in enumerate(self.lines) if l["color"]==c]
            idxs = [tuple(same[:2])] if len(same)>=2 else []
        return idxs

    def legal_plays(self, p):
        out = []
        for card in self.hands[p]:
            for t in self.playable_targets(card):
                out.append((card, t))
        return out

    def move_value(self, p, card, t, prof):
        kind, c, c2 = card
        hand_colors = Counter()
        for k,cc,_ in self.hands[p]:
            if k in ("splice","branch","einde","merge"): hand_colors[cc]+=1
        v = 1.0  # dumpen is goed
        if kind == "einde":
            ln = self.lines[t]["length"]
            if ln >= prof["cap_thresh"]: v += ln * prof["cap_w"]
            else: v -= (prof["cap_thresh"]-ln)*0.6
            if ln == max(l["length"] for l in self.lines): v += prof["steal"]*ln*0.3
        elif kind == "branch":
            v += prof["branch"]
            v += hand_colors[c]*0.25            # meer outs in jouw kleur = goed
        elif kind == "merge":
            v += prof["merge"]
        elif kind == "splice":
            v += hand_colors[c2]*0.3            # zet de draad naar jouw sterke kleur
        elif kind == "pilon":
            best = max(COLORS, key=lambda x: hand_colors[x])
            v += 0.5 + hand_colors[best]*0.2
        return v + self.rng.uniform(0, prof["noise"])

    def apply(self, p, card, t):
        kind, c, c2 = card
        self.hands[p].remove(card)
        self.stats[p][kind]+=1
        if kind == "splice":
            self.lines[t]["length"]+=1; self.lines[t]["color"]=c2
        elif kind == "pilon":
            best = Counter(cc for k,cc,_ in self.hands[p] if k!="action" and cc in COLORS)
            tgt = (best.most_common(1)[0][0] if best else self.lines[t]["color"])
            self.lines[t]["length"]+=1; self.lines[t]["color"]=tgt
        elif kind == "branch":
            par = self.lines.pop(t)
            for _ in range(2): self.lines.append({"color":c,"length":par["length"]+1})
        elif kind == "merge":
            i,j = t
            l1,l2 = self.lines[i], self.lines[j]
            newlen = l1["length"]+l2["length"]+1
            for k in sorted((i,j), reverse=True): self.lines.pop(k)
            self.lines.append({"color":c,"length":newlen})
        elif kind == "einde":
            ln = self.lines.pop(t); self.score[p]+=ln["length"]
            return ln["length"]
        return None

    def try_action(self, p, opp, prof):
        acts = [card for card in self.hands[p] if card[0]=="action"]
        if not acts: return None
        # verstikt? geen legale zet -> knip om bord te heropenen
        if not self.legal_plays(p):
            for card in acts:
                if card[1]=="knip" and self.lines:
                    self.hands[p].remove(card); self.stats[p]["action"]+=1
                    src = max(range(len(self.lines)), key=lambda i:self.lines[i]["length"])
                    par = self.lines.pop(src); half=max(1,par["length"]//2)
                    self.lines += [{"color":par["color"],"length":half},
                                   {"color":par["color"],"length":half}]
                    return ("knip", par["color"])
            for card in acts:                  # anders filter-actie
                if card[1] in ("archief","voorvertoning","herschrijven"):
                    self.hands[p].remove(card); self.stats[p]["action"]+=1
                    self.draw(p, 1)
                    if card[1] in ("archief","herschrijven") and self.hands[p]:
                        self.hands[p].pop(0)
                    return (card[1], None)
            return None
        # agressie: cliffhanger als tegenstander bijna leeg is
        if self.rng.random() < prof["aggression"] and len(self.hands[opp])<=4:
            for card in acts:
                if card[1]=="cliffhanger":
                    self.hands[p].remove(card); self.stats[p]["action"]+=1
                    self.draw(opp, 2)
                    return ("cliffhanger", None)
        return None

    def take_turn(self, p, opp, prof, narrate=False):
        self.turns += 1
        act = self.try_action(p, opp, prof)
        if act:
            if narrate: self.log.append(f"  {p} speelt ACTIE **{act[0]}**"
                                        + (f" ({act[1]})" if act[1] else ""))
            return True
        played = 0; caps=[]
        while played < prof["max_chain"]:
            moves = self.legal_plays(p)
            if not moves: break
            card, t = max(moves, key=lambda m: self.move_value(p, m[0], m[1], prof))
            val = self.move_value(p, card, t, prof)
            if played >= 1 and not prof["speed"] and val < 1.2 and card[0]!="einde":
                break
            capped = self.apply(p, card, t); played += 1
            if capped is not None: caps.append(capped)
            if not self.hands[p]:
                self.emptied = p; self.score[p]+=5
                if narrate: self.log.append(f"  {p} legt een ketting van {played} en **maakt de hand leeg** (+5 finale)")
                return True
        if played == 0:
            if self.deck:
                self.draw(p, 2); self.draw_pen[p]+=1
                if narrate: self.log.append(f"  {p} kan NIETS leggen → trekt 2 (verstikt)")
                return True
            if narrate: self.log.append(f"  {p} kan niets en de stapel is op → **past**")
            return False           # echte pas (deck leeg)
        if narrate:
            cs = f", capt {caps} kijkcijfers" if caps else ""
            self.log.append(f"  {p} monteert {played} scène(s){cs}  · open draden: {len(self.lines)} · score {self.score[p]}")
        return True

    def run(self, narrate=False):
        order = list(self.players); no_prog=0
        for _ in range(300):
            for p in order:
                opp = self.players[1] if p==self.players[0] else self.players[0]
                prog = self.take_turn(p, opp, PROFILES[p], narrate)
                if self.emptied:
                    return self.finish()
                no_prog = 0 if prog else no_prog+1
                if no_prog >= 4:          # beide spelers vast → deck-out
                    return self.finish()
        return self.finish()

    def finish(self):
        a,b = self.players
        win = a if self.score[a]>self.score[b] else (b if self.score[b]>self.score[a] else None)
        return dict(winner=win, score=dict(self.score), emptied=self.emptied,
                    turns=self.turns, draw_pen=dict(self.draw_pen),
                    stats={p:dict(self.stats[p]) for p in self.players},
                    margin=abs(self.score[a]-self.score[b]))

# ---------------------------------------------------------------- run round-robin
def main():
    names = list(PROFILES); pairs=[(names[i],names[j]) for i in range(4) for j in range(i+1,4)]
    GAMES = 60
    wins = Counter(); h2h = defaultdict(lambda: Counter()); scores=defaultdict(list)
    margins=[]; turnlist=[]; finale=0; pointwin=0; draws=0; first_adv=0
    drawpens=[]; usage=Counter()
    for (a,b) in pairs:
        for g in range(GAMES):
            first,second = (a,b) if g%2==0 else (b,a)
            res = Game(seed=1000*hash((a,b))%99999 + g, a=first, b=second).run()
            w=res["winner"]
            if w is None: draws+=1
            else:
                wins[w]+=1; h2h[w][b if w==a else a]+=1 if False else 0  # placeholder
            if w: h2h[(a,b)][w]+=1
            if res["emptied"] and w==res["emptied"]: finale+=1
            elif w: pointwin+=1
            if w==first: first_adv+=1
            margins.append(res["margin"]); turnlist.append(res["turns"])
            for p in (a,b):
                scores[p].append(res["score"][p]); drawpens.append(res["draw_pen"][p])
                for k,v in res["stats"][p].items(): usage[k]+=v
    total = len(pairs)*GAMES

    def pct(x): return f"{100*x/total:.0f}%"
    lines = []
    lines.append("# KUD: Doordraaien — playtest-resultaten\n")
    lines.append(f"_Gesimuleerd met de regelengine. **{total} potjes** (6 paren × {GAMES}), "
                 f"Kijkcijfers-modus. Bordmodel = open verhaallijnen (zie kop van `simulate.py`)._\n")
    lines.append("## Winst per tester (overall)\n")
    lines.append("| Tester | Stijl | Winst | Gem. kijkcijfers |")
    lines.append("|---|---|---|---|")
    styl = {"Sven":"chaos/snel","Marit":"melken/strategie","Joost":"casual/thema","Eline":"tempo/denial"}
    for n in sorted(names, key=lambda x:-wins[x]):
        lines.append(f"| {n} | {styl[n]} | {wins[n]} ({100*wins[n]/total:.0f}% v.d. potjes) | {st.mean(scores[n]):.1f} |")
    lines.append("\n## Onderlinge duels (winnaar per paar)\n")
    lines.append("| Duel | Stand |")
    lines.append("|---|---|")
    for (a,b) in pairs:
        c=h2h[(a,b)]; lines.append(f"| {a} vs {b} | {a} {c[a]} – {c[b]} {b} |")
    lines.append("\n## Balans- & speelgevoel-signalen\n")
    lines.append(f"- **Beslissing:** {pct(finale)} potjes beslist door hand-leeg-finale, "
                 f"{pct(pointwin)} op pure kijkcijfers, {pct(draws)} gelijk.")
    lines.append(f"- **Gem. potjeslengte:** {st.mean(turnlist):.0f} beurten (spreiding {min(turnlist)}–{max(turnlist)}).")
    lines.append(f"- **Margins:** gemiddeld {st.mean(margins):.1f} kijkcijfers; "
                 f"close (≤3): {100*sum(1 for m in margins if m<=3)/len(margins):.0f}%, "
                 f"blowout (≥12): {100*sum(1 for m in margins if m>=12)/len(margins):.0f}%.")
    lines.append(f"- **Beurtspeler-voordeel:** wie eerst begint wint {100*first_adv/total:.0f}% — "
                 f"{'scheef!' if abs(first_adv/total-0.5)>0.08 else 'redelijk in balans'}.")
    lines.append(f"- **Verstikking:** gem. {st.mean(drawpens):.2f} trekstraf-beurten per speler per potje "
                 f"({'vaak — bord choke is sterk' if st.mean(drawpens)>1 else 'matig'}).")
    tot_play = sum(usage.values())
    lines.append(f"- **Kaartgebruik:** " + ", ".join(f"{k} {100*v/tot_play:.0f}%" for k,v in usage.most_common()))
    Path(HERE/"results.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(f"results.md geschreven · {total} potjes")
    print("Winst:", dict(wins))

    # sample-potje (becommentarieerd)
    g = Game(seed=4242, a="Marit", b="Sven"); g.run(narrate=True)
    sl = ["# Voorbeeldpotje — Marit (melken) vs Sven (chaos)\n",
          "_Seed 4242. Zo verloopt een typisch potje, beurt voor beurt._\n"]
    sl += g.log
    sl.append(f"\n**Eind:** Marit {g.score['Marit']} – {g.score['Sven']} Sven · "
              f"{'hand leeg door '+g.emptied if g.emptied else 'deck op'} · {g.turns} beurten.")
    Path(HERE/"sample_game.md").write_text("\n".join(sl)+"\n", encoding="utf-8")
    print("sample_game.md geschreven")

if __name__ == "__main__":
    main()
