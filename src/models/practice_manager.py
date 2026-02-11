"""
Practice Manager - Loads and manages best practices definitions.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


class BestPractice:
    """Represents a single best practice."""
    
    def __init__(self, data: dict):
        """
        Initialize best practice from dictionary.
        
        Args:
            data: Dictionary containing practice data
        """
        self.code = data['code']
        self.title = data['title']
        self.title_en = data.get('title_en', '')
        self.category = data['category']
        self.principle = data['principle']
        self.rationale = data.get('rationale', [])
        self.evaluation_criteria = data.get('evaluation_criteria', {})
        self.examples = data.get('examples', {})
    
    def to_dict(self) -> dict:
        """Convert practice to dictionary."""
        return {
            'code': self.code,
            'title': self.title,
            'title_en': self.title_en,
            'category': self.category,
            'principle': self.principle,
            'rationale': self.rationale,
            'evaluation_criteria': self.evaluation_criteria,
            'examples': self.examples,
        }
    
    def get_compact_description(self) -> str:
        """Get ultra-compact description for LLM prompt (check mode)."""
        # Ultra-compact format: just code, title, and principle
        return f"{self.code}: {self.title} - {self.principle}"
    
    def get_full_description(self) -> str:
        """Get full description for LLM prompt (improve mode)."""
        description = f"{self.code}: {self.title}\n"
        description += f"Principle: {self.principle}\n"
        
        if self.rationale:
            description += "Why?\n"
            for reason in self.rationale:
                description += f"- {reason}\n"
        
        if self.evaluation_criteria:
            description += "\nEvaluation Criteria:\n"
            if 'positive' in self.evaluation_criteria:
                description += f"✔️ Compliant: {self.evaluation_criteria['positive']}\n"
            if 'negative' in self.evaluation_criteria:
                description += f"❌ Non-Compliant: {self.evaluation_criteria['negative']}\n"
        
        return description
    
    def __repr__(self) -> str:
        return f"BestPractice({self.code}: {self.title})"


class PracticeManager:
    """Manages best practices definitions."""
    
    def __init__(self, practices_path: Path):
        """
        Initialize practice manager.
        
        Args:
            practices_path: Path to best_practices.json file
        """
        self.practices_path = practices_path
        self.practices: List[BestPractice] = []
        self._load_practices()
    
    def _load_practices(self):
        """Load practices from JSON file."""
        with open(self.practices_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.version = data.get('version', '1.0.0')
        self.description = data.get('description', '')
        
        for practice_data in data.get('practices', []):
            practice = BestPractice(practice_data)
            self.practices.append(practice)
    
    def get_all_practices(self) -> List[BestPractice]:
        """Get all best practices."""
        return self.practices
    
    def get_practice_by_code(self, code: str) -> Optional[BestPractice]:
        """
        Get practice by code.
        
        Args:
            code: Practice code (e.g., 'CS-01')
        
        Returns:
            BestPractice object or None if not found
        """
        for practice in self.practices:
            if practice.code == code:
                return practice
        return None
    
    def get_practices_by_category(self, category: str) -> List[BestPractice]:
        """
        Get practices by category.
        
        Args:
            category: Category name ('Common Sense' or 'Literature Supported')
        
        Returns:
            List of BestPractice objects
        """
        return [p for p in self.practices if p.category == category]
    
    def get_practice_count(self) -> int:
        """Get total number of practices."""
        return len(self.practices)
    
    def generate_llm_prompt_section(self, mode: str = 'check') -> str:
        """
        Generate LLM prompt section with practices.
        
        Args:
            mode: 'check' for compact version, 'improve' for full version
        
        Returns:
            Formatted string for LLM prompt
        """
        if mode == 'check':
            return self._generate_compact_prompt()
        else:
            return self._generate_full_prompt()
    
    def _generate_compact_prompt(self) -> str:
        """Generate ultra-compact prompt for check mode."""
        prompt = "\n📌 **25 Best Practices** (Compact Format)\n\n"
        
        # Group by category for better organization
        cs_practices = self.get_practices_by_category("Common Sense")
        ls_practices = self.get_practices_by_category("Literature Supported")
        
        # Common Sense practices (ultra-compact)
        prompt += "**Common Sense (CS-01 to CS-14):**\n"
        for practice in cs_practices:
            prompt += f"- {practice.get_compact_description()}\n"
        
        prompt += "\n**Literature Supported (LS-01 to LS-11):**\n"
        for practice in ls_practices:
            prompt += f"- {practice.get_compact_description()}\n"
        
        return prompt
    
    def _generate_full_prompt(self) -> str:
        """Generate full prompt for improve mode."""
        prompt = "\n📌 **Definition of the 25 Best Practices**\n\n"
        
        # Group by category
        cs_practices = self.get_practices_by_category("Common Sense")
        ls_practices = self.get_practices_by_category("Literature Supported")
        
        # Common Sense practices
        prompt += "### Common Sense practices\n\n"
        for practice in cs_practices:
            prompt += practice.get_full_description() + "\n"
        
        # Literature Supported practices
        prompt += "\n### Literature Supported practices\n\n"
        for practice in ls_practices:
            prompt += practice.get_full_description() + "\n"
        
        return prompt
    
    def get_summary(self) -> Dict:
        """Get summary of practices by category."""
        return {
            'total': len(self.practices),
            'common_sense': len(self.get_practices_by_category("Common Sense")),
            'literature_supported': len(self.get_practices_by_category("Literature Supported")),
            'version': self.version
        }
