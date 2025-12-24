from .base_section import BaseSection


class PartiesSection(BaseSection):
    """Section 1: Parties Information"""

    @property
    def section_number(self) -> str:
        return "1"

    @property
    def section_title(self) -> str:
        return "PARTIES INFORMATION"

    def _add_content(self, data: dict) -> None:
        """Add parties information table."""
        self._create_info_table(
            [
                ("Customer Name:", data.get("fullname", "N/A")),
                ("Service Provider:", data.get("ServiceMan", "N/A")),
            ]
        )
