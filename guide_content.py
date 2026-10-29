"""Text and tables for the Python Toolkit Guide, shared by the Streamlit app."""

TITLE = "Python Toolkit Guide"
SUBTITLE = "VS Code, data libraries, uv and GitHub"
INTRO = (
    "A practical reference for setting up a modern Python environment and building "
    "projects on your own: the editor, the libraries, the package tools, and GitHub."
)

# ---------------------------------------------------------------- VS Code
VSCODE_INTRO = (
    "VS Code is a free editor that becomes a full Python and data environment once you "
    "add a few extensions. It handles scripts, Jupyter notebooks, Git, the terminal and "
    "remote servers in one window."
)

EXTENSIONS = [
    ("Python (Microsoft)", "Run, debug and pick the Python interpreter"),
    ("Pylance", "Autocomplete, type checking, go to definition"),
    ("Jupyter", "Run .ipynb notebooks inside VS Code"),
    ("Ruff", "Fast linting and auto-formatting on save"),
    ("GitLens", "Shows who changed each line and when; richer Git history"),
    ("Remote - SSH", "Edit and run code on another machine, such as a Linux server, as if it were local"),
    ("Rainbow CSV / Data Wrangler", "Readable CSV files; a spreadsheet-like view of DataFrames"),
    ("Claude Code (optional)", "An AI assistant that can read, explain and edit code in your project"),
]

FEATURES = [
    ("Command Palette", "Cmd+Shift+P on Mac, Ctrl+Shift+P on Windows. Every command in VS Code is searchable here."),
    ("Select Interpreter", "Tells VS Code which Python (and which virtual environment) to use. Most 'module not found' problems come from this."),
    ("Integrated terminal", "Ctrl+` opens a terminal in your project folder."),
    ("Debugger", "Click left of a line number to set a breakpoint, press F5, and step through the code while inspecting variables."),
    ("Source Control panel", "Stage, commit, push and view diffs without typing Git commands."),
    ("Notebook cells in .py files", "Typing # %% in a regular Python file creates runnable cells: notebook-style exploration in a plain script that Git handles well."),
]

SHORTCUTS = [
    ("Open any file by name", "Cmd+P", "Ctrl+P"),
    ("Command Palette", "Cmd+Shift+P", "Ctrl+Shift+P"),
    ("Go to definition", "F12", "F12"),
    ("Rename a variable everywhere", "F2", "F2"),
    ("Comment out lines", "Cmd+/", "Ctrl+/"),
    ("Multi-cursor on next match", "Cmd+D", "Ctrl+D"),
    ("Toggle terminal", "Ctrl+`", "Ctrl+`"),
]

VSCODE_GOTCHAS = [
    ("Wrong interpreter", "A package is installed but VS Code says it is missing: the bottom-right corner shows which Python is active. Pick the one inside your project's .venv."),
    ("Notebook kernel vs terminal", "A notebook's kernel and the terminal can use different environments. Check both."),
    ("Open the folder, not the file", "Use File > Open Folder on the project root so VS Code finds the .venv, settings and Git repo."),
    ("Workspace settings", "Settings in .vscode/settings.json apply only to that project and override your global ones."),
]

# ---------------------------------------------------------------- Libraries
LIBRARIES_INTRO = (
    "NumPy and pandas are the foundation almost everything else builds on. The biggest "
    "recent trends are faster tools for the same jobs: Polars and DuckDB for data, uv and "
    "Ruff for tooling, marimo for notebooks, and PyTorch replacing TensorFlow for most new "
    "deep learning work."
)

# (category, library, used for, gotcha, trending)
LIBRARIES = [
    ("Core data", "NumPy", "Fast arrays and math; the base layer under pandas, scikit-learn and others",
     "Never compare floats with ==; use np.isclose()", False),
    ("Core data", "pandas", "Tables (DataFrames): load, clean, filter, group, join, time series",
     "Chained assignment like df[df.x > 0]['y'] = 1 does not change df; use df.loc[df.x > 0, 'y'] = 1", False),
    ("Core data", "Polars", "A much faster DataFrame library, often 5 to 10 times quicker on large data",
     "Different syntax from pandas (expressions, no index); lazy queries need .collect()", True),
    ("Core data", "DuckDB", "Run SQL directly on DataFrames, CSV and Parquet files, with no server",
     "Only one process can write to a DuckDB file at a time", True),
    ("Core data", "PyArrow / Parquet", "A compact, typed file format; much faster than CSV for large datasets",
     "CSV loses types (dates become text); save working data as Parquet", False),
    ("Visualization", "Matplotlib", "The standard static plotting library; full control",
     "Two styles exist (plt.plot vs fig, ax); use fig, ax = plt.subplots() consistently", False),
    ("Visualization", "Seaborn", "Statistical charts (distributions, heatmaps) in one line",
     "Works best with 'long' data: one row per observation", False),
    ("Visualization", "Plotly", "Interactive charts with zoom and hover, for notebooks and web apps",
     "Very large datasets make slow, heavy pages; downsample first", False),
    ("Stats and ML", "SciPy", "Statistical tests, optimization, signal processing",
     "Check each test's assumptions (normality, independence)", False),
    ("Stats and ML", "statsmodels", "Regression with full statistical output, time-series models (ARIMA)",
     "sm.OLS needs an explicit constant (sm.add_constant) unless you use the formula API", False),
    ("Stats and ML", "scikit-learn", "Classic ML: regression, classification, clustering, PCA, pipelines",
     "Data leakage: fit scalers and models on training data only; for time series use TimeSeriesSplit, never shuffled splits", False),
    ("Stats and ML", "XGBoost / LightGBM", "Gradient boosting; usually the strongest choice for tabular data",
     "Easy to overfit; tune with cross-validation", False),
    ("Stats and ML", "PyTorch", "Deep learning; now the most common choice for new work",
     "Often overkill for tabular data; try gradient boosting first", True),
    ("Notebooks and apps", "Jupyter", "Interactive notebooks for exploration",
     "Cells run out of order hide bugs; use Restart and Run All before trusting results", False),
    ("Notebooks and apps", "marimo", "Reactive notebooks saved as plain .py files, so they work well with Git",
     "Each variable can only be defined in one cell", True),
    ("Notebooks and apps", "Streamlit", "Turn a script into an interactive web dashboard",
     "The whole script reruns on every click; cache slow loads with @st.cache_data", False),
    ("Getting data", "requests / httpx", "Calling web APIs",
     "No default timeout; always pass timeout=10 or a call can hang forever", False),
    ("Getting data", "SQLAlchemy", "Connecting to MySQL, Postgres and other databases",
     "Use parameters (:name), never f-strings, to put values into SQL", False),
    ("Getting data", "BeautifulSoup / Playwright", "Web scraping: static HTML / pages that need a real browser",
     "Check the site's terms and robots.txt; add delays between requests", False),
    ("Getting data", "Pydantic", "Validating data shapes and types (API responses, configs)",
     "Version 2 changed much of the API; older tutorials use version 1", False),
]

WORKFLOW_CODE = '''import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

# 1. Get data: SQL into a DataFrame
engine = create_engine("mysql+pymysql://user:pass@host/market")
df = pd.read_sql("SELECT symbol, ts, price FROM quotes", engine, parse_dates=["ts"])

# 2. Clean and reshape with pandas
df = df.dropna().sort_values("ts")
df["return"] = df.groupby("symbol")["price"].pct_change()

# 3. Explore: summary stats and an interactive chart
print(df.groupby("symbol")["return"].describe())
px.line(df, x="ts", y="price", color="symbol").show()

# 4. Model with scikit-learn (NumPy arrays underneath)
aapl = df[df.symbol == "AAPL"].dropna()
X = np.arange(len(aapl)).reshape(-1, 1)      # time step as the feature
model = LinearRegression().fit(X, aapl["price"])
print("trend per step:", model.coef_[0])

# 5. Save for later in a fast, typed format
df.to_parquet("quotes.parquet")
'''

# ---------------------------------------------------------------- venv vs uv
UV_INTRO = (
    "Both give each project its own private set of packages, so one project's versions "
    "never break another's. venv is built into Python and only creates the environment; "
    "uv is a newer, much faster tool that also installs Python itself, manages dependencies "
    "and locks exact versions. For new projects, uv is the recommended choice; venv is still "
    "worth knowing because older tutorials and projects use it."
)

VENV_UV_COMPARE = [
    ("Comes with Python", "Yes", "No, one-time install"),
    ("Speed", "Normal", "Often 10 to 100 times faster installs"),
    ("Installs Python versions", "No", "Yes (uv python install 3.13)"),
    ("Dependency list", "requirements.txt, maintained by hand", "pyproject.toml, updated automatically"),
    ("Exact versions locked", "Only if you run pip freeze", "Always, in uv.lock"),
    ("Need to activate the environment", "Yes", "No; uv run uses it automatically"),
]

# (task, venv + pip, uv)
VENV_UV_COMMANDS = [
    ("Start a project", "python -m venv .venv", "uv init"),
    ("Activate (Mac/Linux)", "source .venv/bin/activate", "# not needed"),
    ("Add a package", "pip install pandas", "uv add pandas"),
    ("Save the dependency list", "pip freeze > requirements.txt", "# automatic"),
    ("Recreate on another machine", "pip install -r requirements.txt", "uv sync"),
    ("Run a script", "python etl.py   # after activating", "uv run etl.py"),
]

UV_INSTALL = "curl -LsSf https://astral.sh/uv/install.sh | sh"

UV_GOTCHAS = [
    ("Never commit .venv", "Add it to .gitignore. Commit pyproject.toml and uv.lock (or requirements.txt) instead."),
    ("Forgetting to activate (venv only)", "pip install then installs into the global Python, not the project."),
    ("Mixing tools", "In a uv project use uv add, not pip install, or the lock file falls out of date."),
    ("Conda", "A third option, mainly used for heavy scientific packages with non-Python dependencies; for most data work uv is simpler."),
]

# ---------------------------------------------------------------- Git and GitHub
GIT_INTRO = (
    "Git is version control that runs on your computer: it saves snapshots (commits) of "
    "your project so you can see every change and go back to any point. GitHub is a website "
    "that hosts Git repositories online, so you can back them up, share them and work with "
    "other people."
)

GIT_TERMS = [
    ("Repository (repo)", "A project folder whose history Git tracks"),
    ("Commit", "A saved snapshot with a message describing the change"),
    ("Branch", "A separate line of work; main is the default, and new ideas go on their own branch"),
    ("Remote", "The online copy of the repo, usually called origin"),
    ("Clone", "Download a repo from GitHub to your computer"),
    ("Fork", "Your own copy of someone else's repo on GitHub, which you can change freely"),
    ("Pull request (PR)", "A request to merge a branch into another, with a place for review and discussion"),
    ("Issue", "A bug report, question or idea attached to a repo"),
    (".gitignore", "A list of files Git should never track, such as .venv and .env"),
]

GIT_WORKFLOW = '''git clone https://github.com/user/project.git   # once, to get a copy
git switch -c add-news-tool                      # new branch for a new idea
# ...edit files...
git status                                       # what changed?
git add etl.py                                   # stage the changes to save
git commit -m "Add news to the ETL pipeline"     # save a snapshot
git push -u origin add-news-tool                 # upload the branch to GitHub
# then open a pull request on GitHub and merge it into main
git switch main && git pull                      # get the merged result
'''

GIT_GOTCHAS = [
    ("Secrets in commits", "An API key committed once stays in the history even after you delete the file. Keep keys in .env, list .env in .gitignore, and if a key is ever pushed, revoke it and make a new one."),
    ("Large data files", "GitHub rejects files over 100 MB and repos get slow well before that. Keep data out of Git; commit the code that fetches it."),
    ("Merge conflicts", "When two changes touch the same lines, Git asks you to choose. VS Code shows both versions side by side with Accept buttons."),
    ("Pull before you push", "If GitHub has changes you do not have, your push is rejected; run git pull first."),
    ("Small, frequent commits", "Clear messages make the history useful; one giant 'updates' commit tells you nothing later."),
]

GITHUB_LEARNING = [
    ("Read real code", "Pick a library you use (pandas, Streamlit, FastMCP) and browse its source. Press . on any repo page to open it in a browser version of VS Code."),
    ("Star and watch", "Starring bookmarks a repo; watching (Releases only) tells you when a new version ships."),
    ("Explore and Trending pages", "See what developers are building right now, filtered by language."),
    ("Awesome lists", "Search for lists such as awesome-quant or awesome-python: curated directories of the best tools on a topic."),
    ("Examples and Issues", "Check a repo's examples folder and its Issues. Closed issues often answer the exact problem you hit."),
    ("Codespaces", "Run any repo in the browser without installing anything."),
]

GITHUB_OWN = [
    ("A repo for every project", "From day one, even private ones. It is a backup, a history and a portfolio."),
    ("A good README", "What the project does, how to install it, how to run it, and a screenshot."),
    ("Issues as a to-do list", "Plus a Project board to organize them."),
    ("GitHub Actions", "Runs code automatically on a schedule or on every push: tests, linting, or even a daily data download."),
    ("Gists", "Handy for sharing a single snippet or notebook."),
]

GITHUB_OTHERS = [
    ("Start small", "Look for issues labelled good first issue or help wanted. Typo and documentation fixes are welcome first contributions."),
    ("Read CONTRIBUTING.md", "Before opening a pull request; it explains the project's rules."),
    ("The usual contribution flow", "Fork the repo, clone your fork, create a branch, commit, push, and open a pull request back to the original."),
    ("Write useful issues", "What you expected, what happened, the exact error, and the smallest code that reproduces it."),
    ("Use Discussions", "For questions and ideas rather than Issues, when a repo has them enabled."),
    ("Review others' pull requests", "Reading and commenting on PRs is one of the fastest ways to learn how experienced developers think."),
    ("Keep PRs small and focused", "One change per PR gets reviewed and merged much faster."),
]

# ---------------------------------------------------------------- Learning order
LEARNING_ORDER = [
    ("VS Code and uv", "Install both, create a first project with uv init, and run a script from VS Code."),
    ("Git and GitHub", "Turn that project into a repo, add a .gitignore, and push it to GitHub."),
    ("pandas in a notebook", "Load a CSV or an API response into a DataFrame and explore it with Plotly."),
    ("Database connectivity", "Read from and write to MySQL with SQLAlchemy."),
    ("The ETL project", "Combine the first four steps into a script that runs on a schedule."),
    ("Stats and ML", "Add statsmodels or scikit-learn to the collected data."),
    ("Share it", "A Streamlit dashboard or an MCP server, with a README on GitHub."),
]
