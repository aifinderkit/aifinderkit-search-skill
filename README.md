# AI Finder Kit Search Skill

Source-aware web search and readable page extraction for AI agents.

[Website](https://aifinderkit.com/search) · [API](https://api.aifinderkit.com/v1) · [中文说明](#中文说明)

The repository contains a dependency-free Agent Skill for Codex, Claude Code, and compatible skill runtimes. It supports aggregate search, batch queries, safe page extraction, research bundles, capability discovery, and a sanitized connection check.

## Install

Python 3.10 or newer is required. Clone the repository, then copy the `aifinderkit-search` directory into your agent's Skills directory.

### Codex

```bash
git clone https://github.com/aifinderkit/aifinderkit-search-skill.git
mkdir -p ~/.codex/skills
cp -R aifinderkit-search-skill/aifinderkit-search ~/.codex/skills/
```

### Claude Code

```bash
git clone https://github.com/aifinderkit/aifinderkit-search-skill.git
mkdir -p ~/.claude/skills
cp -R aifinderkit-search-skill/aifinderkit-search ~/.claude/skills/
```

Configure a separately issued search key. No credentials are included in the repository.

```bash
export AIFINDERKIT_API_KEY="your-search-key"
python ~/.codex/skills/aifinderkit-search/scripts/aifinderkit_search.py doctor
```

For Claude Code, replace `~/.codex/skills` with `~/.claude/skills`. Start a new agent session after installation so the Skill can be discovered.

## Commands

```bash
python scripts/aifinderkit_search.py search "query" --limit 10 --mode balanced
python scripts/aifinderkit_search.py batch --query "first" --query "second"
python scripts/aifinderkit_search.py fetch "https://example.com/page"
python scripts/aifinderkit_search.py research "topic" --fetch-top 3
python scripts/aifinderkit_search.py meta
python scripts/aifinderkit_search.py doctor
```

The client uses only the Python standard library. See [`aifinderkit-search/SKILL.md`](aifinderkit-search/SKILL.md) for the agent workflow and [`references/api.md`](aifinderkit-search/references/api.md) for endpoint details.

## Access and security

- Request beta access at [aifinderkit.com/search](https://aifinderkit.com/search#apply).
- Keep keys in `AIFINDERKIT_API_KEY`; never commit them or place them in prompts.
- Search-only beta keys do not grant access to model endpoints.
- The `fetch` endpoint rejects private, loopback, and reserved network targets.

## 中文说明

这是面向 Codex、Claude Code 和兼容 Skills 运行时的网页搜索 Skill。它提供聚合搜索、批量查询、安全正文提取和研究资料包，不包含任何密钥，也不依赖第三方 Python 包。

安装时将仓库中的 `aifinderkit-search` 目录复制到 `~/.codex/skills/` 或 `~/.claude/skills/`，设置 `AIFINDERKIT_API_KEY` 后运行 `doctor` 验证即可。搜索 Key 可在[产品页面](https://aifinderkit.com/search#apply)申请。

## License

[MIT](LICENSE)
