<p align="center">
  <img src="https://raw.githubusercontent.com/open-coder-ai/chock/main/docs/assets/logo.svg" alt="chock logo" width="110">
</p>

<h1 align="center">chock-claude-plugins</h1>

<p align="center"><strong>Blocks your Claude Code agent's wrong moves before they land.</strong></p>
<p align="center">Chock policies as installable Claude Code plugins — each says whether it enforces in your client or advises.</p>

<p align="center">

[![Generated-only](https://github.com/open-coder-ai/chock-claude-plugins/actions/workflows/generated-only.yml/badge.svg)](https://github.com/open-coder-ai/chock-claude-plugins/actions/workflows/generated-only.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Contribute upstream](https://img.shields.io/badge/contribute-chock--catalog-8957e5)](https://github.com/open-coder-ai/chock-catalog)

</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/open-coder-ai/chock/main/docs/assets/demo.gif" alt="Chock's demo: an agent runs a destructive command and a guard plugin denies it before it executes" width="760">
</p>

An agent you're running can already touch your shell, your git history, and your CI config.
You want it to move fast without being the reason a stray `rm -rf` or a force-push actually
happens. Telling it to be careful in a prompt is not a guarantee; a plugin that can refuse
the command is closer to one — and it should be honest about which of those two it is.

## Two ways to get these plugins

**This marketplace: no chock on the machine.** Each policy is its own plugin, republished
with every chock release. You need Python 3.11+ and git, and nothing else.

```bash
# Claude Code
/plugin marketplace add open-coder-ai/chock-claude-plugins
/plugin install block-destructive-commands@chock
```

The Claude plugin format is also read natively by GitHub Copilot CLI, VS Code, and Grok
Build, so this repository works there too.

**The builder: one plugin, needs chock.** Pick the policies you want and the client you run
at **<https://chock.sh/coding/builder/>**; it gives you one command that builds them into a
single plugin on your machine. That command needs `pip install chock`:

```bash
pip install chock
chock install --selection '<code>' --apply
```

`<code>` is the selection the builder shows you.

**Use one route for a given policy, never both.** Every copy of a plugin runs its own hook,
so a policy installed from both places runs twice. To switch a policy from one route to the
other, uninstall it first (`claude plugin uninstall <id>@chock`; to drop the marketplace
too, `claude plugin marketplace remove chock`).

### Builder links, one policy at a time

Each link opens the builder with that one policy preselected for Claude Code. The links pin
`chock-catalog` at commit `e885f918a335e20dfddb4fad0331d4d5b4c5eb43`; the builder lets you add
more policies and shows the catalog version it builds from.

| policy | in Claude Code | builder |
| :--- | :--- | :--- |
| [`agent-discipline`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/agent-discipline/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYWdlbnQtZGlzY2lwbGluZSIsInZlcnNpb24iOiIwLjAuMyIsInNoYTI1NiI6IjAzOGIxOWQ3MjZlZmMxMjVlZWFmMTMyMWFjNGZlYjcwYzdmZDFhMjA3ZGE4ZTg5NTNiZWQ2NWQ0YWNkZDg0NzIifV19) |
| [`block-curl-pipe-sh`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/block-curl-pipe-sh/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYmxvY2stY3VybC1waXBlLXNoIiwidmVyc2lvbiI6IjAuMS40Iiwic2hhMjU2IjoiMzRiOTYxYzQ4MjU4OGQwYjUxYzhkYzc2NTVlOTE1ZWE5OGM1YzQ3MDI3ZGNhMTE0ZjhhN2QxMjdmMzc2NjJmMiJ9XX0) |
| [`block-destructive-commands`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/block-destructive-commands/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYmxvY2stZGVzdHJ1Y3RpdmUtY29tbWFuZHMiLCJ2ZXJzaW9uIjoiMC4zLjAiLCJzaGEyNTYiOiI1NDFiNGQzMjc3ODg0MjQ4ZDMyMTYwMWQwNGNlMDE4MjUzN2MzMGUyNTk2ZGM3ODBjMDAxYWU1MzJiMWI5ZDUwIn1dfQ) |
| [`block-invisible-unicode`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/block-invisible-unicode/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYmxvY2staW52aXNpYmxlLXVuaWNvZGUiLCJ2ZXJzaW9uIjoiMC4xLjEiLCJzaGEyNTYiOiJiMTA4NDMxNTcwNmRjMjZlMzA5N2RkMWMxYTg5M2M3ODA0MTVmMTE2OGFiNWE5OTVjMTlhODk1ZjkzNjg4YzVhIn1dfQ) |
| [`block-no-verify`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/block-no-verify/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYmxvY2stbm8tdmVyaWZ5IiwidmVyc2lvbiI6IjAuNS4wIiwic2hhMjU2IjoiYTQwNmQ1MGU0Y2YzMGQ1NjQzMDg0MDgwYWQ0MjU5ZDM0MmYzZWRkMDcwMzY4ODhjNDdhODIxNGY2NjA5OTRjYyJ9XX0) |
| [`block-test-skips`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/block-test-skips/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYmxvY2stdGVzdC1za2lwcyIsInZlcnNpb24iOiIwLjEuMCIsInNoYTI1NiI6Ijg1MzVjNTJlZDA1NWIwODRiM2Q4NzBiMzM5NDQ4NzQxZTE4MzRmNmZkOTFhYjJkMzJlYWQxZDI2M2Y0NzU1NzQifV19) |
| [`block-unapproved-egress`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/block-unapproved-egress/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYmxvY2stdW5hcHByb3ZlZC1lZ3Jlc3MiLCJ2ZXJzaW9uIjoiMC4yLjQiLCJzaGEyNTYiOiJlNDg2ZmUzN2IxMjFjMjA1NDFmNzFjZWY2Y2I4NTYwNWZlMGEwNmVlZWI2ZTU2MzgzYzk4ZmZiMDBjMDA3ZTEwIn1dfQ) |
| [`block-unguarded-agent-spawn`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/block-unguarded-agent-spawn/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYmxvY2stdW5ndWFyZGVkLWFnZW50LXNwYXduIiwidmVyc2lvbiI6IjAuMi4wIiwic2hhMjU2IjoiZTQ1YzIxNTUxZjFmMWEyNDIyNzU2ODNhZmU5YWUwMDQ2Mjc3ZDhkNTdmNTM3MzQ0YWM3MTNmZmJmYmE0NjEzNyJ9XX0) |
| [`block-wildcard-agent-permissions`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/block-wildcard-agent-permissions/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiYmxvY2std2lsZGNhcmQtYWdlbnQtcGVybWlzc2lvbnMiLCJ2ZXJzaW9uIjoiMC4wLjEwIiwic2hhMjU2IjoiNmIzMTlkZjY4ZjAzYzkzNjI2YzY5NWQyOTg3MGMxNzk0NTZlZmJkZjRlZmIzMzAxMmJlOWZkMGVkOGEzOGVlZCJ9XX0) |
| [`chock-mise`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/chock-mise/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiY2hvY2stbWlzZSIsInZlcnNpb24iOiIwLjAuMyIsInNoYTI1NiI6IjFiMDcyYmQ1MTc0YWM4YTc1YmQ0NDRlZDEwMGQ0MWNkYjc2Y2MzOWYxZDY2Yzg2NmE3YzJkOWE3M2VlY2Y1MWYifV19) |
| [`code-safety`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/code-safety/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiY29kZS1zYWZldHkiLCJ2ZXJzaW9uIjoiMC4wLjQiLCJzaGEyNTYiOiI1MTA2Nzk1MTIzNWE5YWRkMzBmMmFmYTIwNzYyYzUzZmQzOTJiYTJkNTczODQ1OTcwYzI5YmQzMDI5NTFlYWUyIn1dfQ) |
| [`context-hygiene`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/context-hygiene/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiY29udGV4dC1oeWdpZW5lIiwidmVyc2lvbiI6IjAuMC4yIiwic2hhMjU2IjoiNDg5MmQyMTRjNjI4OTdiYjI4M2VmNTJmZjZlY2M4MDU2ZDY3MjEzNjMwZjYxN2MyMTIwNmRmNWQ1YjVlN2Q3NCJ9XX0) |
| [`firecrawl-fallback-only`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/firecrawl-fallback-only/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiZmlyZWNyYXdsLWZhbGxiYWNrLW9ubHkiLCJ2ZXJzaW9uIjoiMC4xLjEiLCJzaGEyNTYiOiJjMWZiM2Y0Y2QyNGRmYjA3MGJjMWRjZmEwZDU3ZDdlOTAxNzQ4MTkwOGJiNTQ4NTBjNTZkNTZkZmNjMDc5MDY0In1dfQ) |
| [`git-safety`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/git-safety/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiZ2l0LXNhZmV0eSIsInZlcnNpb24iOiIwLjAuNCIsInNoYTI1NiI6Ijc4NGMzYTE4OGM1YzQyYTg4NjA3MDMwMTk5ZGU0YjVhY2E5ZjNjMmY0NjI3OThlYjk2NjkxYzcxMzA3Y2E4NTgifV19) |
| [`guard-memory-writes`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/guard-memory-writes/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiZ3VhcmQtbWVtb3J5LXdyaXRlcyIsInZlcnNpb24iOiIwLjAuOSIsInNoYTI1NiI6ImU4OGZkNDZlYmJiN2E1YTY2Zjc3ZTY0YjdhZTY1ZTQwOTQ1YTRkMmE1N2RjMjVkNTNjMzFmNzNlNTc4MGNkN2IifV19) |
| [`injection-defense`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/injection-defense/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiaW5qZWN0aW9uLWRlZmVuc2UiLCJ2ZXJzaW9uIjoiMC4wLjQiLCJzaGEyNTYiOiI2NDM3Y2UyYTM2YTdjYjRhNjBmYjc4YzM5NzhhMzM2MmFhMzVjYzljZGZiOTNmODY3ZTU4NTg1MjdlNzYwOWMwIn1dfQ) |
| [`java-security`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/java-security/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoiamF2YS1zZWN1cml0eSIsInZlcnNpb24iOiIwLjcuMCIsInNoYTI1NiI6IjJiMWE4NTg4MTk0NmUxYmI2NTE1NzE4MzJjNGJlZDQ3ZjNmMjJlNjI1NTc1OWVkMjFkM2ExNzBkZWM5NzAwNTgifV19) |
| [`limit-diff-size`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/limit-diff-size/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoibGltaXQtZGlmZi1zaXplIiwidmVyc2lvbiI6IjAuMC4zIiwic2hhMjU2IjoiYTdlNWFkZDY2YTU3MDZhMDg4OTg0NzY2OTVmZTJjMzBjMDVlMDZlNGJmODBjMGI0YzY3MjJjZDI4OWU1OGFmNCJ9XX0) |
| [`memory-discipline`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/memory-discipline/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoibWVtb3J5LWRpc2NpcGxpbmUiLCJ2ZXJzaW9uIjoiMC4wLjUiLCJzaGEyNTYiOiIwZjdhNjY3YTA3ZThmNWI5Yzk2ZWFkNmY5NmRmN2EyZTllOTg5YzNjMGVjNzc2YWJmODNhMDdmZGRjNjk1NWY4In1dfQ) |
| [`no-a11y-regression`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/no-a11y-regression/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoibm8tYTExeS1yZWdyZXNzaW9uIiwidmVyc2lvbiI6IjEuMS4yIiwic2hhMjU2IjoiMjFjNDdjZmFlYThkOWY3ZDYxZTlmNGQ5ZDliMTI3YjczNzE1MzU2MTNhNTg4ZTFjNWU3NDQzNjAxM2QwYjFkYiJ9XX0) |
| [`pin-github-actions`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/pin-github-actions/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoicGluLWdpdGh1Yi1hY3Rpb25zIiwidmVyc2lvbiI6IjAuMC43Iiwic2hhMjU2IjoiMTY4ZDZlOTQ2MzI0OTMwOWFiZDQwMjJhZGMxNzZiOGQ5N2FiMWZkYjE2ZjRjYTU5NjdmNWM0Y2E4NTg1NjllYyJ9XX0) |
| [`protect-agent-config`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/protect-agent-config/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoicHJvdGVjdC1hZ2VudC1jb25maWciLCJ2ZXJzaW9uIjoiMC43LjEiLCJzaGEyNTYiOiIxOTY0NDU3NTM2NWYyNTVhNjEyMzQ1NDJjNjc2YjNiZGYwMjhiZmQyMGE3YzIwNTczYWMyM2QzMGI1OTA4N2ExIn1dfQ) |
| [`protect-ci-workflows`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/protect-ci-workflows/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoicHJvdGVjdC1jaS13b3JrZmxvd3MiLCJ2ZXJzaW9uIjoiMC4yLjYiLCJzaGEyNTYiOiIwZTUwY2U5NzhmYmE3OTlmM2RlNmViYTUyNGZkMjBiMWNlODZhZGQ5YzljMWY0YmQ2MTljYzk0ZmQ4YjNmMDM3In1dfQ) |
| [`protect-commit-privacy`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/protect-commit-privacy/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoicHJvdGVjdC1jb21taXQtcHJpdmFjeSIsInZlcnNpb24iOiIwLjIuNSIsInNoYTI1NiI6IjMzMTQyOTViYWUxYTRiNzVkNTAzZDk3N2M4NDQ5ZTg5OGE4MTU5MWM1Y2ExZTk4OTY4YzlmNzg5OTAyZmM3MDEifV19) |
| [`protect-main-branch`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/protect-main-branch/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoicHJvdGVjdC1tYWluLWJyYW5jaCIsInZlcnNpb24iOiIwLjAuMyIsInNoYTI1NiI6ImViYTE2NGQwOWMyMmI0NmY1YzJkMjY1NjYwN2Q3MzU5NmQzYjBjZTRjNzc4MTg3MzdlZmM1MjcyZDc4NzE5ZWUifV19) |
| [`protect-test-integrity`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/protect-test-integrity/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoicHJvdGVjdC10ZXN0LWludGVncml0eSIsInZlcnNpb24iOiIwLjAuMyIsInNoYTI1NiI6ImU1MzYwZDZlOTMyMDU0Y2I2ZTM3ZTc3ZWRhM2JlNmU4MWVkOTAwMGZmNTQxYjBiZGQzZjJlZTkyNTVkMmU5MmYifV19) |
| [`rtk-dangerous-actions-blocker`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/rtk-dangerous-actions-blocker/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoicnRrLWRhbmdlcm91cy1hY3Rpb25zLWJsb2NrZXIiLCJ2ZXJzaW9uIjoiMC4zLjAiLCJzaGEyNTYiOiIxNDkwOTc5NjZkMmM4YmRiMmUxNTdhNDRiM2Y4N2JhOTRlYjk1YjRhYzdmNzI0MjQwZTUyNTJkZDU2ZjQ4ZWIxIn1dfQ) |
| [`scan-secrets`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/scan-secrets/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoic2Nhbi1zZWNyZXRzIiwidmVyc2lvbiI6IjAuMS4yIiwic2hhMjU2IjoiODBjMjdiNmNlMmYxNDU3MWIxYzJhMWZhMjNlN2Y3MWUzMDVjYTNlMjFmNzYwYjM1NTc1MDlkZmQ0MzA1NjBkMCJ9XX0) |
| [`token-efficiency`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/token-efficiency/README.md) | advisory | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoidG9rZW4tZWZmaWNpZW5jeSIsInZlcnNpb24iOiIwLjEuMSIsInNoYTI1NiI6IjE5MDAzZmFmYWEyYTQ0ODM2ZGE1NDg2ZjlmNTI4YTY3YTc1YzQ0YjJiNDkyMmUyNjQ0NTJlNTkyOWI1YTFjNzYifV19) |
| [`verify-dependency-exists`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/verify-dependency-exists/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoidmVyaWZ5LWRlcGVuZGVuY3ktZXhpc3RzIiwidmVyc2lvbiI6IjAuMi4wIiwic2hhMjU2IjoiYTk4NjNmZjQ4ZTI0OWYwN2E2MGE1NmYyYjRjZWJhY2YyNGI3YzU0MTE3M2M5MDliZTg0ZjZmNjk5MTc4ODk1NSJ9XX0) |
| [`verify-mcp-allowlist`](https://github.com/open-coder-ai/chock-catalog/blob/main/docs/verify-mcp-allowlist/README.md) | enforces | [build with it](https://chock.sh/coding/builder/#s=eyJzY2hlbWEiOjIsImNsaWVudCI6ImNsYXVkZS1jb2RlIiwiYnVuZGxlIjp7InZlcnNpb24iOiIxLjAuMCJ9LCJjYXRhbG9nIjp7InNvdXJjZSI6Imh0dHBzOi8vZ2l0aHViLmNvbS9vcGVuLWNvZGVyLWFpL2Nob2NrLWNhdGFsb2ciLCJyZWYiOiJlODg1ZjkxOGEzMzVlMjBkZmRkYjRmYWQwMzMxZDRkNWI0YzVlYjQzIn0sInBvbGljaWVzIjpbeyJmcm9tIjoiY2F0YWxvZyIsImlkIjoidmVyaWZ5LW1jcC1hbGxvd2xpc3QiLCJ2ZXJzaW9uIjoiMC41LjMiLCJzaGEyNTYiOiIwNDIxNjg4OWE2MDEyYjJlNTgyMmRhYjgxZGY1ODYzNmEwN2I0ODdjMjBkMWZmYjgwMjNiNzBlMThiNGNlMWE0In1dfQ) |

## Generated from chock-catalog

Every file here is compiled from policy sources in
[chock-catalog](https://github.com/open-coder-ai/chock-catalog) by
[chock](https://github.com/open-coder-ai/chock). Pull requests against this repository are
closed automatically — open them against the catalog instead.

- **Generated only:** CI regenerates from the pinned catalog and fails on any difference.
- **Byte-identical guards:** each guard script is a verbatim copy of its policy's source in the
  catalog, and the hook adapter a verbatim copy of its framework source.
- **Best-effort, not a boundary:** guards are pattern-based filters; see
  [SECURITY.md](https://github.com/open-coder-ai/chock/blob/main/SECURITY.md).
- This README is hand-written, as are `SECURITY.md` and the workflows under `.github/`, so they
  sit outside the generated-only guarantee.

## Part of open-coder-ai

| | |
|---|---|
| [agentseam](https://github.com/open-coder-ai/agentseam) | the primitives — one handler API and a verified capability matrix across 16 agents |
| [chock](https://github.com/open-coder-ai/chock) | the compiler — one policy into git hooks, CI gates and native pre-tool hooks |
| [chock-catalog](https://github.com/open-coder-ai/chock-catalog) | the policies — 42, each labelled enforced or advisory, with replayed evals |
| [context-report](https://github.com/open-coder-ai/context-report) | the evidence — a signed report of whether an agent artifact actually works |
| [chock-threat-intel](https://github.com/open-coder-ai/chock-threat-intel) | the threat ledger the catalog's policies answer to |
| chock-{claude,cursor,copilot,codex}-plugins | the catalog, packaged for each agent's plugin format (generated) |
| chock-quickstart · chock-example | template repos: what `chock init` leaves behind, and a full adoption |

## License

Apache-2.0, same as the framework and the catalog.
