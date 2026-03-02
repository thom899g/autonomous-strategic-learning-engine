"""
Firebase-based state management for ASLE
CRITICAL: All state must persist in Firebase for reliability and real-time updates
"""
import json
from datetime import datetime
from typing import Any, Dict, Optional, List
import logging

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client as FirestoreClient
from google.cloud.firestore_v1.document import DocumentReference

from config.settings import FIREBASE_CONFIG

logger = logging.getLogger(__name__)


class StateManager:
    """Centralized state management using Firebase Firestore"""
    
    def __init__(self):
        """Initialize Firebase connection with error handling"""
        self._client: Optional[FirestoreClient] = None
        self._initialized = False
        self._initialize_firebase()
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase Admin SDK with robust error handling"""
        try:
            if not firebase_admin._apps:
                cred_path = FIREBASE_CONFIG["credentials_path"]
                if not Path(cred_path).exists():
                    raise FileNotFoundError(
                        f"Firebase credentials not found at {cred_path}. "
                        "Please download from Firebase Console and place in project root."
                    )