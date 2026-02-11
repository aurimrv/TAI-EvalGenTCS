# Changelog

All notable changes to TAI-EvalGenTCS CLI will be documented in this file.

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
