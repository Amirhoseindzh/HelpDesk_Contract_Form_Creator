from dataclasses import dataclass

from docx.shared import Inches, Pt, RGBColor


@dataclass(frozen=True)
class FontStyle:
    """Immutable font style configuration."""

    name: str
    size: Pt
    bold: bool = False
    italic: bool = False
    color: RGBColor = None


@dataclass(frozen=True)
class MarginStyle:
    """Document margin configuration."""

    top: Inches
    bottom: Inches
    left: Inches
    right: Inches


class DocumentStyles:
    """Centralized document styles."""

    # === FONTS ===
    TITLE = FontStyle(name="Arial Black", size=Pt(26), bold=True)

    SUBTITLE = FontStyle(name="Arial", size=Pt(14), italic=True)

    SECTION_HEADING = FontStyle(
        name="Arial", size=Pt(14), bold=True, color=RGBColor(0, 51, 102)
    )

    LABEL = FontStyle(name="Arial", size=Pt(11), bold=True)

    BODY = FontStyle(name="Arial", size=Pt(11), bold=False)

    SMALL = FontStyle(name="Arial", size=Pt(9), italic=True)

    FOOTER = FontStyle(
        name="Arial", size=Pt(9), italic=True, color=RGBColor(100, 100, 100)
    )

    # === MARGINS ===
    MARGINS = MarginStyle(
        top=Inches(0.6), bottom=Inches(0.6), left=Inches(0.75), right=Inches(0.75)
    )

    # === COLORS ===
    PRIMARY_COLOR = RGBColor(0, 51, 102)
    SECONDARY_COLOR = RGBColor(0, 102, 153)
    ACCENT_COLOR = RGBColor(0, 128, 0)
    BORDER_COLOR = RGBColor(200, 200, 200)

    # === TABLE ===
    TABLE_LABEL_WIDTH = Inches(2.5)
    TABLE_VALUE_WIDTH = Inches(4.5)

    # === DECORATIVE ===
    THICK_LINE = "═" * 70
    THIN_LINE = "─" * 60

    @staticmethod
    def apply_font(run, style: FontStyle) -> None:
        """Apply font style to a run."""
        run.font.name = style.name
        run.font.size = style.size
        run.font.bold = style.bold
        run.font.italic = style.italic
        if style.color:
            run.font.color.rgb = style.color


# Global instance
STYLES = DocumentStyles()
