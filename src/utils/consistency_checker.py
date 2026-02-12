"""
Consistency Checker - Validates consistency of LLM responses across multiple runs.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List
from statistics import mean, stdev

logger = logging.getLogger(__name__)


class ConsistencyChecker:
    """Checks consistency of analysis results across multiple runs."""
    
    def __init__(self):
        """Initialize consistency checker."""
        self.results = []
    
    def add_result(self, result: Dict):
        """
        Add a result from a single run.
        
        Args:
            result: Analysis result dictionary
        """
        self.results.append(result)
    
    def calculate_consistency_metrics(self) -> Dict:
        """
        Calculate consistency metrics across all results.
        
        Returns:
            Dictionary with consistency metrics
        """
        if len(self.results) < 2:
            return {
                'error': 'Need at least 2 results to calculate consistency',
                'num_runs': len(self.results)
            }
        
        # Extract compliance scores
        scores = []
        for result in self.results:
            score_str = result.get('overall_compliance_score', '0%')
            # Convert "42%" to 42
            score = float(score_str.rstrip('%'))
            scores.append(score)
        
        # Calculate statistics
        mean_score = mean(scores)
        std_dev = stdev(scores) if len(scores) > 1 else 0
        min_score = min(scores)
        max_score = max(scores)
        variance = max_score - min_score
        
        # Calculate coefficient of variation (CV)
        # CV = (std_dev / mean) * 100
        cv = (std_dev / mean_score * 100) if mean_score > 0 else 0
        
        # Determine consistency level
        if cv < 5:
            consistency_level = "Excellent"
        elif cv < 10:
            consistency_level = "Good"
        elif cv < 20:
            consistency_level = "Fair"
        else:
            consistency_level = "Poor"
        
        return {
            'num_runs': len(scores),
            'scores': scores,
            'mean_score': round(mean_score, 2),
            'std_dev': round(std_dev, 2),
            'min_score': min_score,
            'max_score': max_score,
            'variance': round(variance, 2),
            'coefficient_of_variation': round(cv, 2),
            'consistency_level': consistency_level
        }
    
    def generate_consistency_report(self) -> str:
        """
        Generate a human-readable consistency report.
        
        Returns:
            Formatted report as string
        """
        metrics = self.calculate_consistency_metrics()
        
        if 'error' in metrics:
            return f"Error: {metrics['error']}"
        
        report = "# Consistency Report\n\n"
        report += f"**Number of Runs:** {metrics['num_runs']}\n\n"
        report += "## Compliance Scores\n\n"
        
        for i, score in enumerate(metrics['scores'], 1):
            report += f"- Run {i}: {score}%\n"
        
        report += "\n## Statistical Analysis\n\n"
        report += f"- **Mean Score:** {metrics['mean_score']}%\n"
        report += f"- **Standard Deviation:** {metrics['std_dev']}%\n"
        report += f"- **Min Score:** {metrics['min_score']}%\n"
        report += f"- **Max Score:** {metrics['max_score']}%\n"
        report += f"- **Variance (Range):** {metrics['variance']}%\n"
        report += f"- **Coefficient of Variation:** {metrics['coefficient_of_variation']}%\n\n"
        
        report += f"## Consistency Assessment\n\n"
        report += f"**Level:** {metrics['consistency_level']}\n\n"
        
        # Add interpretation
        report += "### Interpretation\n\n"
        
        if metrics['consistency_level'] == "Excellent":
            report += "The results are highly consistent across runs (CV < 5%). "
            report += "The LLM is producing very stable evaluations.\n"
        elif metrics['consistency_level'] == "Good":
            report += "The results show good consistency (CV < 10%). "
            report += "Minor variations are present but acceptable.\n"
        elif metrics['consistency_level'] == "Fair":
            report += "The results show moderate inconsistency (CV < 20%). "
            report += "Consider using a lower temperature or adding a seed parameter.\n"
        else:
            report += "The results show significant inconsistency (CV ≥ 20%). "
            report += "**Recommendations:**\n"
            report += "- Set `LLM_TEMPERATURE=0.0` for maximum determinism\n"
            report += "- Add `LLM_SEED=42` (or any integer) for reproducible results\n"
            report += "- Use a more stable model (e.g., `openai/gpt-4.1-mini`)\n"
            report += "- Avoid models with JSON parsing errors\n"
        
        return report
    
    def save_consistency_report(self, output_path: Path):
        """
        Save consistency report to file.
        
        Args:
            output_path: Path to save the report
        """
        report = self.generate_consistency_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Consistency report saved: {output_path}")


def analyze_multiple_reports(report_paths: List[Path]) -> Dict:
    """
    Analyze consistency across multiple report files.
    
    Args:
        report_paths: List of paths to report JSON files
    
    Returns:
        Consistency metrics dictionary
    """
    checker = ConsistencyChecker()
    
    for report_path in report_paths:
        with open(report_path, 'r', encoding='utf-8') as f:
            result = json.load(f)
            checker.add_result(result)
    
    return checker.calculate_consistency_metrics()
