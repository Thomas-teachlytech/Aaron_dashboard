# Python Toolkit Guide

A practical reference for a modern Python data setup: VS Code, the most popular data
analysis libraries, venv vs uv, and Git/GitHub. It comes in two forms:

- **`app.py`**: an interactive Streamlit app with live demos
- **`toolkit_guide.ipynb`**: a Jupyter notebook with runnable examples of each library and gotcha

## Files

| File | Purpose |
| --- | --- |
| `app.py` | The Streamlit app |
| `guide_content.py` | All guide text and tables, shared by the app and the notebook builder |
| `toolkit_guide.ipynb` | The notebook |
| `build_notebook.py` | Regenerates the notebook from `guide_content.py` |
| `assets/git_workflow.png` | Git diagram used by both |
| `requirements.txt` | Packages Streamlit Community Cloud installs for the app |

## Run the app locally

With uv:

```bash
uv venv
uv pip install -r requirements.txt
uv run streamlit run app.py
```

Or with venv and pip:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Run the notebook

The notebook uses a few extra packages:

```bash
uv pip install -r requirements.txt polars pyarrow matplotlib ipykernel
```

Then open `toolkit_guide.ipynb` in VS Code, pick the `.venv` kernel, and choose **Run All**.
DuckDB is optional; that cell is skipped if it is not installed.

## Deploy to Streamlit Community Cloud (free)

1. Create a new repository on GitHub and push this folder to it:
   ```bash
   git init
   git add .
   git commit -m "Python Toolkit Guide app and notebook"
   git branch -M main
   git remote add origin https://github.com/<your-username>/python-toolkit-guide.git
   git push -u origin main
   ```
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose the repository, branch `main`, and main file `app.py`.
4. Click **Deploy**. Streamlit installs `requirements.txt` and gives the app a public URL.

Every later `git push` to `main` redeploys the app automatically.

## Updating the content

Edit `guide_content.py`, then run `python build_notebook.py` to refresh the notebook.
The app reads the same file, so both stay in sync.
