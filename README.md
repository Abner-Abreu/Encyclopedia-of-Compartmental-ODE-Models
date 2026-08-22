# Encyclopedia of Compartmental ODE Models

Desktop application for managing compartmental ODE models with their parameters, compartments, and associated scientific literature.

## Stack

- Python 3.14
- SQLite + Peewee ORM
- Tkinter GUI

## Requirements

- Python 3.14 or higher
- pip

## Installation
```bash
git clone https://github.com/Abner-Abreu/Encyclopedia-of-Compartmental-ODE-Models.git
```
```bash
cd Encyclopedia-of-Compartmental-ODE-Models
```
```bash
pip install -r requirements.txt
```
> [!NOTE]
> You can skip installing ```requirements.txt``` if you have already installed:
> - ```peewee 4.1.2 or higher```
> - ```platformdirs 4.11.0 or higher```

```bash
python main.py
```

## Database Location

The database file (`encyclopedia.db`) is automatically created in your **Documents folder** inside a directory named `EncyclopediaODEModels`:

- **Windows**: `C:\Users\<YourUser>\Documents\EncyclopediaODEModels\`
- **macOS**: `/Users/<YourUser>/Documents/EncyclopediaODEModels/`
- **Linux**: `/home/<YourUser>/Documents/EncyclopediaODEModels/`

> [!NOTE]
> The database is created automatically on first run. No manual setup is required.

## Scripts de importación y exportación

### Importar modelos desde JSON

```bash
python src/scripts/import_from_json.py <input_path>
```

Ejemplo:
```bash
python src/scripts/import_from_json.py data/import.json
```
#### JSON Structure for Import

The JSON file must contain a "models" array with one or more model objects:

```json
{
  "models": [
    {
      "name": "MODEL_NAME",
      "situation": {
        "name": "SIT_NAME",
        "description": "Situation description"
      },
      "article": {
        "name": "ART_NAME",
        "author": "Author Name",
        "date": "YYYY-MM-DD"
      },
      "data": {
        "name": "DAT_NAME",
        "place": "Location",
        "date": "YYYY-MM-DD"
      },
      "compartments": [
        {
          "name": "COMP_NAME",
          "expression": "Mathematical expression"
        }
      ],
      "params": [
        {
          "name": "PARAM_NAME",
          "linear": true,
          "symbol": "\\alpha",
          "meaning": "Parameter meaning"
        }
      ]
    }
  ]
}
```

Fields:
- name (required): Unique model identifier
- situation (required): Associated situation
- article (required): Associated article
- data (optional): Experimental data entry
- compartments (required): List of compartments with expressions
- params (required): List of parameters with linearity, symbol, and meaning

Date format: YYYY-MM-DD (ISO 8601)

> [!NOTE]
> An example of JSON ready to import can be found in [`data/import_example.json`](data/import_example.json)

### Exportar modelos a JSON

```bash
python src/scripts/export_to_json.py <output_path>
```
Ejemplo:

```bash
python src/scripts/export_to_json.py data/export.json
```
>[!NOTE]
> The output format is similar to the input format, adding export
> datetime and number of models

## Usage

### Adding a New Model

1. Click **"Add Model"** in the main view
2. Enter the number of compartments and parameters
3. Click **"Continue"**
4. Fill in the complete model data in the dialog:
  - Model name
  - Situation details
  - Article information
  - Compartment details (name and expression)
  - Parameter details (name, symbol, meaning, linearity)
  - Optional data entry
5. Click **"Save"**

### Searching Models

- Use the **"Search"** panel to filter models by:
  - Model Name
  - Parameter
  - Compartment
  - Situation
  - Article
- Check "Only models with all linear parameters"
- Click **"Search"** to apply filters
- Click **"Clear"** to reset text fields
- Click **"Show All"** to reset all filters

### Managing Models

- **Right-click** a row for context menu options:
  - **Delete**: Remove the model and all its associations
  - **View Details**: Display complete model information

## Logging

Logs are output to the console with INFO, WARNING, and ERROR levels.
