<p align="center">
  <a href="https://asok-framework.com/">
    <img src="https://raw.githubusercontent.com/codewithmpia/asok-lucide/main/assets/asok.svg" alt="Asok Logo" width="60" height="60" />
  </a>
  <span style="font-size: 32px; font-weight: bold; margin: 0 15px; position: relative; bottom: 15px; color: #6B7280;">+</span>
  <a href="https://lucide.dev/">
    <img src="https://raw.githubusercontent.com/codewithmpia/asok-lucide/main/assets/lucide.svg" alt="Lucide Logo" width="60" height="60" />
  </a>
</p>

<h1 align="center">asok-lucide</h1>

<p align="center">
  <a href="https://pypi.org/project/asok-lucide/">
    <img src="https://img.shields.io/pypi/v/asok-lucide.svg" alt="PyPI version" />
  </a>
</p>

<p align="center">
  <strong>Lucide Icons</strong> integration for the <strong>Asok Framework</strong>.
</p>

<p align="center">
  Render beautiful Lucide Icons server-side with zero client-side JavaScript overhead.
</p>

## Resources

* **PyPI Project**: [pypi.org/project/asok-lucide](https://pypi.org/project/asok-lucide/)
* **Asok Framework**: [asok-framework.com](https://asok-framework.com/)
* **Asok Repository**: [github.com/asok-framework/asok](https://github.com/asok-framework/asok)
* **Lucide Icons**: [lucide.dev](https://lucide.dev/)


## Installation

```bash
pip install asok-lucide
```

For development or contributing, install in editable mode:

```bash
pip install -e .
```

## Setup

Register the extension in your `wsgi.py`:

```python
from asok import Asok
from asok_lucide import AsokLucideExtension

app = Asok()
app.register_extension(AsokLucideExtension)
```

You can optionally configure a custom alias (e.g. `icon`) to shorten the template helper name:

```python
app.register_extension(AsokLucideExtension(alias="icon"))
```

## Usage

### Direct template helper

```html
<button>
    {{ lucide("shopping-cart", class_="w-5 h-5 text-white") }}
    <span>Add to Cart</span>
</button>
```

Or using the custom alias (if registered):

```html
{{ icon("user", class_="w-6 h-6") }}
```

### Template filter

```html
{{ "home" | lucide(class_="w-6 h-6", stroke_width="1.5") }}
```

All standard attributes (such as `class`, `stroke-width`, `stroke`, `fill`, `style`) can be customized dynamically. Use `class_` or snake_case `stroke_width` in template helpers.

## Development & Publishing

### Updating the Icon Dataset

The icons are pre-compiled and bundled inside the package (`asok_lucide/data/lucide-icons.json`) to guarantee fast, deterministic server-side rendering without runtime network dependencies.

To update the bundled Lucide Icons (e.g., when a new Lucide version releases):

1. Run the update script to fetch and resolve all icon definitions & aliases from Iconify:
   ```bash
   python scripts/fetch_icons.py
   ```
2. Run the test suite to verify everything still renders correctly:
   ```bash
   python -m pytest tests
   ```
3. Commit the updated `lucide-icons.json` to Git.

### Releases & GitHub Actions

A GitHub Actions workflow is configured in `.github/workflows/release.yml`. When you publish a release on GitHub:
1. The workflow checks out the repository (which contains the committed `lucide-icons.json` data).
2. It builds the wheel and source distributions.
3. It automatically publishes the package to PyPI using PyPI's **Trusted Publishing** OIDC integration.

