"""Database connection utilities for DuckDB vector database."""

import duckdb
from typing import List, Dict, Any
import os
from config import settings
from utils.logger import logger


class DatabaseManager:
    """Manages DuckDB connection and basic operations."""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager.
        
        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = db_path or settings.database_path
        self._connection = None
    
    def connect(self) -> duckdb.DuckDBPyConnection:
        """Establish connection to DuckDB database with validation.
        
        Returns:
            DuckDB connection object
        """
        if not os.path.exists(self.db_path):
            logger.error(f"Database file not found: {self.db_path}")
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        
        # Check if connection exists and is still valid
        if self._connection is not None:
            try:
                # Test connection validity with a simple query
                result = self._connection.execute("SELECT 1").fetchone()
                if result != (1,):
                    raise Exception("Database connection validation failed: unexpected result")
            except Exception as e:
                logger.warning(f"Existing connection failed validation, reconnecting: {e}")
                self._connection = None
        
        if self._connection is None:
            logger.info(f"Connecting to database: {self.db_path}")
            self._connection = duckdb.connect(self.db_path, read_only=True)
        
        return self._connection
    
    def execute_query(self, query: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of dictionaries with query results
        """
        # TODO: Add vector similarity search methods for querying embeddings
        # TODO: Implement methods to retrieve chunks based on similarity
        
        conn = self.connect()
        
        try:
            if params:
                result = conn.execute(query, params).fetchall()
            else:
                result = conn.execute(query).fetchall()
            
            # Get column names
            columns = [desc[0] for desc in conn.description]
            
            # Convert to list of dictionaries
            result_dicts = [dict(zip(columns, row)) for row in result]
            
            return result_dicts
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def test_connection(self) -> Dict[str, Any]:
        """Test database connection for RAG service initialization.
        
        Returns:
            Dictionary with connection test results
        """
        # TODO: Add schema validation for existing vector tables
        # TODO: Verify embedding columns exist and data is available
        
        try:
            self.connect()
            
            result = {
                "status": "success",
                "db_path": self.db_path
            }
            
            logger.info("Database connection test successful")
            return result
            
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }


# Global database manager instance
db_manager = DatabaseManager()