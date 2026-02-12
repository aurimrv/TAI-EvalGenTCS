"""
Test Analyzer Agent - Analyzes test code and evaluates best practices compliance.
"""

import logging
from pathlib import Path
from typing import Dict, List

from src.models.practice_manager import PracticeManager
from src.services.llm_client import LLMClient

logger = logging.getLogger(__name__)


class TestAnalyzerAgent:
    """Agent responsible for analyzing test code."""
    
    def __init__(self, llm_client: LLMClient, practice_manager: PracticeManager):
        """
        Initialize test analyzer agent.
        
        Args:
            llm_client: LLM client for API calls
            practice_manager: Practice manager with best practices
        """
        self.llm_client = llm_client
        self.practice_manager = practice_manager
        logger.info("Test Analyzer Agent initialized")
    
    def analyze_test_class(
        self,
        test_code: str,
        test_class_name: str,
        mode: str = 'check'
    ) -> Dict:
        """
        Analyze a test class for best practices compliance.
        
        Args:
            test_code: Source code of the test class
            test_class_name: Name of the test class
            mode: 'check' or 'improve'
        
        Returns:
            Dictionary with analysis results following the JSON schema
        """
        logger.info(f"Analyzing test class: {test_class_name} (mode: {mode})")
        
        # Check test file size and warn if it's too large
        test_code_lines = len(test_code.split('\n'))
        test_code_chars = len(test_code)
        logger.debug(f"Test file size: {test_code_lines} lines, {test_code_chars} chars")
        
        if test_code_lines > 200 or test_code_chars > 10000:
            logger.warning(f"Large test file detected ({test_code_lines} lines, {test_code_chars} chars)")
            logger.warning("This may cause token limit issues with some LLM models")
            logger.warning("Consider using a model with larger context window (e.g., openai/gpt-4o-mini)")
        
        # Build system prompt
        system_prompt = self._build_system_prompt(mode)
        
        # Build user message
        user_message = self._build_user_message(test_code, test_class_name)
        
        # Get JSON schema
        json_schema = self._get_json_schema()
        
        # Call LLM
        logger.debug("Sending analysis request to LLM...")
        try:
            result = self.llm_client.generate_json_completion(
                system_prompt=system_prompt,
                user_message=user_message,
                json_schema=json_schema
            )
        except Exception as e:
            logger.error(f"Failed to get valid JSON response from LLM: {e}")
            logger.info("Retrying without strict JSON schema...")
            # Retry without strict schema for models that don't support it
            result = self.llm_client.generate_json_completion(
                system_prompt=system_prompt,
                user_message=user_message,
                json_schema=None
            )
        
        logger.info(f"Analysis completed for {test_class_name}")
        
        return result
    
    def _build_system_prompt(self, mode: str) -> str:
        """Build system prompt based on mode."""
        base_prompt = """You are an expert in software testing and best practices for writing test cases. 
Your task is to analyze the provided test code and compare it against the **25 best practices** listed below.

📌 **CRITICAL: Strict JSON Schema Requirements**
- You MUST return ONLY valid JSON following the exact schema provided
- DO NOT return a flat structure with practice codes as keys
- The response MUST have this structure:
  {
    "test_class_name": "ClassName",
    "test_methods": [
      {
        "test_method_name": "methodName",
        "practices_evaluation": [...],
        "method_compliance_score": "X%",
        "suggested_code": "..."
      }
    ],
    "practices_report": [...],
    "overall_compliance_score": "X%"
  }
- Every test method MUST have evaluations for all 25 practices
- The `"status"` field must be: `"✔️"` (Compliant), `"❌"` (Non-Compliant), or `"⚪"` (Not Applicable)
- Compliance scores are calculated as: (compliant ✔️ / 25) * 100 and formatted as "X%"
- DO NOT include any text outside the JSON structure

📌 **CRITICAL: Consistent Evaluation**
- Evaluate STRICTLY based on the code provided - do not assume missing elements exist
- Use ✔️ ONLY if the practice is clearly implemented in the code
- Use ❌ if the practice is not implemented or only partially implemented
- Use ⚪ ONLY if the practice is genuinely not applicable to this specific test
- Be CONSERVATIVE: when in doubt between ✔️ and ❌, choose ❌
- The evaluation criteria provided for each practice are DEFINITIVE - follow them exactly"""
        
        if mode == 'improve':
            base_prompt += """

📌 **CRITICAL: Improved Code Generation**
- The "suggested_code" field in the FIRST test method MUST contain the COMPLETE improved test class
- Include package declaration, imports, class declaration, ALL test methods, and closing brace
- DO NOT put the improved class in each method - only in the FIRST method's "suggested_code"
- For subsequent methods, set "suggested_code" to an empty string ""
- The improved class must:
  * Preserve the ORIGINAL class name (e.g., UserServiceTest, not UserServiceTest_improved)
  * Implement all applicable best practices
  * Maintain the original test logic and coverage
  * Be fully compilable and runnable Java code
  * NOT include any commented-out code
  * NOT repeat the class definition multiple times

"""
        
        # Add practices definitions
        practices_section = self.practice_manager.generate_llm_prompt_section(mode)
        
        return base_prompt + "\n" + practices_section
    
    def _build_user_message(self, test_code: str, test_class_name: str) -> str:
        """Build user message with test code."""
        return f"""Analyze the following test class and evaluate each of the 25 best practices:

**Test Class:** {test_class_name}

```
{test_code}
```

Please provide the complete analysis in the specified JSON format.
"""
    
    def _get_json_schema(self) -> Dict:
        """Get JSON schema for response validation."""
        return {
            "name": "test_evaluation_report",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "test_class_name": {
                        "type": "string",
                        "description": "Name of the test class being evaluated"
                    },
                    "test_methods": {
                        "type": "array",
                        "description": "List of test methods in the class",
                        "items": {
                            "type": "object",
                            "properties": {
                                "test_method_name": {"type": "string"},
                                "practices_evaluation": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "practice_code": {"type": "string"},
                                            "practice_title": {"type": "string"},
                                            "status": {"type": "string"},
                                            "justification": {"type": "string"},
                                            "original_code": {"type": ["string", "null"]},
                                            "improved_code": {"type": ["string", "null"]}
                                        },
                                        "required": ["practice_code", "practice_title", "status", "justification", "original_code", "improved_code"],
                                        "additionalProperties": False
                                    }
                                },
                                "method_compliance_score": {"type": "string"},
                                "suggested_code": {"type": "string"}
                            },
                            "required": ["test_method_name", "practices_evaluation", "method_compliance_score", "suggested_code"],
                            "additionalProperties": False
                        }
                    },
                    "practices_report": {
                        "type": "array",
                        "description": "Summary report of compliance for each practice",
                        "items": {
                            "type": "object",
                            "properties": {
                                "practice_code": {"type": "string"},
                                "practice_title": {"type": "string"},
                                "description": {"type": "string"},
                                "compliant_methods": {"type": "integer"},
                                "non_compliant_methods": {"type": "integer"},
                                "not_applicable_methods": {"type": "integer"},
                                "total_methods": {"type": "integer"},
                                "compliance_score": {"type": "string"}
                            },
                            "required": [
                                "practice_code", "practice_title", "description",
                                "compliant_methods", "non_compliant_methods",
                                "not_applicable_methods", "total_methods", "compliance_score"
                            ],
                            "additionalProperties": False
                        }
                    },
                    "overall_compliance_score": {
                        "type": "string",
                        "description": "Overall compliance score"
                    }
                },
                "required": ["test_class_name", "test_methods", "practices_report", "overall_compliance_score"],
                "additionalProperties": False
            }
        }
    
    def extract_test_class_name(self, test_code: str) -> str:
        """
        Extract test class name from code.
        
        Args:
            test_code: Source code of the test
        
        Returns:
            Test class name or 'UnknownTestClass'
        """
        # Simple heuristic to extract class name
        # This can be improved with proper parsing
        lines = test_code.split('\n')
        for line in lines:
            if 'class ' in line and '{' in line:
                parts = line.split('class ')[1].split('{')[0].strip()
                # Remove 'extends' or 'implements' if present
                class_name = parts.split()[0]
                return class_name
        
        return 'UnknownTestClass'
    
    def __repr__(self) -> str:
        return "TestAnalyzerAgent()"
