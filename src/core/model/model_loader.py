from pathlib import Path
from typing import Optional, Dict, Any
import torch
from transformers import AutoModel, AutoTokenizer, PreTrainedModel, PreTrainedTokenizer
import logging

logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def load_model(
        self, 
        model_path: str,
        device: Optional[str] = None
    ) -> tuple[PreTrainedModel, PreTrainedTokenizer]:
        """
        Load a model and its tokenizer from the specified path.
        
        Args:
            model_path: Path to the model (local or Hugging Face hub)
            device: Device to load the model to ('cuda', 'cpu', or None for auto)
            
        Returns:
            tuple: (model, tokenizer)
        """
        try:
            # Determine device if not specified
            if device is None:
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
            
            self.logger.info(f"Loading model from {model_path} to {device}")
            
            # Load model and tokenizer
            model = AutoModel.from_pretrained(model_path)
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # Move model to device
            model = model.to(device)
            
            return model, tokenizer
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise
