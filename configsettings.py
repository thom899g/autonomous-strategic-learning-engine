"""
Configuration management for ASLE
Critical: Centralized config prevents hard-coded values and enables runtime adjustments
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

# Path configuration
BASE_DIR = Path(__file__).parent.parent
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
STRATEGIES_DIR = BASE_DIR / "strategies"

# Create directories if they don't exist
for directory in [LOG_DIR, DATA_DIR, STRATEGIES_DIR]:
    directory.mkdir(exist_ok=True)

# Exchange configuration
EXCHANGE_CONFIG = {
    "binance": {
        "api_key": os.getenv("BINANCE_API_KEY", ""),
        "secret": os.getenv("BINANCE_API_SECRET", ""),
        "rate_limit": True,
        "enableRateLimit": True
    },
    "coinbase": {
        "api_key": os.getenv("COINBASE_API_KEY", ""),
        "secret": os.getenv("COINBASE_API_SECRET", ""),
        "timeout": 30000
    }
}

# Strategy parameters
DEFAULT_STRATEGY_PARAMS = {
    "lookback_periods": [20, 50, 200],
    "volatility_window": 20,
    "risk_per_trade": 0.02,  # 2% risk per trade
    "max_positions": 5,
    "min_confidence_threshold": 0.65
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "min_sharpe_ratio": 1.0,
    "max_drawdown": -0.20,
    "min_win_rate": 0.45,
    "min_profit_factor": 1.5
}

# Firebase configuration (CRITICAL for state management)
FIREBASE_CONFIG = {
    "project_id": os.getenv("FIREBASE_PROJECT_ID", ""),
    "credentials_path": os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json"),
    "collections": {
        "strategies": "asle_strategies",
        "trades": "asle_trades",
        "market_data": "asle_market_data",
        "performance": "asle_performance"
    }
}

def validate_config() -> Dict[str, bool]:
    """Validate all required configuration is present"""
    validations = {
        "exchange_credentials": bool(EXCHANGE_CONFIG["binance"]["api_key"]),
        "firebase_credentials": os.path.exists(FIREBASE_CONFIG["credentials_path"]),
        "directories_exist": all([
            LOG_DIR.exists(),
            DATA_DIR.exists(),
            STRATEGIES_DIR.exists()
        ])
    }
    return validations