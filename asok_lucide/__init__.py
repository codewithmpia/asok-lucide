from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from asok import AsokExtension
from asok.templates.filters import TEMPLATE_FILTERS

from .icons import load_icons, render_lucide_icon

if TYPE_CHECKING:
    from asok.core.asok import Asok


class AsokLucideExtension(AsokExtension):
    """Extension to integrate Lucide Icons seamlessly into Asok."""

    def __init__(self, app: Optional[Asok] = None, alias: Optional[str] = None) -> None:
        self.alias = alias
        super().__init__(app)

    def init_app(self, app: Asok) -> None:
        super().init_app(app)

        # 1. Preload icons in memory
        load_icons()

        # 2. Register the template filter in Asok
        TEMPLATE_FILTERS["lucide"] = render_lucide_icon
        if self.alias:
            TEMPLATE_FILTERS[self.alias] = render_lucide_icon

        # 3. Share the helper function globally for all templates
        # Variables registered via app.share() are called with the request if they are callable,
        # so we must return the rendering function as a factory taking request as a parameter.
        def lucide_helper(request: Any) -> Any:
            return render_lucide_icon

        app.share(lucide=lucide_helper)
        if self.alias:
            def alias_helper(request: Any) -> Any:
                return render_lucide_icon
            app.share(**{self.alias: alias_helper})
