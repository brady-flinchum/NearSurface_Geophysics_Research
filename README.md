# Academic Site

Built with [Sphinx](https://www.sphinx-doc.org/) + [pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io/).

## Local development

```bash
pip install -r requirements.txt
sphinx-build -b html docs/ docs/_build/html
open docs/_build/html/index.html
```

## Adding a new page

1. Create `docs/your-section/new-page.md` (or `.rst`)
2. Add `new-page` to the `toctree` in that section's `index.rst`
3. `git add`, `git commit`, `git push` → GitHub builds automatically

## Adding a notebook with PyVista

1. Create your notebook in `docs/code/my-notebook.ipynb`
2. At the top of the notebook, set:
   ```python
   import pyvista as pv
   pv.set_jupyter_backend('static')   # static screenshots for CI
   ```
3. Add `my-notebook` to `docs/code/index.rst`
4. Push — nbsphinx will execute it and embed the output

## Site URL

`https://YOUR_USERNAME.github.io/YOUR_REPO`
