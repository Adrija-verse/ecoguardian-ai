"""
Session Manager - EcoGuardian AI
Manages user sessions and integrates with MemoryBank for persistent storage
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import json

# Configure logging
logger = logging.getLogger(__name__)

# Import the global logger
from observability.logger import eco_logger


class Session:
    """Represents a user session"""
    
    def __init__(self, session_id: str, initial_state: Dict[str, Any] = None):
        self.session_id = session_id
        self.state = initial_state or {}
        self.messages = []
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
    
    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Add a message to the session"""
        self.messages.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })
        self.last_accessed = datetime.now()
    
    def update_state(self, key: str, value: Any):
        """Update session state"""
        self.state[key] = value
        self.last_accessed = datetime.now()
    
    def get_context(self, max_messages: int = 10) -> List[Dict]:
        """Get recent messages for context"""
        return self.messages[-max_messages:]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        return {
            "session_id": self.session_id,
            "state": self.state,
            "messages": self.messages,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat()
        }


class InMemorySessionService:
    """
    Session service with in-memory storage
    Implements session management with Memory Bank integration
    """
    
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        eco_logger.logger.info("InMemorySessionService initialized")
    
    def create_session(self, session_id: str, initial_state: Dict[str, Any] = None) -> Session:
        """Create a new session"""
        if session_id in self.sessions:
            logger.info(f"Session {session_id} already exists, returning existing")
            return self.sessions[session_id]
        
        session = Session(session_id, initial_state)
        self.sessions[session_id] = session
        logger.info(f"Created session: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve a session"""
        session = self.sessions.get(session_id)
        if session:
            session.last_accessed = datetime.now()
        return session
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session with new data"""
        session = self.get_session(session_id)
        if not session:
            logger.warning(f"Session {session_id} not found")
            return False
        
        for key, value in data.items():
            session.update_state(key, value)
        
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
    
    def list_sessions(self) -> List[str]:
        """List all active session IDs"""
        return list(self.sessions.keys())
    
    def cleanup_old_sessions(self, hours: int = 24):
        """Remove sessions older than specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        to_remove = []
        
        for session_id, session in self.sessions.items():
            if session.last_accessed < cutoff_time:
                to_remove.append(session_id)
        
        for session_id in to_remove:
            self.delete_session(session_id)
        
        logger.info(f"Cleaned up {len(to_remove)} old sessions")


class MemoryBank:
    """
    Long-term memory storage for EcoGuardian AI agents.
    Provides persistent storage with context compaction and intelligent retrieval.
    """
    
    def __init__(self, max_memory_size: int = 10000, compaction_threshold: float = 0.8):
        """
        Initialize the Memory Bank.
        
        Args:
            max_memory_size: Maximum number of memory entries before compaction
            compaction_threshold: Threshold (0-1) for triggering automatic compaction
        """
        self.max_memory_size = max_memory_size
        self.compaction_threshold = compaction_threshold
        self.memory_store = {}
        self.memory_metadata = {}
        self.context_index = defaultdict(list)
        self.access_counts = defaultdict(int)
        self.compaction_history = []
        
        eco_logger.logger.info("MemoryBank initialized")
    
    def store(self, *args, **kwargs) -> bool:
        # Handle both signatures
        if len(args) == 2:
            # Called as: store(key, value, context=...)
            key, value = args
            category = "default"
            context = kwargs.get('context')
        elif len(args) == 3:
            # Called as: store(category, key, value, context=...)
            category, key, value = args
            context = kwargs.get('context')
        else:
            category = args[0] if len(args) > 0 else "default"
            key = args[1] if len(args) > 1 else ""
            value = args[2] if len(args) > 2 else None
            context = kwargs.get('context')
    
        full_key = f"{category}:{key}"
        """
        Store a memory entry with optional context metadata.
        
        Args:
            category: Category for the memory (e.g., 'city_profiles', 'predictions')
            key: Unique identifier within the category
            value: Data to store
            context: Optional context metadata
            
        Returns:
            True if stored successfully
        """
        full_key = f"{category}:{key}"
        
        try:
            # Check if compaction is needed
            if len(self.memory_store) >= int(self.max_memory_size * self.compaction_threshold):
                logger.info("Memory threshold reached, triggering compaction")
                self.compact_memory()
            
            # Store the value
            self.memory_store[full_key] = value
            
            # Store metadata
            self.memory_metadata[full_key] = {
                "timestamp": datetime.now().isoformat(),
                "category": category,
                "context": context or {},
                "size": len(json.dumps(value, default=str)),
                "access_count": 0,
                "last_accessed": None
            }
            
            # Index by context
            if context:
                for context_key, context_value in context.items():
                    self.context_index[f"{context_key}:{context_value}"].append(full_key)
            
            logger.info(f"Memory stored: {full_key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store memory {full_key}: {str(e)}")
            return False
    
    def retrieve(self, category: str, key: str) -> Optional[Any]:
        """Retrieve a memory entry"""
        full_key = f"{category}:{key}"
        
        if full_key not in self.memory_store:
            logger.warning(f"Memory not found: {full_key}")
            return None
        
        # Update access metadata
        self.access_counts[full_key] += 1
        if full_key in self.memory_metadata:
            self.memory_metadata[full_key]["access_count"] += 1
            self.memory_metadata[full_key]["last_accessed"] = datetime.now().isoformat()
        
        logger.info(f"Memory retrieved: {full_key}")
        return self.memory_store[full_key]
    
    def search(self, category: str, filter_fn=None) -> List[Dict]:
        """
        Search memory entries in a category.
        
        Args:
            category: Category to search
            filter_fn: Optional filter function (takes value, returns bool)
            
        Returns:
            List of matching entries
        """
        results = []
        
        for key, value in self.memory_store.items():
            if key.startswith(f"{category}:"):
                if filter_fn is None or filter_fn(value):
                    results.append(value)
        
        return results
    
    def delete(self, category: str, key: str) -> bool:
        """Delete a memory entry"""
        full_key = f"{category}:{key}"
        
        if full_key not in self.memory_store:
            return False
        
        del self.memory_store[full_key]
        
        if full_key in self.memory_metadata:
            del self.memory_metadata[full_key]
        
        for index_key, keys in self.context_index.items():
            if full_key in keys:
                keys.remove(full_key)
        
        if full_key in self.access_counts:
            del self.access_counts[full_key]
        
        logger.info(f"Memory deleted: {full_key}")
        return True
    
    def compact_memory(self, target_reduction: float = 0.3):
        """Compact memory by removing least accessed and oldest entries"""
        logger.info(f"Starting memory compaction (target reduction: {target_reduction*100}%)")
        
        current_size = len(self.memory_store)
        if current_size == 0:
            return
        
        target_size = int(current_size * (1 - target_reduction))
        
        # Score entries
        entry_scores = []
        for key in self.memory_store.keys():
            metadata = self.memory_metadata.get(key, {})
            
            access_count = metadata.get("access_count", 0)
            try:
                timestamp = datetime.fromisoformat(metadata.get("timestamp", datetime.now().isoformat()))
                age_days = (datetime.now() - timestamp).days
            except:
                age_days = 0
            
            score = access_count / (age_days + 1)
            entry_scores.append((key, score))
        
        # Sort by score (ascending - lowest first)
        entry_scores.sort(key=lambda x: x[1])
        
        # Remove lowest scoring entries
        entries_to_remove = entry_scores[:current_size - target_size]
        removed_count = 0
        
        for key, score in entries_to_remove:
            category, _, item_key = key.partition(":")
            if self.delete(category, item_key):
                removed_count += 1
        
        # Record compaction
        compaction_event = {
            "timestamp": datetime.now().isoformat(),
            "entries_removed": removed_count,
            "before_size": current_size,
            "after_size": len(self.memory_store),
            "reduction_percent": round((removed_count / current_size) * 100, 2) if current_size > 0 else 0
        }
        self.compaction_history.append(compaction_event)
        
        logger.info(f"Memory compaction completed: {removed_count} entries removed")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory bank statistics"""
        total_size = sum(
            self.memory_metadata.get(key, {}).get("size", 0)
            for key in self.memory_store.keys()
        )
        
        return {
            "total_entries": len(self.memory_store),
            "total_size_bytes": total_size,
            "max_capacity": self.max_memory_size,
            "utilization_percent": round((len(self.memory_store) / self.max_memory_size) * 100, 2) if self.max_memory_size > 0 else 0,
            "context_indices": len(self.context_index),
            "total_accesses": sum(self.access_counts.values()),
            "compaction_events": len(self.compaction_history),
            "most_accessed_entries": self._get_most_accessed(5)
        }
    
    def _get_most_accessed(self, limit: int = 5) -> List[Dict]:
        """Get the most frequently accessed memory entries"""
        sorted_entries = sorted(
            self.access_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                "key": key,
                "access_count": count,
                "metadata": self.memory_metadata.get(key)
            }
            for key, count in sorted_entries[:limit]
        ]
    
    def export_memory(self, filepath: str) -> bool:
        """Export memory bank to a JSON file"""
        try:
            export_data = {
                "memory_store": self.memory_store,
                "memory_metadata": self.memory_metadata,
                "export_timestamp": datetime.now().isoformat(),
                "statistics": self.get_statistics()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Memory exported to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export memory: {str(e)}")
            return False
    
    def import_memory(self, filepath: str, merge: bool = True) -> bool:
        """Import memory bank from a JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if not merge:
                self.memory_store.clear()
                self.memory_metadata.clear()
                self.context_index.clear()
                self.access_counts.clear()
            
            self.memory_store.update(import_data.get("memory_store", {}))
            self.memory_metadata.update(import_data.get("memory_metadata", {}))
            
            # Rebuild context index
            for key, metadata in self.memory_metadata.items():
                context = metadata.get("context", {})
                for context_key, context_value in context.items():
                    self.context_index[f"{context_key}:{context_value}"].append(key)
            
            logger.info(f"Memory imported from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import memory: {str(e)}")
            return False
    
    def clear_all(self):
        """Clear all memory entries"""
        self.memory_store.clear()
        self.memory_metadata.clear()
        self.context_index.clear()
        self.access_counts.clear()
        logger.warning("All memory cleared")


# Create global instances
session_service = InMemorySessionService()
memory_bank = MemoryBank()