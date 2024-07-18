# Customised Jupyter Environment Example

The default JupyterLab and Jupyter notebook environments defined by the `container-builder` `jupyterlab` and `notebook` packs do not have any extensions installed by default.

We can create a highly customised environment featuring a range of extensions as described in the [OU TM351 JupyterLab Customisation Guide](https://innovationoutside.github.io/ou-tm351-jl-extensions/overview.html) by installing a simple convenience package into the `packages.pip.system` environment.

```yaml
packages:
  pip:
    system:
      - ou-tm351-jl-extensions>=0.2.8
```

This convenience package then installs the following extensions:

```bash
# Branding and OU extensions
jupyterlab-ou-brand-extension = "^0.2.0" # OU brand extension (favicon, logo)

# Notebook cell tools
jupyterlab-cell-status-extension = "^0.2.2" # cell execution status; accessibility tools
jupyterlab-empinken-extension = "^0.5.2" # cell background styling
jupyterlab-skip-traceback = "^5.1.0" # skip trackeback / error reporting
jupyterlab-myst = "^2.4.0" ## MyST parser and styling (markdown cells)
jupyterlab-spellchecker = "^0.8.4" ## Spellchecker

# Code support
#jupyterlab-lsp = "^5.1.0" # language server protocol
jupyterlab-code-formatter = "^2.2.1" # Code formatter
black = "^24.4.2" # code formatting
isort = "^5.13.2" # code formatting

# Language packs
jupyterlab-language-pack-fr-fr = "^4.1.post2" # French
jupyterlab-language-pack-zh-cn = "^4.1.post2" # Chinese

# File browsing and handling
jupyterlab-unfold = "^0.3.0" # tree view in files sidebar
jupyter-archive = "^3.4.0" # archive file download
jupyterlab-filesystem-access = "^0.6.0" # local filesystem access
jupyterlab-git = "^0.50.0" # Git/Github tools
jupytext = "^1.16.0" # text notebook formats

# Renderers
jupyterlab-geojson = "^3.3.1" # geojson renderer
jupyter-compare-view = "^0.2.4" # compare images

# Resource monitoring
#jupyter-resource-usage = "^1.0.2" # memory/CPU
jupyterlab_execute_time = "^3.1.2" # cell execution time
```
