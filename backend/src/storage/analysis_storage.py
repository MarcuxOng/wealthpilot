import shelve
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import json

class AnalysisStorage:
    def __init__(self, storage_dir: str = "app/records"):
        self.storage_dir = storage_dir
        self.db_path = os.path.join(storage_dir, "ai_analysis_db")
        os.makedirs(storage_dir, exist_ok=True)
    
    def store_analysis(self, client_id: str, analysis_data: Dict[str, Any]) -> bool:
        try:
            analysis_record = {
                "client_id": client_id,
                "analysis_data": analysis_data,
                "timestamp": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            with shelve.open(self.db_path) as db:
                if client_id in db:
                    existing_data = db[client_id]
                    if isinstance(existing_data, list):
                        existing_data.append(analysis_record)
                        db[client_id] = existing_data
                    else:
                        db[client_id] = [existing_data, analysis_record]
                else:
                    db[client_id] = [analysis_record]
                
            return True
            
        except Exception as e:
            print(f"Error storing analysis for client {client_id}: {str(e)}")
            return False
    
    def get_analysis(self, client_id: str) -> Optional[Dict[str, Any]]:
        try:
            with shelve.open(self.db_path) as db:
                if client_id in db:
                    data = db[client_id]
                    if isinstance(data, list):
                        return data[-1] if data else None
                    else:
                        return data
                return None
                
        except Exception as e:
            print(f"Error retrieving analysis for client {client_id}: {str(e)}")
            return None
    
    def get_all_analyses(self) -> Dict[str, Any]:
        try:
            with shelve.open(self.db_path) as db:
                return dict(db)
                
        except Exception as e:
            print(f"Error retrieving all analyses: {str(e)}")
            return {}

    def get_client_analyses(self, client_id: str) -> List[Dict[str, Any]]:
        try:
            with shelve.open(self.db_path) as db:
                if client_id in db:
                    data = db[client_id]
                    if isinstance(data, list):
                        return sorted(data, key=lambda x: x.get('timestamp', ''))
                    else:
                        return [data]
                return []
                
        except Exception as e:
            print(f"Error retrieving analyses for client {client_id}: {str(e)}")
            return []
    
    def delete_analysis(self, client_id: str) -> bool:
        try:
            with shelve.open(self.db_path) as db:
                if client_id in db:
                    del db[client_id]
                    return True
                return False
                
        except Exception as e:
            print(f"Error deleting analysis for client {client_id}: {str(e)}")
            return False

    def delete_specific_analysis(self, client_id: str, timestamp: str) -> bool:
        try:
            with shelve.open(self.db_path) as db:
                if client_id in db:
                    data = db[client_id]
                    if isinstance(data, list):
                        filtered_data = [analysis for analysis in data if analysis.get('timestamp') != timestamp]
                        if len(filtered_data) < len(data):
                            if filtered_data:
                                db[client_id] = filtered_data
                            else:
                                del db[client_id]
                            return True
                    else:
                        if data.get('timestamp') == timestamp:
                            del db[client_id]
                            return True
                return False
                
        except Exception as e:
            print(f"Error deleting specific analysis for client {client_id}: {str(e)}")
            return False
    
    def get_analysis_count(self) -> int:
        try:
            with shelve.open(self.db_path) as db:
                total_count = 0
                for client_id, data in db.items():
                    if isinstance(data, list):
                        total_count += len(data)
                    else:
                        total_count += 1
                return total_count
                
        except Exception as e:
            print(f"Error getting analysis count: {str(e)}")
            return 0
    
    def get_analyses_by_date_range(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        try:
            with shelve.open(self.db_path) as db:
                filtered_analyses = {}
                
                for client_id, analysis_record in db.items():
                    analysis_timestamp = datetime.fromisoformat(analysis_record["timestamp"])
                    
                    if start_date <= analysis_timestamp <= end_date:
                        filtered_analyses[client_id] = analysis_record
                
                return filtered_analyses
                
        except Exception as e:
            print(f"Error getting analyses by date range: {str(e)}")
            return {}

analysis_storage = AnalysisStorage()
