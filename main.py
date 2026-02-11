#!/usr/bin/env python3
"""
TAI-EvalGenTCS CLI - Test AI Evaluator and Generator of Test Case Suites
Command-line interface for evaluating and improving test suites based on best practices.

Author: Camilo Hernán Villota Ibarra
Based on PhD Thesis: "Towards a strategy and tool support for test generation based on good software testing practices: classification and prioritization"
"""

import argparse
import sys
from pathlib import Path

from src.config.settings import Settings
from src.services.orchestrator import TestEvaluationOrchestrator
from src.utils.logger import setup_logger


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="TAI-EvalGenTCS: Evaluate and improve test suites based on best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check best practices compliance
  python main.py --check-best-practice --original-test-set tests/UserServiceTest.java --output-dir ./reports

  # Improve test suite based on best practices
  python main.py --improve-best-practice --original-test-set tests/UserServiceTest.java --output-dir ./improved

  # Use specific LLM model
  python main.py --check-best-practice --original-test-set tests/UserServiceTest.java --output-dir ./reports --llm-model gpt-4.1-mini
        """
    )
    
    # Mutually exclusive group for operation mode
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--check-best-practice',
        action='store_true',
        help='Generate detailed report about best practice compliance'
    )
    mode_group.add_argument(
        '--improve-best-practice',
        action='store_true',
        help='Create improved version of test suite based on best practices'
    )
    
    # Required arguments
    parser.add_argument(
        '--original-test-set',
        type=str,
        required=True,
        help='Path to the original test set file to evaluate'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        required=True,
        help='Directory where output files will be saved'
    )
    
    # Optional arguments
    parser.add_argument(
        '--llm-model',
        type=str,
        help='LLM model to use (overrides .env configuration)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set logging level (overrides --verbose and .env LOG_LEVEL)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom configuration file'
    )
    
    return parser.parse_args()


def validate_arguments(args):
    """Validate command-line arguments."""
    # Check if test set file exists
    test_set_path = Path(args.original_test_set)
    if not test_set_path.exists():
        print(f"Error: Test set file not found: {args.original_test_set}")
        sys.exit(1)
    
    if not test_set_path.is_file():
        print(f"Error: Test set path is not a file: {args.original_test_set}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return test_set_path, output_dir


def main():
    """Main entry point for the CLI application."""
    args = parse_arguments()
    
    # Load settings first to get log level from .env
    settings = Settings(config_path=args.config)
    
    # Setup logger with priority: CLI --log-level > CLI --verbose > .env LOG_LEVEL
    log_level = args.log_level if args.log_level else (None if not args.verbose else 'DEBUG')
    if not log_level:
        log_level = settings.log_level
    
    logger = setup_logger(log_level=log_level)
    logger.info("TAI-EvalGenTCS CLI - Starting...")
    
    # Validate arguments
    test_set_path, output_dir = validate_arguments(args)
    
    try:
        
        # Override LLM model if specified
        if args.llm_model:
            settings.llm_model = args.llm_model
            logger.info(f"Using LLM model: {args.llm_model}")
        
        # Determine operation mode
        operation_mode = "check" if args.check_best_practice else "improve"
        logger.info(f"Operation mode: {operation_mode}")
        logger.info(f"Test set: {test_set_path}")
        logger.info(f"Output directory: {output_dir}")
        
        # Create orchestrator
        orchestrator = TestEvaluationOrchestrator(settings)
        
        # Execute operation
        if operation_mode == "check":
            logger.info("Checking best practice compliance...")
            result = orchestrator.check_best_practices(test_set_path, output_dir)
            logger.info(f"Report generated: {result['report_path']}")
            logger.info(f"Overall compliance score: {result['compliance_score']}")
        else:
            logger.info("Improving test suite based on best practices...")
            result = orchestrator.improve_test_suite(test_set_path, output_dir)
            logger.info(f"Improved test suite: {result['improved_test_path']}")
            logger.info(f"Report generated: {result['report_path']}")
            logger.info(f"Overall compliance score: {result['compliance_score']}")
        
        logger.info("Operation completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
