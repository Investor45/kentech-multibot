"""
Pairing algorithms for bot matching.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
import random

from src.bots.models import Bot


class PairingAlgorithm(ABC):
    """Abstract base class for pairing algorithms."""
    
    @abstractmethod
    def pair_bots(self, bots: List[Bot]) -> List[Tuple[Bot, Bot]]:
        """Pair bots based on the algorithm logic."""
        pass


class DefaultPairingAlgorithm(PairingAlgorithm):
    """Default pairing algorithm - simple random pairing."""
    
    def pair_bots(self, bots: List[Bot]) -> List[Tuple[Bot, Bot]]:
        """Randomly pair available bots."""
        if len(bots) < 2:
            return []
        
        # Shuffle bots for random pairing
        shuffled_bots = bots.copy()
        random.shuffle(shuffled_bots)
        
        pairs = []
        for i in range(0, len(shuffled_bots) - 1, 2):
            pairs.append((shuffled_bots[i], shuffled_bots[i + 1]))
        
        return pairs


class CapabilityBasedPairingAlgorithm(PairingAlgorithm):
    """Pair bots based on complementary capabilities."""
    
    def pair_bots(self, bots: List[Bot]) -> List[Tuple[Bot, Bot]]:
        """Pair bots with complementary capabilities."""
        if len(bots) < 2:
            return []
        
        # Sort bots by capabilities for better matching
        sorted_bots = sorted(bots, key=lambda b: b.capabilities or "")
        
        pairs = []
        used_bots = set()
        
        for i, bot1 in enumerate(sorted_bots):
            if bot1.id in used_bots:
                continue
            
            # Find the best matching partner
            best_match = None
            best_score = -1
            
            for j, bot2 in enumerate(sorted_bots[i + 1:], i + 1):
                if bot2.id in used_bots:
                    continue
                
                score = self._calculate_compatibility(bot1, bot2)
                if score > best_score:
                    best_score = score
                    best_match = bot2
            
            if best_match:
                pairs.append((bot1, best_match))
                used_bots.add(bot1.id)
                used_bots.add(best_match.id)
        
        return pairs
    
    def _calculate_compatibility(self, bot1: Bot, bot2: Bot) -> float:
        """Calculate compatibility score between two bots."""
        # Simple compatibility scoring based on capabilities
        caps1 = set((bot1.capabilities or "").split(","))
        caps2 = set((bot2.capabilities or "").split(","))
        
        # Different capabilities are complementary
        if caps1 != caps2:
            return len(caps1.union(caps2)) / max(len(caps1), len(caps2), 1)
        
        return 0.5  # Same capabilities get neutral score


class TypeBasedPairingAlgorithm(PairingAlgorithm):
    """Pair bots based on bot types."""
    
    def pair_bots(self, bots: List[Bot]) -> List[Tuple[Bot, Bot]]:
        """Pair bots of different types when possible."""
        if len(bots) < 2:
            return []
        
        # Group bots by type
        bot_types = {}
        for bot in bots:
            if bot.bot_type not in bot_types:
                bot_types[bot.bot_type] = []
            bot_types[bot.bot_type].append(bot)
        
        pairs = []
        used_bots = set()
        type_list = list(bot_types.keys())
        
        # Try to pair different types first
        for i, type1 in enumerate(type_list):
            for type2 in type_list[i + 1:]:
                bots1 = [b for b in bot_types[type1] if b.id not in used_bots]
                bots2 = [b for b in bot_types[type2] if b.id not in used_bots]
                
                min_pairs = min(len(bots1), len(bots2))
                for j in range(min_pairs):
                    pairs.append((bots1[j], bots2[j]))
                    used_bots.add(bots1[j].id)
                    used_bots.add(bots2[j].id)
        
        # Pair remaining bots of same type
        for bot_type, type_bots in bot_types.items():
            available_bots = [b for b in type_bots if b.id not in used_bots]
            for i in range(0, len(available_bots) - 1, 2):
                pairs.append((available_bots[i], available_bots[i + 1]))
                used_bots.add(available_bots[i].id)
                used_bots.add(available_bots[i + 1].id)
        
        return pairs
