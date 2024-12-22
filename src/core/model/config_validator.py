from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ModelConfigValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def validate_merge_config(
        self,
        config: Dict[str, Any]
    ) -> bool:
        """
        Validate a model merge configuration.
        
        Args:
            config: Dictionary containing merge configuration
            
        Returns:
            bool: True if configuration is valid
        """
        required_fields = ['model_paths', 'merge_strategy']
        
        try:
            # Check required fields
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate model paths
            if not isinstance(config['model_paths'], list):
                raise ValueError("model_paths must be a list")
            if len(config['model_paths']) < 2:
                raise ValueError("At least two models are required for merging")
            
            # Validate merge strategy
            valid_strategies = ['weighted_average']
            if config['merge_strategy'] not in valid_strategies:
                raise ValueError(
                    f"Invalid merge strategy. Must be one of: {valid_strategies}"
                )
            
            # Validate weights if provided
            if 'weights' in config:
                weights = config['weights']
                if not isinstance(weights, list):
                    raise ValueError("weights must be a list")
                if len(weights) != len(config['model_paths']):
                    raise ValueError(
                        "Number of weights must match number of models"
                    )
                if abs(sum(weights) - 1.0) > 1e-6:
                    raise ValueError("Weights must sum to 1")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation error: {str(e)}")
            raise