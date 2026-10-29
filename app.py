"""Python Toolkit Guide as a Streamlit app.

Run locally:  streamlit run app.py
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression

import guide_content as gc

ASSETS = Path(__file__).parent / "assets"

st.set_page_config(page_title=gc.TITLE, page_icon=":books:", layout="wide")


def table(rows, columns):
    """Show a list of tuples as a clean, index-free table."""
    st.dataframe(pd.DataFrame(rows, columns=columns), hide_index=True, width="stretch")


def bullet_list(items):
    for name, text in items:
        st.markdown(f"- **{name}.** {text}")


@st.cache_data
def sample_prices(days: int = 500, seed: int = 7) -> pd.DataFrame:
    """Simulated daily prices so the demo runs without an API key or database."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=days)
    start = {"AAPL": 180, "MSFT": 400, "NVDA": 120, "AMZN": 170, "GOOGL": 150}
    frames = []
    for symbol, p0 in start.items():
        returns = rng.normal(0.0005, 0.018, days)
        frames.append(pd.DataFrame({"symbol": symbol, "ts": dates,
                                    "price": p0 * np.exp(np.cumsum(returns))}))
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------- pages
def page_overview():
    st.title(gc.TITLE)
    st.subheader(gc.SUBTITLE)
    st.write(gc.INTRO)
    st.markdown("Use the menu on the left to move between topics. "
                "Several pages include live demos you can interact with.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Libraries covered", len(gc.LIBRARIES))
    c2.metric("Trending tools", sum(1 for lib in gc.LIBRARIES if lib[4]))
    c3.metric("VS Code extensions", len(gc.EXTENSIONS))
    c4.metric("Learning steps", len(gc.LEARNING_ORDER))


def page_vscode():
    st.header("VS Code")
    st.write(gc.VSCODE_INTRO)
    st.subheader("Extensions to install first")
    table(gc.EXTENSIONS, ["Extension", "What it adds"])
    st.subheader("Features worth learning early")
    bullet_list(gc.FEATURES)
    st.subheader("Handy shortcuts")
    table(gc.SHORTCUTS, ["Action", "Mac", "Windows"])
    st.subheader("Gotchas")
    bullet_list(gc.VSCODE_GOTCHAS)


def page_libraries():
    st.header("Data analysis libraries")
    st.write(gc.LIBRARIES_INTRO)

    df = pd.DataFrame(gc.LIBRARIES, columns=["Category", "Library", "Used for", "Gotcha", "Trending"])
    c1, c2, c3 = st.columns([2, 2, 1])
    categories = c1.multiselect("Category", df["Category"].unique(), default=list(df["Category"].unique()))
    search = c2.text_input("Search", placeholder="e.g. SQL, charts, time series")
    trending_only = c3.toggle("Trending only")

    shown = df[df["Category"].isin(categories)]
    if trending_only:
        shown = shown[shown["Trending"]]
    if search:
        hit = shown.apply(lambda r: search.lower() in " ".join(map(str, r)).lower(), axis=1)
        shown = shown[hit]
    st.dataframe(shown, hide_index=True, width="stretch",
                 column_config={"Trending": st.column_config.CheckboxColumn()})

    st.subheader("See the gotchas in action")
    with st.expander("NumPy: never compare floats with =="):
        st.code("0.1 + 0.2 == 0.3\nnp.isclose(0.1 + 0.2, 0.3)")
        st.write("`0.1 + 0.2 == 0.3` returns", 0.1 + 0.2 == 0.3,
                 "while `np.isclose(0.1 + 0.2, 0.3)` returns", bool(np.isclose(0.1 + 0.2, 0.3)))

    with st.expander("pandas: chained assignment does not change the DataFrame"):
        demo = pd.DataFrame({"x": [-1, 2, 3], "y": [0, 0, 0]})
        chained = demo.copy()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            chained[chained.x > 0]["y"] = 1
        fixed = demo.copy()
        fixed.loc[fixed.x > 0, "y"] = 1
        left, right = st.columns(2)
        left.code('df[df.x > 0]["y"] = 1')
        left.dataframe(chained, hide_index=True)
        left.caption("Unchanged: the assignment went to a temporary copy.")
        right.code('df.loc[df.x > 0, "y"] = 1')
        right.dataframe(fixed, hide_index=True)
        right.caption("Changed as intended.")

    with st.expander("Streamlit: the whole script reruns on every click"):
        st.write("This page reran when you opened this expander. Slow work such as loading "
                 "data belongs in a function decorated with `@st.cache_data`, which runs once "
                 "and then returns the saved result.")


def page_workflow():
    st.header("How the libraries work together")
    st.write("A typical analysis moves through the same stages: get data, clean it, explore it, "
             "model it, show it. This demo uses simulated prices so it runs anywhere.")

    prices = sample_prices()
    symbols = st.multiselect("Tickers", prices["symbol"].unique(), default=["AAPL", "NVDA"])
    lo, hi = prices["ts"].min().date(), prices["ts"].max().date()
    start, end = st.slider("Date range", min_value=lo, max_value=hi, value=(lo, hi))

    df = prices[prices["symbol"].isin(symbols) & prices["ts"].dt.date.between(start, end)].copy()
    if df.empty:
        st.info("Pick at least one ticker.")
        return
    df["return"] = df.groupby("symbol")["price"].pct_change()

    st.plotly_chart(px.line(df, x="ts", y="price", color="symbol",
                            labels={"ts": "Date", "price": "Price (USD)"}), width="stretch")

    left, right = st.columns(2)
    left.markdown("**Daily return summary**")
    left.dataframe(df.groupby("symbol")["return"].describe().round(4), width="stretch")

    right.markdown("**Linear trend (scikit-learn)**")
    for symbol, g in df.groupby("symbol"):
        X = np.arange(len(g)).reshape(-1, 1)
        slope = LinearRegression().fit(X, g["price"]).coef_[0]
        right.write(f"{symbol}: {slope:+.3f} USD per trading day")

    with st.expander("The same steps as a script against a real database"):
        st.code(gc.WORKFLOW_CODE, language="python")


def page_uv():
    st.header("venv vs uv")
    st.write(gc.UV_INTRO)
    table(gc.VENV_UV_COMPARE, ["", "venv + pip", "uv"])

    st.subheader("The same task with each tool")
    tasks = [row[0] for row in gc.VENV_UV_COMMANDS]
    task = st.selectbox("Task", tasks)
    _, venv_cmd, uv_cmd = gc.VENV_UV_COMMANDS[tasks.index(task)]
    left, right = st.columns(2)
    left.markdown("**venv + pip**")
    left.code(venv_cmd, language="bash")
    right.markdown("**uv**")
    right.code(uv_cmd, language="bash")

    with st.expander("All commands"):
        table(gc.VENV_UV_COMMANDS, ["Task", "venv + pip", "uv"])

    st.markdown("Install uv on a Mac or Linux:")
    st.code(gc.UV_INSTALL, language="bash")
    st.subheader("Gotchas")
    bullet_list(gc.UV_GOTCHAS)


def page_git():
    st.header("Git and GitHub")
    st.write(gc.GIT_INTRO)
    st.image(str(ASSETS / "git_workflow.png"), width="stretch")
    st.caption("Nothing reaches GitHub until you push, and nothing from GitHub reaches "
               "your computer until you pull.")
    st.subheader("Core ideas")
    table(gc.GIT_TERMS, ["Term", "Meaning"])
    st.subheader("The daily workflow")
    st.code(gc.GIT_WORKFLOW, language="bash")
    st.write("VS Code's Source Control panel does all of this with buttons, which is a good way "
             "to start; the commands are worth learning so you understand what the buttons do.")
    st.subheader("Gotchas")
    bullet_list(gc.GIT_GOTCHAS)


def page_github():
    st.header("Getting the most out of GitHub")
    st.write("GitHub is also the best free classroom for programming: millions of real projects "
             "are open to read, run, question and improve.")
    tab1, tab2, tab3 = st.tabs(["For learning", "For your own projects", "Working with others"])
    with tab1:
        bullet_list(gc.GITHUB_LEARNING)
    with tab2:
        bullet_list(gc.GITHUB_OWN)
    with tab3:
        bullet_list(gc.GITHUB_OTHERS)


def page_path():
    st.header("A suggested order")
    st.write("Each step uses the one before it. Tick them off as you go "
             "(progress resets when the page is reloaded).")
    done = 0
    for i, (name, text) in enumerate(gc.LEARNING_ORDER, start=1):
        if st.checkbox(f"**{i}. {name}.** {text}", key=f"step{i}"):
            done += 1
    st.progress(done / len(gc.LEARNING_ORDER), text=f"{done} of {len(gc.LEARNING_ORDER)} done")


PAGES = {
    "Overview": page_overview,
    "VS Code": page_vscode,
    "Data libraries": page_libraries,
    "Try it: workflow demo": page_workflow,
    "venv vs uv": page_uv,
    "Git and GitHub": page_git,
    "GitHub for learning": page_github,
    "Learning path": page_path,
}

choice = st.sidebar.radio("Topics", list(PAGES))
PAGES[choice]()
