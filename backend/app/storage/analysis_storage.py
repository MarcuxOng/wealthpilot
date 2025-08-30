import shelve
import os
from datetime import datetime
from typing import Dict, Any, Optional
import json

class AnalysisStorage:
    """Storage class for AI analysis data using Python shelve"""
    
    def __init__(self, storage_dir: str = "app/records"):
        """
        Initialize the storage with the specified directory
        
        Args:
            storage_dir: Directory where the shelve database will be stored
        """
        self.storage_dir = storage_dir
        self.db_path = os.path.join(storage_dir, "ai_analysis_db")
        
        # Ensure the storage directory exists
        os.makedirs(storage_dir, exist_ok=True)
    
    def store_analysis(self, client_id: str, analysis_data: Dict[str, Any]) -> bool:
        """
        Store AI analysis data for a client
        
        Args:
            client_id: The client identifier
            analysis_data: The AI analysis data to store
            
        Returns:
            bool: True if storage was successful, False otherwise
        """
        try:
            # Add timestamp to the analysis data
            analysis_record = {
                "client_id": client_id,
                "analysis_data": analysis_data,
                "timestamp": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat()
            }
            
            with shelve.open(self.db_path) as db:
                # Use client_id as the key
                db[client_id] = analysis_record
                
            return True
            
        except Exception as e:
            print(f"Error storing analysis for client {client_id}: {str(e)}")
            return False
    
    def get_analysis(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve AI analysis data for a client
        
        Args:
            client_id: The client identifier
            
        Returns:
            Optional[Dict]: The analysis data if found, None otherwise
        """
        try:
            with shelve.open(self.db_path) as db:
                if client_id in db:
                    return db[client_id]
                return None
                
        except Exception as e:
            print(f"Error retrieving analysis for client {client_id}: {str(e)}")
            return None
    
    def get_all_analyses(self) -> Dict[str, Any]:
        """
        Retrieve all stored AI analyses
        
        Returns:
            Dict: All stored analyses with client_id as keys
        """
        try:
            with shelve.open(self.db_path) as db:
                return dict(db)
                
        except Exception as e:
            print(f"Error retrieving all analyses: {str(e)}")
            return {}
    
    def delete_analysis(self, client_id: str) -> bool:
        """
        Delete AI analysis data for a client
        
        Args:
            client_id: The client identifier
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            with shelve.open(self.db_path) as db:
                if client_id in db:
                    del db[client_id]
                    return True
                return False
                
        except Exception as e:
            print(f"Error deleting analysis for client {client_id}: {str(e)}")
            return False
    
    def get_analysis_count(self) -> int:
        """
        Get the total number of stored analyses
        
        Returns:
            int: Number of stored analyses
        """
        try:
            with shelve.open(self.db_path) as db:
                return len(db)
                
        except Exception as e:
            print(f"Error getting analysis count: {str(e)}")
            return 0
    
    def get_analyses_by_date_range(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Get analyses within a specific date range
        
        Args:
            start_date: Start date for the range
            end_date: End date for the range
            
        Returns:
            Dict: Analyses within the specified date range
        """
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

# Create a global instance for easy access
analysis_storage = AnalysisStorage()
