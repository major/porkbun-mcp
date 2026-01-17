# GitHub Copilot Code Review Instructions

## Review Philosophy: Invert, Always Invert

Apply Charlie Munger's inversion principle: Instead of asking "Is this code good?", ask **"What would make this code fail?"**

Focus on preventing failure rather than achieving brilliance:
- What edge cases would break this?
- What would cause this to fail in production?
- What would make this unmaintainable in 6 months?
- What security holes does this open?

When something could fail, explain **HOW** it would fail and suggest the prevention.

---

## Project Context: porkbun-mcp

MCP (Model Context Protocol) server for Porkbun DNS API. Python 3.14+, FastMCP 2.14+.

### Tech Stack
- **MCP Framework**: FastMCP 2.14+
- **DNS Client**: oinker (async-first)
- **Type checking**: ty
- **Linting/Formatting**: ruff
- **Testing**: pytest + pytest-asyncio
- **Package manager**: uv

### Key Design Decisions
- `--get-muddy` flag enables write operations (read-only by default)
- MCP Resources for read-only data browsing
- Unified tools (one `dns_create` with `record_type` param)
- Strict output schemas via Pydantic response models

---

## Inversion Checklists by File Type

### Source Code (`src/porkbun_mcp/**/*.py`)

**MCP server failures to prevent:**
- Tools not returning proper Pydantic response models
- Missing `--get-muddy` guard on write operations
- Not handling oinker exceptions (must convert to `ToolError`)
- Blocking calls in async tool functions
- Missing type hints or docstrings

**FastMCP patterns to enforce:**
- Tools use `@mcp.tool()` decorator with proper type hints
- Resources use `@mcp.resource()` decorator
- Context accessed via `ctx.request_context.lifespan_context`
- Errors raised as `ToolError` or `ResourceError`

### Tools (`src/porkbun_mcp/tools/**/*.py`)

**What would cause tools to fail?**
- Write tools not checking `settings.get_muddy`
- Not using oinker's `create_record()` factory for DNS creation
- Exceptions not mapped to `ToolError` via `handle_oinker_error()`
- Missing `Annotated[type, Field(...)]` for parameter descriptions
- Return type not matching declared Pydantic model

### Resources (`src/porkbun_mcp/resources/**/*.py`)

**What would cause resources to fail?**
- Resources attempting write operations (they're read-only!)
- Resource URI patterns not matching expected format
- Not handling missing domains gracefully

### Configuration (`src/porkbun_mcp/config.py`)

**What would cause config to fail?**
- Missing `env_prefix="PORKBUN_"` (env vars won't load)
- Credentials logged or exposed in error messages
- `get_muddy` defaulting to `True` (should be `False` for safety)

### Error Handling (`src/porkbun_mcp/errors.py`)

**What would make error handling fail?**
- Not handling all oinker exception types
- Generic `except` clauses hiding real errors
- Error messages too vague for debugging
- Not preserving exception chains (use `from e`)

### Tests (`tests/**/*.py`)

**What would make these tests meaningless?**
- Tests that pass but don't assert meaningful outcomes
- Mocks without `spec=` (won't catch attribute errors)
- Not testing the `--get-muddy` guard on write tools
- Missing edge cases: empty responses, network errors, invalid data
- Not testing both success and failure paths

### Project Config (`pyproject.toml`)

**What would break the build/test cycle?**
- Missing dev dependencies
- Incompatible version constraints
- pytest-asyncio missing `asyncio_mode = "auto"`
- Coverage excluding important paths

---

## What NOT to Review

Don't nitpick these—automated tools handle them:
- **Style issues**: ruff handles formatting and linting
- **Type errors**: ty handles type checking
- **Import order**: ruff's isort handles this

Focus review time on logic, architecture, and failure modes.
