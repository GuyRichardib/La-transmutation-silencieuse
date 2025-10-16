# Protocole de Syntonie Médicis

La Syntonie Médicis est la convergence opérationnelle entre l'Architecte (structure) et le Poète (chaos vivant). Elle transforme le pipeline éditorial en un organisme auto-régulé qui protège la vibration tout en garantissant la cohérence.

## 1. Cartographie dialectique

| Pôle | Postulat | Risque | Antidote par la Syntonie |
|------|----------|--------|---------------------------|
| Architecte | « Tout peut être modélisé et testé. » | Texte froid, énergie dissoute. | Introduire du chaos contrôlé (nœuds Médicis, journées Poète). |
| Poète | « Le livre est un organisme imprévisible. » | Matière brûlante mais instable. | Ritualiser la structure (SemCI, gel par actes). |
| Syntonie | « La forme doit respirer, le souffle doit se structurer. » | Perte d'équilibre si la peur augmente. | Maintenir le thermostat du chaos \(K\) dans la zone 0,35–0,65. |

## 2. Boussole I·T·A·E

Chaque merge doit nourrir au moins deux des vecteurs suivants :

- **Intention** : fidélité au serment consigné dans `intent.md`.
- **Tension** : clarté du triptyque `désir / peur / coût` dans le chapitre.
- **Attention** : qualité d'exécution (voix, lisibilité, structure).
- **Extension** : impact sur le lecteur et le monde (tests de réception, heatmap d'ennui).

## 3. Protocole Syntonie‑12

1. **SID – Sovereign Intention Document** : créer `intent.md`, relu avant chaque sprint.
2. **Ledger de continuité** : maintenir `continuity.md` (entités, dettes, règles du monde) et lancer un *coherence diff* à chaque PR.
3. **Budget de motifs** : limiter les motifs actifs à sept. Toute nouvelle entrée doit remplacer ou fusionner un motif existant.
4. **Balises D·F·C** : chaque fichier de chapitre commence par :
   ```markdown
   <!-- desire: ... -->
   <!-- fear: ... -->
   <!-- cost: ... -->
   ```
   Le script `python3 scripts/syntony_guard.py` bloque la CI si l'une des balises manque.
5. **Alternance Poète/Ingénieur** : calendrier 2:1. Jours Poète = création brute sans outils. Jours Ingénieur = refactor, build, PR.
6. **Nœuds Médicis** : aux chapitres 3, 9, 15 et 22, injecter un croisement disciplinaire (science, art, philosophie, artisanat). Documenter le choix dans la PR.
7. **Pré-mortem / Red Team** : avant chaque acte, rédiger le scénario d'échec et les contre-mesures. Merge bloqué tant que le binôme n'est pas produit.
8. **SemCI** : évaluer chaque chapitre (cohérence, tension, lisibilité, voix). Seuil de merge = 80/100.
9. **Télémétrie d'énergie** : loguer dans `logs/energie.csv` l'énergie ressentie (1–5) à chaque session.
10. **Gel par acte** : tagger `vActeI`, `vActeII`, `vActeIII`. Aucun retour arrière sans incohérence critique.
11. **Boucle lecteur** : lecture mensuelle sur liseuse, production d'une heatmap d'ennui et plan d'action associé.
12. **Rituel d'accord** : relire `intent.md` et 10 lignes du chapitre totem avant d'ouvrir un prompt.

## 4. Thermostat du chaos \(K\)

- \(K < 0,35\) : excès de structure → déclencher une séance Poète + un nœud Médicis.
- \(0,35 \leq K \leq 0,65\) : bord du chaos, zone idéale.
- \(K > 0,65\) : excès de chaos → doubler les journées Ingénieur, lancer `make semci` et réduire les expérimentations.

Le thermostat se mesure par :
\[
K = \frac{C_{exp}}{C_{exp} + C_{struct}}
\]
où `C_exp` = temps passé en création brute durant le sprint, `C_struct` = temps passé en structuration.

## 5. Métriques de vérité

| Indicateur | Calcul | Plage cible |
|------------|--------|-------------|
| **FD – Foreshadowing Density** | Indices narratifs / 10 000 mots | 6 – 10 |
| **CL – Climax Latency** | Mots entre promesse et pay-off | décroissant par acte |
| **MRR – Motif Reuse Rate** | Occurrences motif dominant / total motifs | 0,5 – 0,7 |
| **VD – Voice Drift** | Distance lexicale au chapitre totem | ≤ 15 % |

## 6. Cadence fractale

- **Micro (scène)** : action, retournement, coût immédiat.
- **Meso (chapitre)** : bascule claire de statut (relation, pouvoir, croyance).
- **Macro (acte)** : transformation irréversible du protagoniste.

La validation d'un chapitre requiert une synthèse micro/meso/macro en trois phrases maximum, jointe à la PR.

## 7. Kit opérationnel

- `templates/intent-template.md` : serment initial et boussole émotionnelle.
- `templates/syntonie-config.yaml` : configuration de la Syntonie (thermostat, motifs, seuils SemCI).
- `scripts/syntony_guard.py` : vérifie les balises D·F·C et la conformité au budget de motifs.
- `logs/energie.csv` : journal des sessions (énergie, observations, décisions).

> *« La structure garde le feu ; le feu transfigure la structure. »*
