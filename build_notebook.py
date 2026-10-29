"""Generate toolkit_guide.ipynb from guide_content.py.

Run:  python build_notebook.py
"""

from pathlib import Path

import nbformat as nbf

import guide_content as gc

HERE = Path(__file__).parent
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip()))


def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip()))


def md_table(rows, headers):
    escape = lambda s: str(s).replace("|", "\\|")
    lines = ["| " + " | ".join(headers) + " |", "|" + " --- |" * len(headers)]
    lines += ["| " + " | ".join(escape(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def md_bullets(items):
    return "\n".join(f"- **{name}.** {text}" for name, text in items)


# ---------------------------------------------------------------- intro
md(f"""
# {gc.TITLE}: {gc.SUBTITLE}

{gc.INTRO}

Run the cells from top to bottom (**Run All**). The demos use simulated data, so no API keys
or database are needed.

**Packages used:** numpy, pandas, polars, pyarrow, matplotlib, plotly, scikit-learn.
Install them in your project with `uv add numpy pandas polars pyarrow matplotlib plotly scikit-learn ipykernel`.
DuckDB is optional (`uv add duckdb`).
""")

code("""
import sys
import warnings

import numpy as np
import pandas as pd

# Which Python is this notebook using? It should point inside your project's .venv
print(sys.executable)
""")

# ---------------------------------------------------------------- VS Code
md(f"""
## 1. VS Code

{gc.VSCODE_INTRO}

### Extensions to install first
{md_table(gc.EXTENSIONS, ["Extension", "What it adds"])}

### Features worth learning early
{md_bullets(gc.FEATURES)}

### Handy shortcuts
{md_table(gc.SHORTCUTS, ["Action", "Mac", "Windows"])}

### Gotchas
{md_bullets(gc.VSCODE_GOTCHAS)}

The cell above printed `sys.executable`: the quickest way to check the "wrong interpreter" gotcha.
""")

# ---------------------------------------------------------------- libraries
by_cat = {}
for cat, name, used, gotcha, trending in gc.LIBRARIES:
    by_cat.setdefault(cat, []).append((name + (" (trending)" if trending else ""), used, gotcha))
lib_tables = "\n\n".join(f"### {cat}\n{md_table(rows, ['Library', 'Used for', 'Gotcha'])}"
                         for cat, rows in by_cat.items())
md(f"""
## 2. Data analysis libraries

{gc.LIBRARIES_INTRO}

{lib_tables}
""")

md("### Gotcha demos\n\n**NumPy: never compare floats with `==`**")
code("""
print(0.1 + 0.2 == 0.3)            # False: floats are stored in binary, not exactly
print(np.isclose(0.1 + 0.2, 0.3))  # True: compares within a small tolerance
""")

md("**pandas: chained assignment does not change the DataFrame**")
code("""
df = pd.DataFrame({"x": [-1, 2, 3], "y": [0, 0, 0]})

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    df[df.x > 0]["y"] = 1          # writes to a temporary copy
print("chained:\\n", df)

df.loc[df.x > 0, "y"] = 1          # the right way: one .loc call
print("\\nwith .loc:\\n", df)
""")

md("**Polars: same job, different syntax, and lazy queries need `.collect()`**")
code("""
import polars as pl

pdf = pl.DataFrame({"symbol": ["AAPL", "AAPL", "NVDA"], "price": [180.0, 182.5, 120.0]})

# Eager: runs immediately
print(pdf.group_by("symbol").agg(pl.col("price").mean()))

# Lazy: builds a plan, nothing runs until .collect()
plan = pdf.lazy().filter(pl.col("price") > 150)
print(type(plan))
print(plan.collect())
""")

md("**DuckDB: SQL directly on a pandas DataFrame** (skipped if DuckDB is not installed)")
code("""
try:
    import duckdb
    quotes = pd.DataFrame({"symbol": ["AAPL", "NVDA", "AAPL"], "price": [180, 120, 182]})
    print(duckdb.sql("SELECT symbol, AVG(price) AS avg_price FROM quotes GROUP BY symbol").df())
except ImportError:
    print("DuckDB not installed. Install it with: uv add duckdb")
""")

md("**CSV loses types, Parquet keeps them**")
code("""
df = pd.DataFrame({"ts": pd.date_range("2026-01-01", periods=3), "price": [1.0, 2.0, 3.0]})
df.to_csv("demo.csv", index=False)
df.to_parquet("demo.parquet")

print("from CSV:    ", pd.read_csv("demo.csv").dtypes["ts"])          # object (text)
print("from Parquet:", pd.read_parquet("demo.parquet").dtypes["ts"])  # datetime64
""")

md("**scikit-learn: for time series, never shuffle the split**")
code("""
from sklearn.model_selection import KFold, TimeSeriesSplit

days = np.arange(10)
shuffled = next(KFold(n_splits=5, shuffle=True, random_state=0).split(days))
ordered = next(TimeSeriesSplit(n_splits=4).split(days))

print("Shuffled  train:", shuffled[0], "test:", shuffled[1])  # trains on the future
print("TimeSeries train:", ordered[0], "test:", ordered[1])   # only the past predicts the future
""")

md("**Matplotlib: use the `fig, ax` style consistently**")
code("""
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot([1, 2, 3, 4], [10, 12, 9, 14])
ax.set_title("fig, ax style")
ax.set_xlabel("Day")
ax.set_ylabel("Price")
plt.show()
""")

# ---------------------------------------------------------------- workflow
md("""
## 3. How they work together

A typical analysis moves through the same stages: get data, clean it, explore it, model it,
show it. Here step 1 simulates prices instead of reading them from MySQL; the commented line
shows the real version.
""")
code("""
import plotly.express as px
from sklearn.linear_model import LinearRegression

# 1. Get data (simulated). With a database it would be:
# df = pd.read_sql("SELECT symbol, ts, price FROM quotes", engine, parse_dates=["ts"])
rng = np.random.default_rng(7)
dates = pd.bdate_range("2025-01-01", periods=250)
df = pd.concat([
    pd.DataFrame({"symbol": s, "ts": dates, "price": p0 * np.exp(np.cumsum(rng.normal(0.0005, 0.018, 250)))})
    for s, p0 in {"AAPL": 180, "NVDA": 120, "MSFT": 400}.items()
], ignore_index=True)

# 2. Clean and reshape with pandas
df = df.dropna().sort_values("ts")
df["return"] = df.groupby("symbol")["price"].pct_change()

# 3. Explore: summary stats and an interactive chart
display(df.groupby("symbol")["return"].describe().round(4))
px.line(df, x="ts", y="price", color="symbol", title="Simulated prices").show()

# 4. Model with scikit-learn (NumPy arrays underneath)
aapl = df[df.symbol == "AAPL"].dropna()
X = np.arange(len(aapl)).reshape(-1, 1)
model = LinearRegression().fit(X, aapl["price"])
print("AAPL trend per trading day:", round(model.coef_[0], 3))

# 5. Save for later in a fast, typed format
df.to_parquet("prices.parquet")
""")

# ---------------------------------------------------------------- uv
cmd_rows = [(task, f"`{v}`", f"`{u}`") for task, v, u in gc.VENV_UV_COMMANDS]
md(f"""
## 4. venv vs uv

{gc.UV_INTRO}

{md_table(gc.VENV_UV_COMPARE, ["", "venv + pip", "uv"])}

### The same tasks, side by side
{md_table(cmd_rows, ["Task", "venv + pip", "uv"])}

Install uv on a Mac or Linux:

```bash
{gc.UV_INSTALL}
```

### Gotchas
{md_bullets(gc.UV_GOTCHAS)}
""")
code("""
# Is this notebook running inside a virtual environment?
print("Environment:", sys.prefix)
print("Inside a venv:", sys.prefix != sys.base_prefix)
""")

# ---------------------------------------------------------------- Git
md(f"""
## 5. Git and GitHub

{gc.GIT_INTRO}

![Git workflow](assets/git_workflow.png)

Nothing reaches GitHub until you push, and nothing from GitHub reaches your computer until you pull.

### Core ideas
{md_table(gc.GIT_TERMS, ["Term", "Meaning"])}

### The daily workflow
```bash
{gc.GIT_WORKFLOW.strip()}
```

### Gotchas
{md_bullets(gc.GIT_GOTCHAS)}
""")

md(f"""
## 6. Getting the most out of GitHub

GitHub is also the best free classroom for programming: millions of real projects are open
to read, run, question and improve.

### For learning
{md_bullets(gc.GITHUB_LEARNING)}

### For your own projects
{md_bullets(gc.GITHUB_OWN)}

### Working with others
{md_bullets(gc.GITHUB_OTHERS)}
""")

steps = "\n".join(f"{i}. **{name}.** {text}" for i, (name, text) in enumerate(gc.LEARNING_ORDER, 1))
md(f"""
## 7. A suggested order

Each step uses the one before it, and the projects give each skill a real job to do.

{steps}
""")

code("""
# Clean up the demo files this notebook created
from pathlib import Path
for f in ["demo.csv", "demo.parquet", "prices.parquet"]:
    Path(f).unlink(missing_ok=True)
""")

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
nbf.write(nb, HERE / "toolkit_guide.ipynb")
print("wrote", HERE / "toolkit_guide.ipynb")
