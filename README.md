 # statement-parser-service

 Finance-specific block that turns page text from any bank/brokerage statement into validated `Account` and `Transaction` objects from the `data-models` package.

 ## Environment Variables
 - `PARSER_BACKEND`: selects the LLM adapter. Options:
   - `stub` (default): uses a fixed stub response for offline testing.
   - `gpt4`: uses the `OpenAIAdapter` (requires `OPENAI_API_KEY`).
 - `OPENAI_API_KEY`: required if `PARSER_BACKEND=gpt4`.

 ## Installation
 ```bash
 pip install pydantic python-dateutil openai data-models
 ```

 ## Usage
 ```python
 from models.parsed_input import ParsedInput, Page
 from service.core import parse_statement

 # Build input
 input_data = ParsedInput(
     document_id="doc123",
     pages=[Page(number=1, text="...statement text...")]
 )

 # Parse statement
 result = parse_statement(input_data)
 print(result.accounts, result.transactions)
 ```

 ## Testing
 Run all tests offline (uses `StubAdapter` by default):
 ```bash
 pytest -q
 ```

 ## Publishing
 After CI is green and version is set in `utility_contract.json`:
 ```bash
 pb-registry publish utility_contract.json
 ```