# habari-mcp
<!-- mcp-name: io.github.gabrielmahia/habari-mcp -->

## Why This Exists

Kenya publishes gazette notices, tenders, parliamentary activity and open data continuously, but the volume makes it effectively invisible. Accountability depends on being able to find the one notice that matters, not on everything being technically public.

## Install

```bash
pip install habari-mcp
```

## Tools (5)

- **`gazette_search`** —   
  <sub>args: search_type, date_range</sub>
- **`tender_search_guide`** —   
  <sub>args: sector, county</sub>
- **`open_data_guide`** —   
  <sub>args: data_type</sub>
- **`parliament_tracker`** —   
  <sub>args: query_type</sub>
- **`citizen_feedback_channels`** —   
  <sub>args: issue_type</sub>

## Example

```python
from habari_mcp.server import gazette_guide

result = gazette_guide()
# what the Gazette publishes, how to search, why it matters
```

## Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "habari-mcp": {
      "command": "python",
      "args": ["-m", "habari_mcp.server"]
    }
  }
}
```

## Data & Disclaimers

Pointers to official sources rather than a live mirror. For legal effect, always read the notice in the Kenya Gazette itself.

Every tool response carries a `source` field. Responses labelled `DEMO` are
illustrative reference data, not a live feed — verify against the authority
named in the response before acting on it.

## Part of the East Africa Coordination Stack

This MCP server is part of the Kenya coordination infrastructure.
Connect it to [`africa-coord-bus`](https://github.com/gabrielmahia/africa-coord-bus) —
the coordination event bus that routes signals between domains automatically.

```bash
pip install africa-coord-bus
```

All servers: [pypi.org/user/gmahia](https://pypi.org/user/gmahia/)
Live demo: [coord-cascade-demo](https://github.com/gabrielmahia/coord-cascade-demo)

## IP & Collaboration

MIT licensed. Feedback via GitHub Issues only — pull requests are not accepted. Demo data is labeled DEMO and is not suitable for operational decisions. Full policy: [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md). Security reports: see [SECURITY.md](SECURITY.md).

<!-- interconnect:v1 -->
## Part of the East Africa coordination stack

- **Install & run:** `pip install reli-cli && reli list` — the MCP servers on the [official MCP Registry](https://registry.modelcontextprotocol.io) under `io.github.gabrielmahia`
- **Evaluate any model on Swahili agent tasks:** [kipimo](https://github.com/gabrielmahia/kipimo) · [dataset](https://huggingface.co/datasets/gmahia/kipimo) · [leaderboard](https://huggingface.co/spaces/gmahia/kipimo-leaderboard)
- **Coordinate across servers:** [africa-coord-bus](https://pypi.org/project/africa-coord-bus/) — offline-first event bus with a built-in Kenya routing table
- **Datasets:** [huggingface.co/gmahia](https://huggingface.co/gmahia) · **Docs hub:** [nairobi-stack](https://github.com/gabrielmahia/nairobi-stack)

Model-agnostic by design: closed APIs, open-weight models, and small distilled models are all first-class citizens.
<!-- /interconnect:v1 -->
