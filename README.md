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

The database file (`encyclopedia.db`) is automatically created in your **Documents folder** inside a directory named `Encyclopedia Of Compartmental ODE Models`:

- **Windows**: `C:\Users\<YourUser>\Documents\Encyclopedia Of Compartmental ODE Models\`
- **macOS**: `/Users/<YourUser>/Documents/Encyclopedia Of Compartmental ODE Models/`
- **Linux**: `/home/<YourUser>/Documents/Encyclopedia Of Compartmental ODE Models/`

> [!NOTE]
> The database is created automatically on first run. No manual setup is required.

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
