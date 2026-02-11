# Changelog

All notable changes to TAI-EvalGenTCS CLI will be documented in this file.

## [1.1.0] - 2025-02-12

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

## [1.0.0] - 2025-02-11

### Initial Release
- Multi-agent architecture for test evaluation and improvement
- Support for 25 best practices (14 Common Sense + 11 Literature Supported)
- Integration with OpenRouter API
- Two operation modes: `--check-best-practice` and `--improve-best-practice`
- JSON report generation
- Rate limiting and retry logic
- Configurable via `.env` file
