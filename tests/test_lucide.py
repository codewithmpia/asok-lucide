from asok_lucide import AsokLucideExtension
from asok_lucide.icons import _ICONS, load_icons, render_lucide_icon

from asok.core import Asok
from asok.templates.filters import TEMPLATE_FILTERS


def test_icons_preloading() -> None:
    """Verify that Lucide icons are preloaded in memory."""
    load_icons()
    assert len(_ICONS) > 1000
    assert "home" in _ICONS
    assert "shopping-cart" in _ICONS


def test_icon_rendering_basic() -> None:
    """Verify standard SVG generation with default attributes."""
    svg = render_lucide_icon("home")
    assert svg is not None
    assert str(svg).startswith("<svg")
    assert 'xmlns="http://www.w3.org/2000/svg"' in str(svg)
    assert 'width="24"' in str(svg)
    assert 'height="24"' in str(svg)
    assert 'viewBox="0 0 24 24"' in str(svg)
    assert 'stroke="currentColor"' in str(svg)
    assert "</svg>" in str(svg)


def test_icon_rendering_with_custom_attributes() -> None:
    """Verify custom attributes are correctly merged and serialized."""
    # Tester class_, stroke_width (converti en stroke-width) et styles/couleurs personnalisés
    svg = render_lucide_icon(
        "home",
        class_="w-6 h-6 text-indigo-500",
        stroke_width=3,
        stroke="red",
        style="margin-top: 10px;",
    )
    svg_str = str(svg)
    assert 'class="w-6 h-6 text-indigo-500"' in svg_str
    assert 'stroke-width="3"' in svg_str
    assert 'stroke="red"' in svg_str
    assert 'style="margin-top: 10px;"' in svg_str
    # Les attributs par défaut sont conservés s'ils ne sont pas écrasés
    assert 'width="24"' in svg_str
    # Les attributs internes ne doivent pas outrepasser la personnalisation
    assert 'stroke-width="2"' not in svg_str
    assert 'stroke="currentColor"' not in svg_str



def test_icon_name_normalization() -> None:
    """Verify camelCase, PascalCase, snake_case and kebab-case work."""
    ref_svg = str(render_lucide_icon("shopping-cart"))

    assert str(render_lucide_icon("shoppingCart")) == ref_svg
    assert str(render_lucide_icon("ShoppingCart")) == ref_svg
    assert str(render_lucide_icon("shopping_cart")) == ref_svg
    assert str(render_lucide_icon("shopping-cart")) == ref_svg


def test_icon_not_found() -> None:
    """Verify missing icons return a comment instead of crashing."""
    svg = render_lucide_icon("nonexistent-icon-name-xyz")
    assert "nonexistent-icon-name-xyz" in str(svg)
    assert str(svg).startswith("<!--")


def test_extension_registration() -> None:
    """Verify extension registers filters and shared helpers correctly."""
    app = Asok()
    # Réinitialiser TEMPLATE_FILTERS pour le test
    TEMPLATE_FILTERS.pop("lucide", None)

    AsokLucideExtension(app)

    # 1. Filtre enregistré
    assert "lucide" in TEMPLATE_FILTERS
    assert TEMPLATE_FILTERS["lucide"] == render_lucide_icon

    # 2. Aide partagée disponible globalement
    assert "lucide" in app._shared
    assert app._shared["lucide"](None) == render_lucide_icon


def test_extension_alias_registration() -> None:
    """Verify custom alias option registers filter and helper under the alias."""
    app = Asok()
    # Réinitialiser TEMPLATE_FILTERS pour le test
    TEMPLATE_FILTERS.pop("lucide", None)
    TEMPLATE_FILTERS.pop("icon", None)

    AsokLucideExtension(app, alias="icon")

    # 1. Les deux filtres existent
    assert "lucide" in TEMPLATE_FILTERS
    assert "icon" in TEMPLATE_FILTERS

    # 2. Les deux variables d'aide existent
    assert "lucide" in app._shared
    assert "icon" in app._shared
