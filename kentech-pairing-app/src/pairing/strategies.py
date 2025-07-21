"""
Pairing strategies for different use cases.
"""

from enum import Enum
from typing import Dict, Type

from src.pairing.algorithms import (
    PairingAlgorithm,
    DefaultPairingAlgorithm,
    CapabilityBasedPairingAlgorithm,
    TypeBasedPairingAlgorithm
)


class PairingStrategy(str, Enum):
    """Available pairing strategies."""
    DEFAULT = "default"
    CAPABILITY_BASED = "capability_based"
    TYPE_BASED = "type_based"


# Strategy registry
STRATEGY_REGISTRY: Dict[str, Type[PairingAlgorithm]] = {
    PairingStrategy.DEFAULT: DefaultPairingAlgorithm,
    PairingStrategy.CAPABILITY_BASED: CapabilityBasedPairingAlgorithm,
    PairingStrategy.TYPE_BASED: TypeBasedPairingAlgorithm,
}


def get_strategy(strategy_name: str) -> PairingAlgorithm:
    """Get a pairing algorithm instance by strategy name."""
    algorithm_class = STRATEGY_REGISTRY.get(
        strategy_name,
        DefaultPairingAlgorithm
    )
    return algorithm_class()


def get_available_strategies() -> list[str]:
    """Get list of available strategy names."""
    return list(STRATEGY_REGISTRY.keys())
