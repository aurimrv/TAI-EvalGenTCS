# Quick Start Guide - TAI-EvalGenTCS CLI

This guide provides quick instructions to get started with the tool.

## 📦 Quick Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd tai-evalgentcs-cli

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure .env
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

## 🔑 Getting an API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Create an account
3. Navigate to [API Keys](https://openrouter.ai/keys)
4. Create a new key
5. Add credit (minimum $15 recommended)
6. Copy the key to your `.env` file

## 🚀 Basic Usage

### Check Compliance

```bash
python main.py --check-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./reports
```

**Result:**
- `reports/UserServiceTest_bp_report.json` - Full report

### Improve Tests

```bash
python main.py --improve-best-practice \
  --original-test-set examples/UserServiceTest.java \
  --output-dir ./improved
```

**Result:**
- `improved/UserServiceTest_improved.java` - Improved code
- `improved/UserServiceTest_bp_report.json` - Full report
- `improved/UserServiceTest_improvement_summary.md` - Summary

## 📊 Interpreting Results

### Compliance Status

- **✔️** - Compliant
- **❌** - Non-compliant (see suggestions)
- **⚪** - Not applicable

### Scores

- **Method Compliance Score**: Per-method compliance (0-100%)
- **Overall Compliance Score**: Overall class compliance (0-100%)
- **Practice Compliance Score**: Per-practice compliance (0-100% or N/A)

## 🎯 Next Steps

1. Review the generated JSON report
2. Analyze non-compliant practices (❌)
3. Compare the original code with the improved version
4. Apply the improvements to your project
5. Run the tool again to verify improvements

## 💡 Tips

- Use `--verbose` for detailed logs
- Start with `--check-best-practice` to understand the current state
- Use `--improve-best-practice` when you want concrete suggestions
- Manually review the improved code before applying it

## 🆘 Common Issues

### Error: "OPENROUTER_API_KEY not found"
- Check if the `.env` file exists
- Confirm that the key is correctly configured

### Error: "Rate limit exceeded"
- Wait a few minutes
- Check if you have sufficient credit on OpenRouter
- Adjust `RATE_LIMIT_REQUESTS_PER_MINUTE` in `.env`

### Error: "Best practices file not found"
- Check if `data/best_practices.json` exists
- Run the command from the project's root directory

## 📚 Full Documentation

For detailed information, refer to:
- `README.md` - Full documentation
- `data/best_practices.json` - Definitions of the 25 practices
- `data/report-schema.json` - JSON report schema
