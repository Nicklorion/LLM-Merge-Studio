from dataclasses import dataclass
from typing import Optional
import torch
import psutil
import math

@dataclass
class SystemResources:
    total_cpu: float  # MHz
    available_cpu: float
    total_ram: float  # GB
    available_ram: float
    total_gpu_memory: Optional[float] = None  # GB
    available_gpu_memory: Optional[float] = None
    cuda_available: bool = False

@dataclass
class ModelRequirements:
    estimated_cpu: float
    estimated_ram: float
    estimated_gpu_memory: Optional[float] = None
    requires_cuda: bool = False

class ResourcePredictor:
    def __init__(self):
        self.system_resources = self._get_system_resources()
    
    def _get_system_resources(self) -> SystemResources:
        """Get current system resources"""
        cpu_freq = psutil.cpu_freq()
        mem = psutil.virtual_memory()
        
        resources = SystemResources(
            total_cpu=cpu_freq.max if cpu_freq else 0,
            available_cpu=cpu_freq.current if cpu_freq else 0,
            total_ram=mem.total / (1024**3),
            available_ram=mem.available / (1024**3),
            cuda_available=torch.cuda.is_available()
        )
        
        if resources.cuda_available:
            resources.total_gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            resources.available_gpu_memory = (torch.cuda.get_device_properties(0).total_memory - 
                                           torch.cuda.memory_allocated()) / (1024**3)
        
        return resources
    
    def estimate_merge_requirements(
        self,
        model_sizes: list[int],  # Sizes in bytes
        merge_strategy: str
    ) -> ModelRequirements:
        """Estimate resource requirements for model merging"""
        total_size = sum(model_sizes)
        
        # Base RAM requirement: sum of model sizes + 20% overhead
        base_ram = (total_size / (1024**3)) * 1.2
        
        # GPU memory if available
        gpu_memory = base_ram if self.system_resources.cuda_available else None
        
        # CPU estimation based on model size and merge strategy
        cpu_factor = 1.5 if merge_strategy == "weighted_average" else 2.0
        estimated_cpu = min(psutil.cpu_count() or 1, math.ceil(base_ram * cpu_factor))
        
        return ModelRequirements(
            estimated_cpu=estimated_cpu,
            estimated_ram=base_ram,
            estimated_gpu_memory=gpu_memory,
            requires_cuda=self.system_resources.cuda_available
        )
    
    def can_perform_merge(self, requirements: ModelRequirements) -> tuple[bool, str]:
        """Check if merge operation can be performed with current resources"""
        messages = []
        can_perform = True
        
        # Check RAM
        if requirements.estimated_ram > self.system_resources.available_ram:
            can_perform = False
            messages.append(
                f"Insufficient RAM. Required: {requirements.estimated_ram:.2f}GB, "
                f"Available: {self.system_resources.available_ram:.2f}GB"
            )
        
        # Check GPU if required
        if requirements.requires_cuda:
            if not self.system_resources.cuda_available:
                can_perform = False
                messages.append("CUDA required but not available")
            elif (requirements.estimated_gpu_memory and 
                  requirements.estimated_gpu_memory > self.system_resources.available_gpu_memory):
                can_perform = False
                messages.append(
                    f"Insufficient GPU memory. Required: {requirements.estimated_gpu_memory:.2f}GB, "
                    f"Available: {self.system_resources.available_gpu_memory:.2f}GB"
                )
        
        return can_perform, ". ".join(messages)
