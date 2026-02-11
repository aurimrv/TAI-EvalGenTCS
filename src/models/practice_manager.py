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
        """Get compact description for LLM prompt (check mode)."""
        return f"{self.code}: {self.title}\n- {self.principle}"
    
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
        self.source = data.get('source', '')
        self.author = data.get('author', '')
        
        for practice_data in data['practices']:
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
        """Generate compact prompt for check mode."""
        prompt = "📌 **Definition of the 25 Best Practices**\n\n"
        
        # Common Sense practices
        cs_practices = self.get_practices_by_category('Common Sense')
        prompt += "### **Common Sense Practices**\n"
        for practice in cs_practices:
            prompt += f"{practice.get_compact_description()}\n\n"
        
        # Literature Supported practices
        ls_practices = self.get_practices_by_category('Literature Supported')
        prompt += "### **Literature Supported Practices**\n"
        for practice in ls_practices:
            prompt += f"{practice.get_compact_description()}\n\n"
        
        return prompt
    
    def _generate_full_prompt(self) -> str:
        """Generate full prompt for improve mode."""
        prompt = "📌 **Definition of the 25 Best Practices**\n\n"
        
        # Common Sense practices
        cs_practices = self.get_practices_by_category('Common Sense')
        prompt += "### **Common Sense Practices**\n\n"
        for practice in cs_practices:
            prompt += f"{practice.get_full_description()}\n---\n\n"
        
        # Literature Supported practices
        ls_practices = self.get_practices_by_category('Literature Supported')
        prompt += "### **Literature Supported Practices**\n\n"
        for practice in ls_practices:
            prompt += f"{practice.get_full_description()}\n---\n\n"
        
        return prompt
    
    def get_practice_summary(self) -> Dict[str, int]:
        """Get summary of practices by category."""
        cs_count = len(self.get_practices_by_category('Common Sense'))
        ls_count = len(self.get_practices_by_category('Literature Supported'))
        
        return {
            'total': self.get_practice_count(),
            'common_sense': cs_count,
            'literature_supported': ls_count,
        }
    
    def __repr__(self) -> str:
        summary = self.get_practice_summary()
        return (
            f"PracticeManager(total={summary['total']}, "
            f"CS={summary['common_sense']}, "
            f"LS={summary['literature_supported']})"
        )
