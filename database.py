"""Database connection utilities for DuckDB vector database."""

import duckdb
from typing import Optional, Dict, Any
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
        self._connection: Optional[duckdb.DuckDBPyConnection] = None
    
    def connect(self) -> duckdb.DuckDBPyConnection:
        """Establish connection to DuckDB database with validation.
        
        Returns:
            duckdb.DuckDBPyConnection: An active DuckDB connection object.
            
        Raises:
            FileNotFoundError: If the database file does not exist at the specified path.
        """
        if self._connection:
            try:
                # Lightweight check if connection is alive
                self._connection.execute("SELECT 1")
                return self._connection
            except Exception:
                logger.warning("Connection lost, reconnecting...")
                self._connection = None

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found at: {self.db_path}")
            
        logger.info(f"Connecting to database: {self.db_path}")
        self._connection = duckdb.connect(self.db_path, read_only=True)
        return self._connection
    
    def close(self):
        """Close the active database connection.
        
        Safely closes the connection if it exists and resets the internal state.
        Should be called when the application is shutting down or the connection
        is no longer needed.
        """
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def test_connection(self) -> Dict[str, Any]:
        """Verify database accessibility and connection health.
        
        Attempts to establish a connection to the database to ensure it is
        accessible and functioning correctly.
        
        Returns:
            Dict[str, Any]: A dictionary containing the status of the connection test.
                Format: {"status": "success"|"error", "db_path": str, "error": str (optional)}
        """
        try:
            self.connect()
            return {"status": "success", "db_path": self.db_path}
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {"status": "error", "error": str(e)}

# Global instance for basic connectivity checks
db_manager = DatabaseManager()