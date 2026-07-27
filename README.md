# AI Finder Kit Search Skill

Source-aware web search and readable page extraction for AI agents.

[Website](https://aifinderkit.com/search) · [API](https://api.aifinderkit.com/v1) · [中文说明](#中文说明)

The repository contains a dependency-free Agent Skill for Codex, Claude Code, and compatible skill runtimes. It supports three retrieval modes, strict/relaxed academic presets, aggregate and vertical search, domain filtering, safe page/document extraction, bounded map/crawl, multi-query evidence bundles, capability discovery, and a sanitized connection check.

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

Alternatively run `python scripts/aifinderkit_search.py configure` once. It reads
the key without echo and stores it outside the repository at
`~/.config/aifinderkit/credentials` with mode `0600`.

For Claude Code, replace `~/.codex/skills` with `~/.claude/skills`. Start a new agent session after installation so the Skill can be discovered.

## Commands

```bash
python scripts/aifinderkit_search.py search "query" --limit 10 --mode balanced
python scripts/aifinderkit_search.py search "query" --language zh --category news
python scripts/aifinderkit_search.py search "query" --include-domain github.com
python scripts/aifinderkit_search.py domains --domain academic --domain code
python scripts/aifinderkit_search.py search "multimodal learning" --preset academic-strict --mode deep
python scripts/aifinderkit_search.py batch --query "first" --query "second"
python scripts/aifinderkit_search.py fetch "https://example.com/page"
python scripts/aifinderkit_search.py map "https://example.com/docs" --max-links 30
python scripts/aifinderkit_search.py crawl "https://example.com/docs" --max-pages 5 --max-depth 1
python scripts/aifinderkit_search.py research "topic" --subquery "official evidence" --fetch-top 3
python scripts/aifinderkit_search.py research "graph neural network survey" --preset academic-strict --fetch-top 5
python scripts/aifinderkit_search.py meta
python scripts/aifinderkit_search.py doctor
```

The client uses only the Python standard library. See [`aifinderkit-search/SKILL.md`](aifinderkit-search/SKILL.md) for the agent workflow and [`references/api.md`](aifinderkit-search/references/api.md) for endpoint details.

## Access and security

- Request beta access at [aifinderkit.com/search](https://aifinderkit.com/search#apply).
- Keep keys in `AIFINDERKIT_API_KEY`; never commit them or place them in prompts.
- Search-only beta keys do not grant access to model endpoints.
- The service pins a validated public IP at connection time, rechecks redirects, ignores environment proxies, and rejects private, loopback, link-local, multicast, and reserved targets.
- PDF and Office extraction enforce download, archive, page, concurrency, and time limits. Map/crawl is static HTML, same-host, depth two and eight pages maximum.

## 中文说明

这是面向 Codex、Claude Code 和兼容 Skills 运行时的网页搜索 Skill。它提供三种检索模式、严格/宽松学术预设、聚合及垂直搜索、域名过滤、HTML/PDF/Office/GitHub 提取、受限 Map/Crawl、多子问题证据矩阵与引用工作流。学术模式支持 DOI/作者/年份和合法开放 PDF 元数据。Skill 不包含任何密钥，客户端只使用 Python 标准库。

安装时将仓库中的 `aifinderkit-search` 目录复制到 `~/.codex/skills/` 或 `~/.claude/skills/`，设置 `AIFINDERKIT_API_KEY` 后运行 `doctor` 验证即可。搜索 Key 可在[产品页面](https://aifinderkit.com/search#apply)申请。

## License

[MIT](LICENSE)
