# Data Directory

This directory contains JSON files with compartmental ODE models extracted from scientific literature. Each file corresponds to one article and follows the import format defined in `import_example.json`.

## File Naming Convention

`{year}_{topic}_model.json`

- **year**: Publication year of the article
- **topic**: Descriptive topic name (snake_case)
- **model**: Fixed suffix indicating model data

---

## Generated Model JSONs (from PDF articles)

| File | Article | Authors | Year | Models Included |
| ------ | --------- | --------- | ------ | ----------------- |
| `2024_marriage_divorce_model.json` | Dynamics of a Social Model for Marriage and Divorce Relationship | Helal, M. M., et al. | 2024 | Marriage/divorce social model (3 compartments: single males, single females, married) with fear effect |
| `2006_feynman_diagrams_spread.json` | The power of a good idea: Quantitative modeling of the spread of ideas from epidemiological models | Bettencourt, L.M.A., Cintron-Arias, A., Kaiser, D.I., Castillo-Chavez, C. | 2006 | SIR, SEI (incubation), SEIZ (skeptics) for Feynman diagram adoption |
| `2009_zombie_attack_models.json` | When Zombies Attack!: Mathematical Modelling of an Outbreak of Zombie Infection | Munz, P., Hudea, I., Imad, J., Smith?, R.J. | 2009 | Basic SZR, SIZR (latent), SIZRQ (quarantine), SIZR (cure), impulsive eradication |
| `2013_vampire_human_models.json` | Mathematical Models of Interactions between Species: Peaceful Co-existence of Vampires and Humans | Strielkowski, W., Lisin, E., Welkins, E. | 2013 | Stoker-King, Rice, Harris-Meyer-Kostova (3 vampire-human interaction scenarios) |
| `2014_spatial_zombie_model.json` | The Zombie Swarm | Sander, E., Topaz, C.M. | 2014 | Spatial zombie PDE (swarm), spatial zombie with cure |
| `2014_facebook_irSIR_model.json` | Epidemiological modeling of online social network dynamics | Cannarella, J., Spechler, J.A. | 2014 | SIR, irSIR (infectious recovery) for Facebook adoption |
| `2015_illicit_drug_use_model.json` | Modeling Illicit Drug Use Dynamics and Its Optimal Control Analysis | Mushayabasa, S., Tapedzesa, G. | 2015 | Drug use SIR-type (5 compartments), optimal control extension |
| `2013_drug_user_dynamics_model.json` | Drug user dynamics: A compartmental model of drug users for scenario analyses | Santoro, M., Triolo, L., Rossi, C. | 2013 | Italian 6-compartment drug model (cannabis/other × occasional/regular/intensive + health care) |
| `2002_depression_young_women_model.json` | A Mathematical Model of Depression in Young Women as a Function of the Pressure to be Beautiful | Dillon, J.L., Baeza, N., Ruales, M.C., Song, B. | 2002 | Depression model (4 compartments: high/low vulnerability, depressed, treatment) |

---

## Reference Files (Read-Only)

| File | Description |
|------|-------------|
| `import_example.json` | Example import format from the repository (shows thermal cooling, CSTR reactor, SIR epidemiological models) |

---

## Generation Process

These JSON files were **generated using the skill `.opencode/skill/pdf_to_ode_json.md`** following its exact procedure:

1. **Extract text** from PDF articles using `pdftotext "article.pdf" -`
2. **Identify model components** from the extracted text:
   - Compartments (state variables and their ODEs)
   - Parameters (symbols, definitions, linearity)
   - Article metadata (title, authors, date, journal)
   - Data sources (simulations, empirical data, case studies)
3. **Map to JSON schema** following the skill's output format:
   - One JSON file per article named `{year}_{topic}_model.json`
   - Structure matching `import_example.json` exactly
   - All `name` fields in snake_case
   - Compartment expressions copied verbatim from paper
   - Parameter meanings copied verbatim from paper tables
4. **Validate JSON structure only** (syntax, required fields, naming conventions) — no database import performed

The skill enforces these guardrails:

- Never invent parameters not in the paper
- Never modify ODE expressions — copy exactly
- Never guess meanings — use paper's definitions
- Never combine models from different papers in one JSON

## Usage

To import into the encyclopedia database:

```bash
python src/scripts/import_from_json.py data/2024_marriage_divorce_model.json
```

Each file contains a `models` array with one or more model objects. All data is sourced exclusively from the corresponding articles — no external information.
