from typing import List, Dict, Any, Optional
import torch
from transformers import PreTrainedModel
import logging

logger = logging.getLogger(__name__)

class ModelMerger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def merge_models(
        self,
        models: List[PreTrainedModel],
        weights: Optional[List[float]] = None,
        merge_strategy: str = "weighted_average"
    ) -> PreTrainedModel:
        """
        Merge multiple models using the specified strategy.
        
        Args:
            models: List of models to merge
            weights: Optional list of weights for each model (must sum to 1)
            merge_strategy: Strategy to use for merging ("weighted_average" for now)
            
        Returns:
            Merged model
        """
        if not models:
            raise ValueError("No models provided for merging")
            
        if len(models) == 1:
            return models[0]
            
        # Validate models are compatible
        base_config = models[0].config
        for model in models[1:]:
            if not self._are_models_compatible(models[0], model):
                raise ValueError("Models are not compatible for merging")
        
        # Handle weights
        if weights is None:
            weights = [1.0 / len(models)] * len(models)
        elif len(weights) != len(models):
            raise ValueError("Number of weights must match number of models")
        elif abs(sum(weights) - 1.0) > 1e-6:
            raise ValueError("Weights must sum to 1")
            
        try:
            if merge_strategy == "weighted_average":
                return await self._weighted_average_merge(models, weights)
            else:
                raise ValueError(f"Unsupported merge strategy: {merge_strategy}")
                
        except Exception as e:
            self.logger.error(f"Error during model merging: {str(e)}")
            raise
            
    async def _weighted_average_merge(
        self,
        models: List[PreTrainedModel],
        weights: List[float]
    ) -> PreTrainedModel:
        """
        Merge models using weighted average of their parameters.
        """
        merged_model = models[0].__class__(models[0].config)
        
        with torch.no_grad():
            for name, param in merged_model.named_parameters():
                # Initialize with weighted parameters of first model
                param.data = models[0].state_dict()[name].data * weights[0]
                
                # Add weighted parameters from other models
                for model, weight in zip(models[1:], weights[1:]):
                    param.data += model.state_dict()[name].data * weight
                    
        return merged_model
        
    def _are_models_compatible(
        self,
        model1: PreTrainedModel,
        model2: PreTrainedModel
    ) -> bool:
        """
        Check if two models are compatible for merging.
        """
        # Check architecture
        if model1.__class__ != model2.__class__:
            return False
            
        # Check parameter shapes
        for (name1, param1), (name2, param2) in zip(
            model1.named_parameters(), model2.named_parameters()
        ):
            if name1 != name2 or param1.shape != param2.shape:
                return False
                
        return True
