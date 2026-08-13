import json
import logging
import sys
from pathlib import Path
from datetime import date

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from services import ServiceHandler
from dtos import (
    ModelInfoDto,
    CompartmentDto,
    ParamInfoDto,
    SituationDto,
    ArticleDto,
    DataDto
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JsonImporter:
    def __init__(self):
        self.service = ServiceHandler()
    
    def import_from_file(self, filepath: str):
        """Imports data from JSON file"""
        path = Path(filepath)
        if not path.exists():
            logger.error(f"File not found: {filepath}")
            return False
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return self.import_from_dict(data)
    
    def import_from_dict(self, data: dict):
        """Imports data from dictionary."""
        if 'models' not in data:
            logger.error("JSON must contain 'models' key")
            return False
        
        success_count = 0
        error_count = 0
        
        for model_data in data['models']:
            try:
                model_info = self._parse_model_data(model_data)
                if self.service.create_complete(model_info):
                    success_count += 1
                    logger.info(f"✅ Imported model: {model_info.name}")
                else:
                    error_count += 1
                    logger.error(f"❌ Failed to import model: {model_data.get('name', 'Unknown')}")
            except Exception as e:
                error_count += 1
                logger.error(f"❌ Error importing model: {e}")
        
        logger.info(f"📊 Import complete: {success_count} imported, {error_count} errors")
        return error_count == 0
    
    def _parse_model_data(self, data: dict) -> ModelInfoDto:
        """Transfer info from a Dictionary to a ModelInfoDto."""
        name = data.get('name', '').strip()
        if not name:
            raise ValueError("Model name is required")
        
        # Parse situation
        situation_data = data.get('situation', {})
        situation = SituationDto(
            name=situation_data.get('name', 'SIT_DEFAULT'),
            description=situation_data.get('description', '')
        )
        
        # Parse article
        article_data = data.get('article', {})
        article = ArticleDto(
            name=article_data.get('name', 'ART_DEFAULT'),
            author=article_data.get('author', 'Unknown'),
            date=self._parse_date(article_data.get('date', '2024-01-01'))
        )
        
        # Parse data (optional)
        data_entry = None
        if 'data' in data and data['data']:
            data_data = data['data']
            data_entry = DataDto(
                name=data_data.get('name', 'DAT_DEFAULT'),
                place=data_data.get('place', 'Unknown'),
                date=self._parse_date(data_data.get('date', ''))
            )
        
        # Parse compartments
        compartments = []
        for comp_data in data.get('compartments', []):
            compartments.append(CompartmentDto(
                name=comp_data.get('name', '').strip(),
                expression=comp_data.get('expression', '').strip()
            ))
        
        # Parse parameters
        params = []
        for param_data in data.get('params', []):
            params.append(ParamInfoDto(
                name=param_data.get('name', '').strip(),
                linear=param_data.get('linear', False),
                symbol=param_data.get('symbol', '').strip(),
                meaning=param_data.get('meaning', '').strip()
            ))
        
        return ModelInfoDto(
            name=name,
            compartments=compartments,
            params=params,
            situation=situation,
            article=article,
            data=data_entry
        )
    
    def _parse_date(self, date_str: str) -> date:
        """Convert string to date. If no possible use today date."""
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            logger.warning(f"Invalid date format: {date_str}, using today")
            return date.today()


def main():  
    
    import sys

    if len(sys.argv) < 2:
        print("Usage: python import_from_json.py <path_to_json>")
        sys.exit(1)
    
    from database import init_db

    init_db()

    filepath = sys.argv[1]
    importer = JsonImporter()
    success = importer.import_from_file(filepath)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()