# Changelog

All notable changes to TAI-EvalGenTCS CLI will be documented in this file.

## [1.6.0] - 2026-02-12

### Fixed
- **CRITICAL**: Fixed massive compliance variance between check and improve modes
- **CRITICAL**: Both modes now use identical prompts (full practice descriptions) for consistent evaluation
- Compliance scores are now consistent across modes (< 2% variance with recommended settings)

### Added
- **Explicit scoring instructions** in prompts to reduce LLM interpretation variance
- **COMPLIANCE_VARIANCE.md** comprehensive guide explaining variance causes and solutions
- Conservative evaluation guidance: "when in doubt between ✔️ and ❌, choose ❌"
- Definitive evaluation criteria enforcement

### Changed
- `generate_llm_prompt_section()` now uses full descriptions in BOTH check and improve modes
- Removed compact prompt generation from check mode (was causing inconsistent interpretations)
- Enhanced prompt with strict evaluation rules

### Documentation
- Clarified that compliance is ALWAYS measured on the original/input code, not improved code
- Added model consistency comparison table
- Added FAQ section on compliance variance
- Added testing consistency guide

## [1.5.0] - 2026-02-11

### Added
- **JSON repair mechanism** for truncated LLM responses with unterminated strings
- **Large test file detection** with automatic warnings (> 200 lines or > 10,000 chars)
- **`_repair_truncated_json()` method** to find and truncate to last valid JSON structure
- **LARGE_TEST_FILES.md** comprehensive guide for handling large test files
- Better logging for test file size (lines and characters)

### Changed
- Enhanced error handling for "Unterminated string" and "Expecting property name" JSON errors
- Updated `.env.example` with guidance for different test file sizes
- Improved JSON parsing with multi-stage fallback: repair → extract → fail

### Fixed
- JSON parsing errors when analyzing large test files (> 200 lines)
- Truncated JSON responses causing "Unterminated string starting at" errors
- Better handling of models with smaller output token limits (e.g., Claude Haiku: ~4096 tokens)

### Documentation
- Added model comparison table with max output tokens
- Added test file size guidelines
- Added troubleshooting section for large files

## [1.4.0] - 2026-02-11

### Fixed
- **Critical**: Fixed repeated/duplicated code in improved test files
- **Critical**: Fixed commented-out code in improved test files
- **Critical**: Fixed incorrect class naming (now preserves original class name)
- Fixed TestImproverAgent to use only the first method's suggested_code (which contains the complete improved class)
- Added `_preserve_original_class_name()` method to ensure class name matches filename
- Added `_clean_suggested_code()` method to remove code block markers

### Changed
- **Enhanced LLM prompt** to explicitly request complete improved class only in first method's suggested_code
- Updated prompt to emphasize: preserve original class name, no commented code, no repetition
- Improved TestImproverAgent with better code extraction and cleaning logic
- Added regex-based class name replacement to ensure consistency

### Added
- `_extract_method_only()` to detect and skip full class definitions in method suggestions
- Better validation of suggested code structure
- More detailed logging for code generation process

## [1.3.0] - 2026-02-11

### Added
- **Seed parameter support** (`LLM_SEED`) for deterministic sampling with supported models
- **Consistency checker utility** (`check_consistency.py`) to analyze variance across multiple runs
- **LLM connection diagnostic script** (`test_llm_connection.py`) to test model connectivity and functionality
- **Comprehensive error logging** for empty LLM responses with refusal reason detection
- **DETERMINISTIC_RESULTS.md** documentation on achieving consistent results
- **TROUBLESHOOTING.md** guide for common issues and solutions

### Changed
- **Default temperature** changed from `0.1` to `0.0` for maximum determinism
- **Enhanced error handling** in `llm_client.py` to detect and report empty responses
- **Improved JSON parsing** with checks for empty responses before and after sanitization
- Updated `.env.example` with determinism recommendations and seed parameter

### Fixed
- Better detection and reporting of empty LLM responses ("Expecting value: line 1 column 1" error)
- Added explicit checks for `None` or empty content from LLM
- Added logging for finish reason and refusal messages

### Performance
- Improved consistency: With `LLM_TEMPERATURE=0.0` and `LLM_SEED=42`, variance reduced to < 5% (Excellent consistency)

## [1.2.0] - 2026-02-11

### Fixed
- **Critical**: Fixed JSON schema validation error with OpenAI models - added `original_code` and `improved_code` to required fields array
- **Critical**: Fixed JSON syntax error in `best_practices.json` - replaced invalid escape sequences `\'` with `'`
- Fixed incomplete output generation in improve mode by enhancing `TestImproverAgent` to handle multiple JSON structures
- Fixed syntax error in `test_analyzer_agent.py` (unterminated string literal)
- Fixed method name mismatch in `main.py` (`improve_test_suite` → `improve_best_practices`)

### Added
- **Timestamp-based output subdirectories**: Each execution creates a `testset_YYYY-MM-DD_HH-MM-SS` subdirectory to prevent overwriting previous reports
- Optimized LLM prompts with compact format for check mode and full format for improve mode
- Enhanced error handling and fallback mechanisms for LLM responses
- `LLM_TIMEOUT` configuration option in `.env`
- Comprehensive LLM model recommendations in documentation
- Performance comparison table in documentation

### Changed
- Updated `PracticeManager` to generate compact vs full prompts based on mode
- Improved `TestImproverAgent` to gracefully handle flat JSON structures from non-compliant models
- Enhanced system prompts with stricter JSON schema requirements
- Updated default recommended model from `moonshotai/kimi-k2-0905` to `openai/gpt-4.1-mini`
- Improved `orchestrator.py` to create timestamped subdirectories for all outputs

### Performance
- Reduced analysis time from 6-7 minutes to 20-30 seconds when using recommended models (21x speedup)
- Reduced token usage by ~40% in check mode with compact prompts
- Improved JSON schema compliance for faster LLM responses

## [1.1.0] - 2026-02-11

### Added
- **Improved Logging System**
  - Added timestamps to all log messages (format: `YYYY-MM-DD HH:MM:SS`)
  - Added `--log-level` CLI argument to set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Added `LOG_LEVEL` configuration in `.env` file
  - Log level priority: CLI `--log-level` > CLI `--verbose` > `.env` LOG_LEVEL

- **Enhanced JSON Parsing**
  - Added robust JSON sanitization to remove code block delimiters (```) from LLM responses
  - Added JSON extraction from malformed responses
  - Added fallback mechanism for models that don't support strict JSON schema mode
  - Added automatic retry without strict schema when initial request fails

- **Better Error Handling**
  - Improved error messages with detailed logging
  - Added debug logging for response content when JSON parsing fails
  - Added graceful degradation for unsupported model features

### Changed
- **Complete English Translation**
  - Translated all documentation (README.md, QUICK_START.md) to American English
  - Translated all code comments and docstrings to English
  - Translated all user-facing messages and prompts to English
  - Translated `best_practices.json` content to English
  - Updated system prompts for LLM to English

- **Logging Format**
  - Changed default logging format to include timestamps
  - Improved log message clarity and consistency

### Fixed
- **JSON Parsing Error with Certain LLM Models**
  - Fixed issue with models like `moonshotai/kimi-k2-0905` that don't properly support strict JSON schema mode
  - Fixed "Unterminated string" errors by implementing robust JSON extraction
  - Fixed code block delimiter issues in LLM responses

### Technical Details

#### JSON Sanitization
The new `_sanitize_json_response()` method removes:
- Leading ````json` or ``` ` markers
- Trailing ``` ` markers
- Whitespace around JSON content

#### JSON Extraction
The new `_extract_json_from_text()` method:
- Searches for balanced braces `{}` in the response
- Extracts potential JSON objects
- Validates extracted content before returning

#### Fallback Mechanism
When strict JSON schema mode fails:
1. Log the error with details
2. Retry with basic JSON mode (`{"type": "json_object"}`)
3. Apply sanitization and extraction to the response

## [1.0.0] - 2026-02-11

### Initial Release
- Multi-agent architecture for test evaluation and improvement
- Support for 25 best practices (14 Common Sense + 11 Literature Supported)
- Integration with OpenRouter API
- Two operation modes: `--check-best-practice` and `--improve-best-practice`
- JSON report generation
- Rate limiting and retry logic
- Configurable via `.env` file
