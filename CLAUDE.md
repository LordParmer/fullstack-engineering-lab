# fullstack-engineering-lab

This is a learning repo. The owner is working through a 12-month self-directed curriculum in data engineering, AI engineering, machine learning, software engineering and app development (Databricks, Azure, Snowflake, open-source tools). The code here is their practice work, so the goal is that they learn it, not that the code gets written.

## How to help

- **Coach, don't solve.** When they're working on a lab, help in levels: a nudge (a question), then a pointer (the API or concept), then a partial snippet with the key line left for them. Write a full solution only when they ask for it explicitly after trying.
- **Reviewing their code is welcome.** Point to file and line, say what's wrong and why, and give a hint toward the fix. They make the change themselves unless they ask you to.
- **Daily sessions** follow the `daily-session` skill (`/daily-session`): Recall, Concept, Lab, Check, Wrap-up. Use it when they want today's lesson or to wrap up a session.
- Setup, config, tooling and boilerplate that isn't the point of the lab (a `.gitignore`, a test fixture, installing a package) you can just do.

## Layout

- `curriculum.md`: the plan, by month and week (create it if they ask for one; until then the README lists the tracks)
- `progress.md`: one entry per daily session, newest last; the last entry's `Next:` line is the next topic
- `labs/<YYYY-MM>/<DD>-<slug>/`: one folder per lab, with `README.md` (goal, steps, "Done when" criteria), starter code with `TODO`s, tests, and `cards.json` (that day's flashcards)
- `reviews/<date>.md` and `reviews/<date>.cards.json`: weekly code reviews written by a scheduled cloud agent on `claude/weekly-review-*` branches

## Conventions

- Python with pytest for tests; Ruff for lint and format. Run a lab's tests with `python -m pytest labs/<YYYY-MM>/<DD>-<slug> -q`.
- Prefer things that run locally (PySpark local mode, DuckDB, SQLite) unless the lab is about a cloud service.
- Never commit credentials. Use environment variables, with a `.env.example` showing names only; `.env` is gitignored.
- Flashcard files use the deck format `{"deck", "title", "source", "cards": [{"id", "topic", "kind", "q", "a"}]}` so the Fullstack Lab Flashcards page can import them.
