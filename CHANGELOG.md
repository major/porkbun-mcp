# Changelog

All notable changes to this project will be documented in this file.

This project uses [Semantic Versioning](https://semver.org/) and [Conventional Commits](https://www.conventionalcommits.org/).

## v0.1.3 (2026-01-19)

### Fix

- **ci**: remove broken plugin config from Claude Code review

## v0.1.2 (2026-01-19)

### Fix

- **ci**: grant write permissions for Claude Code review comments

## v0.1.1 (2026-01-19)

### Fix

- add claude.md symlink

## v0.1.0 (2026-01-19)

### Feat

- add automated release pipeline with commitizen and MCP registry
- add readOnlyHint annotations to all resources
- add idempotentHint annotations to create/edit tools
- add destructiveHint annotations to delete tools
- add readOnlyHint annotations to read-only tools
- add typed lifespan context (AppContext)
- enhance server instructions with workflow guidance
- add MCP prompt templates for common DNS workflows
- initial porkbun-mcp implementation

### Fix

- use quoted FastMCP annotations for Python 3.13 compatibility
- **ci**: pass CODECOV_TOKEN to codecov action

### Refactor

- remove --get-muddy write protection
