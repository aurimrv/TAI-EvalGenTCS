"""
Test Evaluation Orchestrator - Coordinates agents and manages workflow.
"""

import json
import logging
from pathlib import Path
from typing import Dict

from src.models.practice_manager import PracticeManager
from src.services.llm_client import LLMClient
from src.agents.test_analyzer_agent import TestAnalyzerAgent
from src.agents.test_improver_agent import TestImproverAgent

logger = logging.getLogger(__name__)


class TestEvaluationOrchestrator:
    """Orchestrates the test evaluation and improvement process."""
    
    def __init__(self, settings):
        """
        Initialize orchestrator.
        
        Args:
            settings: Settings object with configuration
        """
        self.settings = settings
        
        # Initialize components
        self.practice_manager = PracticeManager(settings.best_practices_path)
        self.llm_client = LLMClient(settings)
        self.analyzer_agent = TestAnalyzerAgent(self.llm_client, self.practice_manager)
        self.improver_agent = TestImproverAgent()
        
        logger.info("Test Evaluation Orchestrator initialized")
        logger.info(f"Loaded {self.practice_manager.get_practice_count()} best practices")
    
    def check_best_practices(
        self,
        test_set_path: Path,
        output_dir: Path
    ) -> Dict:
        """
        Check best practices compliance and generate report.
        
        Args:
            test_set_path: Path to test set file
            output_dir: Directory for output files
        
        Returns:
            Dictionary with results including report path and compliance score
        """
        logger.info(f"Checking best practices for: {test_set_path}")
        
        # Read test code
        test_code = self._read_test_file(test_set_path)
        
        # Extract test class name
        test_class_name = self.analyzer_agent.extract_test_class_name(test_code)
        
        # Analyze test code
        analysis_result = self.analyzer_agent.analyze_test_class(
            test_code=test_code,
            test_class_name=test_class_name,
            mode='check'
        )
        
        # Save report
        report_path = self._save_report(
            analysis_result,
            test_set_path,
            output_dir
        )
        
        # Extract compliance score
        compliance_score = analysis_result.get('overall_compliance_score', 'N/A')
        
        logger.info(f"Best practices check completed. Score: {compliance_score}")
        
        return {
            'report_path': str(report_path),
            'compliance_score': compliance_score,
            'analysis_result': analysis_result
        }
    
    def improve_test_suite(
        self,
        test_set_path: Path,
        output_dir: Path
    ) -> Dict:
        """
        Improve test suite based on best practices and generate report.
        
        Args:
            test_set_path: Path to test set file
            output_dir: Directory for output files
        
        Returns:
            Dictionary with results including improved test path, report path, and compliance score
        """
        logger.info(f"Improving test suite for: {test_set_path}")
        
        # Read test code
        test_code = self._read_test_file(test_set_path)
        
        # Extract test class name
        test_class_name = self.analyzer_agent.extract_test_class_name(test_code)
        
        # Analyze test code with improvement suggestions
        analysis_result = self.analyzer_agent.analyze_test_class(
            test_code=test_code,
            test_class_name=test_class_name,
            mode='improve'
        )
        
        # Generate improved test suite
        improved_code = self.improver_agent.generate_improved_test_suite(
            analysis_result=analysis_result,
            original_code=test_code
        )
        
        # Save improved test suite
        improved_test_path = self._save_improved_test(
            improved_code,
            test_set_path,
            output_dir
        )
        
        # Save report
        report_path = self._save_report(
            analysis_result,
            test_set_path,
            output_dir
        )
        
        # Generate and save improvement summary
        summary = self.improver_agent.generate_improvement_summary(analysis_result)
        summary_path = self._save_summary(
            summary,
            test_set_path,
            output_dir
        )
        
        # Extract compliance score
        compliance_score = analysis_result.get('overall_compliance_score', 'N/A')
        
        logger.info(f"Test suite improvement completed. Score: {compliance_score}")
        
        return {
            'improved_test_path': str(improved_test_path),
            'report_path': str(report_path),
            'summary_path': str(summary_path),
            'compliance_score': compliance_score,
            'analysis_result': analysis_result
        }
    
    def _read_test_file(self, test_set_path: Path) -> str:
        """Read test file content."""
        logger.debug(f"Reading test file: {test_set_path}")
        with open(test_set_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _save_report(
        self,
        analysis_result: Dict,
        test_set_path: Path,
        output_dir: Path
    ) -> Path:
        """Save analysis report as JSON."""
        # Generate report filename
        test_name = test_set_path.stem
        report_filename = f"{test_name}_bp_report.json"
        report_path = output_dir / report_filename
        
        logger.debug(f"Saving report to: {report_path}")
        
        # Save JSON report
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Report saved: {report_path}")
        
        return report_path
    
    def _save_improved_test(
        self,
        improved_code: str,
        test_set_path: Path,
        output_dir: Path
    ) -> Path:
        """Save improved test suite."""
        # Generate improved test filename
        test_name = test_set_path.stem
        extension = test_set_path.suffix
        improved_filename = f"{test_name}_improved{extension}"
        improved_path = output_dir / improved_filename
        
        logger.debug(f"Saving improved test to: {improved_path}")
        
        # Save improved code
        with open(improved_path, 'w', encoding='utf-8') as f:
            f.write(improved_code)
        
        logger.info(f"Improved test saved: {improved_path}")
        
        return improved_path
    
    def _save_summary(
        self,
        summary: str,
        test_set_path: Path,
        output_dir: Path
    ) -> Path:
        """Save improvement summary."""
        # Generate summary filename
        test_name = test_set_path.stem
        summary_filename = f"{test_name}_improvement_summary.md"
        summary_path = output_dir / summary_filename
        
        logger.debug(f"Saving summary to: {summary_path}")
        
        # Save summary
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        logger.info(f"Summary saved: {summary_path}")
        
        return summary_path
    
    def __repr__(self) -> str:
        return f"TestEvaluationOrchestrator(practices={self.practice_manager.get_practice_count()})"
