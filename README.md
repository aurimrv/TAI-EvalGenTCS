# TAI-EvalGenTCS CLI

**Test AI Evaluator and Generator of Test Case Suites - Command Line Interface**

A command-line tool for evaluating and improving test suites based on 25 software engineering best practices, developed as part of doctoral research at the **Federal University of São Carlos (UFSCar)**.

## 📋 About the Project

This tool implements the findings of the PhD thesis *"Towards a strategy and tool support for test generation based on good software testing practices: classification and prioritization"* by **Camilo Hernán Villota Ibarra**, offering a command-line interface to:

- **Evaluate** the compliance of test cases with 25 fundamental best practices
- **Automatically improve** test suites based on these best practices
- **Generate** detailed reports in JSON format

### Theoretical Foundation

The tool is based on a **Systematic Literature Review (SLR)** that:
- Identified **131 software testing practices** from 103 primary studies
- Refined and synthesized these into **40 essential best practices**
- Empirically validated them through a survey with professional testers
- Implements **25 fundamental best practices** divided into:
  - **Common Sense (CS)**: 14 industry-validated common-sense practices
  - **Literature Supported (LS)**: 11 practices backed by academic research

## 🏗️ Architecture

The system uses a **multi-agent architecture** with the following components:

```
tai-evalgentcs-cli/
├── main.py                          # CLI entry point
├── src/
│   ├── agents/                      # Specialized agents
│   │   ├── test_analyzer_agent.py   # Test code analysis
│   │   └── test_improver_agent.py   # Improved code generation
│   ├── config/                      # Configuration
│   │   └── settings.py              # Settings management
│   ├── models/                      # Data models
│   │   └── practice_manager.py      # Best practices management
│   ├── services/                    # Services
│   │   ├── llm_client.py            # LLM client with rate limiting
│   │   └── orchestrator.py          # Workflow orchestration
│   └── utils/                       # Utilities
│       └── logger.py                # Logging configuration
├── data/
│   └── best_practices.json          # Definitions of the 25 best practices
├── requirements.txt                 # Python dependencies
└── .env.example                     # Configuration template
```

### Core Components

- **TestAnalyzerAgent**: Analyzes test code and evaluates compliance with best practices
- **TestImproverAgent**: Generates improved versions of the test code
- **PracticeManager**: Manages the definitions of the 25 best practices
- **LLMClient**: Client for communication with the OpenRouter API (rate limiting and retry)
- **TestEvaluationOrchestrator**: Coordinates the workflow between agents

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- An [OpenRouter](https://openrouter.ai/) account
- A minimum credit of $15 on OpenRouter (for adequate rate limits)

### Installation Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd tai-evalgentcs-cli
```

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

## ⚙️ Configuration

Edit the `.env` file with your settings:

```env
# OpenRouter API Key (required)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# LLM Model (recommended: openai/gpt-4.1-mini)
LLM_MODEL=openai/gpt-4.1-mini

# Temperature (0.0-1.0, recommended: 0.1 for code analysis)
LLM_TEMPERATURE=0.1

# Rate Limiting (for credit > $15)
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_TOKENS_PER_MINUTE=100000
```

## 📖 Usage

### Mode 1: Check Best Practice Compliance

Generates a detailed JSON report on test code compliance:

```bash
python main.py --check-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./reports
```

**Output:**
- `UserServiceTest_bp_report.json`: Complete JSON report

### Mode 2: Improve Test Suite

Generates an improved version of the test code based on best practices:

```bash
python main.py --improve-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./improved
```

**Output:**
- `UserServiceTest_improved.java`: Improved test code
- `UserServiceTest_bp_report.json`: Complete JSON report
- `UserServiceTest_improvement_summary.md`: Summary of improvements

### Additional Options

```bash
# Use a specific LLM model
python main.py --check-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./reports \
  --llm-model openai/gpt-4-turbo

# Enable verbose logging
python main.py --check-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./reports \
  --verbose

# Use a custom configuration file
python main.py --check-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./reports \
  --config custom.env
```

## 📊 Report Format

The JSON report follows the schema defined in `report-schema.json` and includes:

### Report Structure

```json
{
  "test_class_name": "UserServiceTest",
  "test_methods": [
    {
      "test_method_name": "testCreateUser",
      "practices_evaluation": [
        {
          "practice_code": "CS-01",
          "practice_title": "Atomic Specification of Test Cases",
          "status": "✔️",
          "justification": "The test focuses on a single behavior...",
          "original_code": null,
          "improved_code": null
        }
      ],
      "method_compliance_score": "92%",
      "suggested_code": "..."
    }
  ],
  "practices_report": [
    {
      "practice_code": "CS-01",
      "practice_title": "Atomic Specification of Test Cases",
      "description": "...",
      "compliant_methods": 5,
      "non_compliant_methods": 1,
      "not_applicable_methods": 0,
      "total_methods": 6,
      "compliance_score": "83%"
    }
  ],
  "overall_compliance_score": "87%"
}
```

### Compliance Status

- **✔️ (Compliant)**: The practice is followed correctly
- **❌ (Non-Compliant)**: The practice is not followed (with improvement suggestions)
- **⚪ (Not Applicable)**: The practice does not apply to the test context

## 🎯 The 25 Best Practices

### Common Sense Practices (CS-01 to CS-14)

1. **CS-01**: Atomic Specification of Test Cases
2. **CS-02**: Complete Independence of Test Cases
3. **CS-03**: Coverage of Normal and Exceptional Flows
4. **CS-04**: Boundary Value Analysis
5. **CS-05**: Complete Modularity of Test Cases
6. **CS-06**: Detailed Analysis of Size and Complexity
7. **CS-07**: Complex Design for Fault Detection
8. **CS-08**: Complete Maintenance of Test Code
9. **CS-09**: Complete Traceability of Test Cases
10. **CS-10**: Rigorous Use of Performance and Security Tests
11. **CS-11**: Regular Review of Test Cases
12. **CS-12**: Clear Understanding of Test Cases
13. **CS-13**: Structured Coverage of the Testing Process
14. **CS-14**: Complete Guarantee of Test Code Quality

### Literature Supported Practices (LS-01 to LS-11)

1. **LS-01**: Adequate Use of Code Coverage
2. **LS-02**: Necessary Use of Missing Tests
3. **LS-03**: Efficient Use of Code Coverage
4. **LS-04**: Small Footprint of Test Code Generation
5. **LS-05**: Complete Prioritization of Test Case Design
6. **LS-06**: Responsible Addition of Test Code Maintenance
7. **LS-07**: Adequate Use of Test Assertions
8. **LS-08**: Responsible Addition of Debugging Comments
9. **LS-09**: Deterministic Design of Test Results
10. **LS-10**: Complete Avoidance of Test Side Effects
11. **LS-11**: Adequate Use of Labels and Categories

Full details in `data/best_practices.json`.

## 🔧 Development

### Running Tests

```bash
pytest tests/ -v --cov=src
```

### Clean Architecture

The project follows **Clean Architecture** principles:

- **Separation of concerns**: Each module has a clear responsibility
- **Dependency inversion**: Components depend on abstractions
- **Testability**: Easily testable code with mocks
- **External configuration**: All settings via `.env`

## 📚 References

- **PhD Thesis**: "Towards a strategy and tool support for test generation based on good software testing practices: classification and prioritization"
- **Author**: Camilo Hernán Villota Ibarra
- **Advisor**: Prof. Dr. Auri Marcelo Rizzo Vincenzi
- **Co-advisor**: Prof. Dr. José Carlos Maldonado
- **Institution**: Federal University of São Carlos (UFSCar)

## 📄 License

This project is part of academic research at UFSCar.

## 👥 Authors

- **Camilo Hernán Villota Ibarra** - Main Author and Researcher
- **Auri Marcelo Rizzo Vincenzi** - Advisor
- **José Carlos Maldonado** - Co-advisor

## 🤝 Contributions

For questions, suggestions, or contributions, please contact the authors.
