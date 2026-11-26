# Skill: PDF to ODE Model JSON Converter

## Purpose

Convert scientific PDF articles about compartmental ODE models into structured JSON files compatible with the Encyclopedia of Compartmental ODE Models database import format.

## When to Use

- When you have PDF articles containing compartmental ODE models
- When you need to extract mathematical models from literature for database import
- When preparing data for the `import_from_json.py` script

## Input Requirements

- One or more PDF files containing compartmental ODE models
- Access to `pdftotext` (Poppler) for text extraction
- The target repository with `data/import_example.json` as reference format

## Output Format

Each article produces one JSON file in `data/` named `{year}_{topic}_model.json` containing:

```json
{
  "models": [
    {
      "name": "snake_case_model_name",
      "situation": {
        "name": "snake_case_situation_name",
        "description": "Description of the modeling situation/context"
      },
      "article": {
        "name": "Full Article Title",
        "author": "Author names as in paper",
        "date": "YYYY-MM-DD"
      },
      "data": {
        "name": "snake_case_data_name",
        "place": "Location/context of data",
        "date": "YYYY-MM-DD",
        "source": "DOI, journal, or URL"
      },
      "compartments": [
        {
          "name": "snake_case_compartment_name",
          "expression": "dX/dt = ... (exact ODE from paper)"
        }
      ],
      "params": [
        {
          "name": "snake_case_param_name",
          "linear": true|false,
          "symbol": "Greek letter or symbol from paper",
          "meaning": "Exact definition from paper"
        }
      ]
    }
  ]
}
```

## Process

### 1. Extract Text from PDFs

```bash
pdftotext "path/to/article.pdf" -
```

- Use stdout (`-`) to capture text directly
- For multi-page papers, the full text will be concatenated

### 2. Identify Model Components

Search the extracted text for:

- **Compartments**: State variables (S, I, R, M, F, G, etc.) and their differential equations
- **Parameters**: Greek letters (β, γ, α, μ, etc.) with definitions in tables or text
- **Model name**: From title or section headers
- **Article metadata**: Title, authors, publication date, journal
- **Data source**: Any empirical data, simulations, or case studies mentioned

### 3. Map to JSON Structure

#### Compartments

- Use exact ODE expressions from the paper
- Preserve original notation (dM/dt, dS/dt, etc.)
- Include all terms exactly as written
- Name compartments descriptively in snake_case

#### Parameters

- **linear: true** for parameters appearing linearly in ODEs (e.g., μ, γ, δ)
- **linear: false** for parameters in nonlinear terms (e.g., β in βSI, α in αMF/(1+nG))
- Use the exact symbol from the paper (β, gamma, alpha1, etc.)
- Copy parameter meanings verbatim from paper tables/definitions

#### Article & Data

- Date: Use publication year with `-01-01` if only year known
- Source: Include DOI, journal reference, or arXiv ID
- Data: Note if from simulations, empirical data, or case studies

### 4. Handle Multiple Models per Paper

If a paper presents multiple model variants (e.g., SIR, SEI, SEIZ):

- Create separate model objects in the `models` array
- Use descriptive names distinguishing variants
- Share article/data metadata where appropriate

### 5. Validate JSON Structure Only

- Ensure all required fields present (`models`, `name`, `situation`, `article`, `compartments`, `params`)
- Check that compartment expressions are valid ODEs from the paper
- Verify parameter symbols match those used in expressions
- Confirm snake_case naming convention for all `name` fields
- Verify JSON is syntactically valid

## Rules (Guardrails)

- **Never invent parameters** not in the paper
- **Never modify ODE expressions** - copy exactly
- **Never guess meanings** - use paper's definitions
- **Never combine models** from different papers in one JSON
- **Always use snake_case** for all name fields
- **Always include all compartments** from the model
- **Always include all parameters** referenced in ODEs

## Example Workflow

```bash
# 1. Extract text
pdftotext "paper.pdf" - > paper_text.txt

# 2. Analyze text for models, compartments, parameters
# 3. Create JSON following format above
# 4. Save to data/{year}_{topic}_model.json
# 5. Validate JSON syntax (e.g., python -m json.tool file.json)
```

## Common Patterns to Recognize

| Pattern | JSON Mapping |
| --------- | ------------- |
| `dS/dt = -βSI/N` | compartment "susceptible", expression "dS/dt = -β*S*I/N" |
| `β = transmission rate` | param "transmission_rate", symbol "β", linear: false |
| `μ = death rate` | param "death_rate", symbol "μ", linear: true |
| Table with parameter definitions | Extract all rows to params array |
| Multiple model versions (Sec 2, 3, 4) | Separate model objects in models array |
| "Basic reproductive number R₀ = ..." | Include as param with linear: false |

## Error Handling

- If PDF extraction fails: note which file failed, continue with others
- If model unclear: create JSON with what's identifiable, mark gaps in description
- If parameters missing meanings: use "As defined in paper" as placeholder
- If ODE uses undefined symbols: include as-is, note in description

## Quality Checklist

- [ ] All compartments from paper included
- [ ] All parameters in ODEs listed in params
- [ ] Linear/nonlinear correctly classified
- [ ] Symbols match paper exactly
- [ ] Meanings copied from paper tables
- [ ] Article metadata complete
- [ ] Data source documented
- [ ] File named correctly (`{year}_{topic}_model.json`)
- [ ] JSON is syntactically valid
