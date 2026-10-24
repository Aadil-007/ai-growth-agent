# AI Growth Agent

An agent that collects trusted AI news every day, filters what matters, explains it simply,
and (in later phases) drafts LinkedIn posts in my own voice, for me to review before posting.

**Why:** the UAE has some of the world's highest AI adoption, but few people have received AI training.
This project helps working professionals stay updated without drowning in news.

## Status
- [x] Phase 1: Reporter (RSS collector, SQLite storage, de-duplication, tests, daily schedule)
- [ ] Phase 2: Analyst (summaries and ranking with the Claude API)
- [ ] Phase 3: Writer and human approval (Telegram)
- [ ] Phase 4: Docker, logging, evaluation set

## Architecture
```
sources.yaml -> collectors (RSS) -> dedupe -> SQLite -> [analyst] -> [writer] -> [human approval]
```

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q
PYTHONPATH=src python -m ai_growth_agent.main        # Windows PowerShell: $env:PYTHONPATH="src"; python -m ai_growth_agent.main
```

## Adding a source
Edit `config/sources.yaml`. No code changes needed.

## Author
Aadil K. | GitHub: https://github.com/Aadil-007 | LinkedIn: https://linkedin.com/in/aadil-kamarudheen-93b123224
