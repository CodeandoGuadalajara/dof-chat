"""Database connection utilities for DuckDB vector database."""

import duckdb
import threading
from typing import Dict, Any
import os
from config import settings
from utils.logger import logger


class DatabaseManager:
    """Manages DuckDB connections with thread-local storage for concurrency.
    
    Each thread gets its own connection to avoid race conditions since
    DuckDB connections are not thread-safe for concurrent query execution.
    """
    
    def __init__(self, db_path: str = None):
        """Initialize database manager.
        
        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = db_path or settings.database_path
        self._thread_local = threading.local()  # Each thread gets own connection
    
    def connect(self, read_only: bool = True) -> duckdb.DuckDBPyConnection:
        """Get or create thread-local connection for current thread.
        
        Args:
            read_only: Whether to open in read-only mode (default: True).
        
        Returns:
            duckdb.DuckDBPyConnection: Connection object for this thread.
            
        Raises:
            FileNotFoundError: If database file not found.
        """
        # Check if current thread already has a connection
        if getattr(self._thread_local, 'connection', None):
            return self._thread_local.connection

        # Create new connection for this thread
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found at: {self.db_path}")
            
        logger.info(f"[Thread {threading.current_thread().name}] Connecting to database: {self.db_path}")
        self._thread_local.connection = duckdb.connect(self.db_path, read_only=read_only)
        return self._thread_local.connection
    
    def reconnect(self, read_only: bool = True) -> duckdb.DuckDBPyConnection:
        """Force new connection for current thread (closes existing, creates new).
        
        Used when a query fails due to stale connection.
        
        Args:
            read_only: Whether to open in read-only mode (default: True).
            
        Returns:
            duckdb.DuckDBPyConnection: New connection object for this thread.
        """
        logger.warning(f"[Thread {threading.current_thread().name}] Forcing database reconnection...")
        
        # Close existing connection for this thread
        if getattr(self._thread_local, 'connection', None):
            self._thread_local.connection.close()
            self._thread_local.connection = None
        
        # Create new connection
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found at: {self.db_path}")
            
        logger.info(f"[Thread {threading.current_thread().name}] Reconnecting to database: {self.db_path}")
        self._thread_local.connection = duckdb.connect(self.db_path, read_only=read_only)
        return self._thread_local.connection
    
    def close(self):
        """Close connection for current thread (safe if not connected)."""
        if getattr(self._thread_local, 'connection', None):
            self._thread_local.connection.close()
            self._thread_local.connection = None
    
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
        except duckdb.Error as e:
            logger.error("Connection test failed (duckdb error)", exc_info=True)
            return {"status": "error", "error": str(e)}
        except Exception as e:
            logger.error("Connection test failed (unexpected error)", exc_info=True)
            return {"status": "error", "error": str(e)}

# Global instance for basic connectivity checks
db_manager = DatabaseManager()