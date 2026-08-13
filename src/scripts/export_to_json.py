# src/scripts/export_to_json.py
import sys
import json
import logging
from pathlib import Path
from datetime import date, datetime

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from services import ServiceHandler
from database import init_db, db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JsonExporter:
    def __init__(self):
        self.service = ServiceHandler()
    
    def export_all_models(self, output_path: str):
        """Export all models to a JSON file."""
        models = self.service.model.to_list()
        
        if not models:
            logger.warning("No models found in database")
            return False
        
        result = {
            "exported_at": datetime.now().isoformat(),
            "total_models": len(models),
            "models": []
        }
        
        for model in models:
            try:
                model_info = self.service.model.get_all(model.name)
                result["models"].append(self._model_to_dict(model_info))
                print(self._model_to_dict(model_info))
                logger.info(f"✅ Exported model: {model_info.name}")
            except Exception as e:
                logger.error(f"❌ Error exporting {model.name}: {e}")
        
        #Save file
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📊 Export complete: {len(result['models'])} models exported to {output_path}")
        return True
    
    def _model_to_dict(self, model_info) -> dict:
        """Converts a ModelInfoDto to a serializable dictionary."""
        return {
            "name": model_info.name,
            "situation": {
                "name": model_info.situation.name,
                "description": model_info.situation.description
            } if model_info.situation else None,
            "article": {
                "name": model_info.article.name,
                "author": model_info.article.author,
                "date": self._format_date(model_info.article.date)
            } if model_info.article else None,
            "data": {
                "name": model_info.data.name,
                "place": model_info.data.place,
                "date": self._format_date(model_info.data.date)
            } if model_info.data else None,
            "compartments": [
                {
                    "name": c.name,
                    "expression": c.expression
                }
                for c in model_info.compartments
            ],
            "params": [
                {
                    "name": p.name,
                    "linear": p.linear,
                    "symbol": p.symbol,
                    "meaning": p.meaning
                }
                for p in model_info.params
            ]
        }
    
    def _format_date(self, date_value) -> str:
        """Convert a date to an ISO string (YYYY-MM-DD)."""
        if date_value is None:
            return None
        if isinstance(date_value, (date, datetime)):
            return date_value.isoformat()
        return str(date_value)


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/scripts/export_to_json.py <output_path>")
        print("\nExample:")
        print("  python src/scripts/export_to_json.py data/export.json")
        sys.exit(1)
    
    output_path = sys.argv[1]

    #Add extension if not given
    path = Path(output_path)
    if path.suffix == '':
        output_path = str(path.with_suffix('.json'))
    
    init_db()
    
    exporter = JsonExporter()
    success = exporter.export_all_models(output_path)
    
    db.close()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()