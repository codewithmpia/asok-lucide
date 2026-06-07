import json
import os
import re
from typing import Any

from asok.templates import SafeString, _render_attrs

# Dictionnaire global pour stocker les icônes chargées
_ICONS: dict[str, str] = {}


def load_icons() -> None:
    """Précharge les icônes Lucide en mémoire."""
    global _ICONS
    if not _ICONS:
        data_path = os.path.join(os.path.dirname(__file__), "data", "lucide-icons.json")
        with open(data_path, "r", encoding="utf-8") as f:
            _ICONS.clear()
            _ICONS.update(json.load(f))


def render_lucide_icon(name: str, **attrs: Any) -> SafeString:
    """Génère le rendu SVG d'une icône Lucide."""
    # Convertir camelCase / PascalCase / snake_case en kebab-case
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    normalized_name = re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1).lower().replace("_", "-")

    # Charger les icônes si ce n'est pas déjà fait
    if not _ICONS:
        load_icons()

    body = _ICONS.get(normalized_name)
    if not body:
        return SafeString(f"<!-- Lucide icon '{name}' not found -->")

    # Attributs SVG par défaut de Lucide
    svg_attrs = {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": "24",
        "height": "24",
        "viewBox": "0 0 24 24",
        "fill": "none",
        "stroke": "currentColor",
        "stroke-width": "2",
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
    }

    # Fusion avec les attributs personnalisés passés
    # Gérer la convention python class_ -> class, etc.
    custom_attrs = {}
    for k, v in attrs.items():
        key = k.rstrip("_") if k.endswith("_") and k != "_" else k
        key = key.replace("_", "-")  # ex: stroke_width -> stroke-width
        custom_attrs[key] = v

    svg_attrs.update(custom_attrs)

    # Utiliser _render_attrs d'Asok
    rendered_attrs = _render_attrs(svg_attrs)

    return SafeString(f"<svg{rendered_attrs}>{body}</svg>")
