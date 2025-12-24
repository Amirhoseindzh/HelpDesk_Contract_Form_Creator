from .base_section import BaseSection


class DeviceSection(BaseSection):
    """Section 2: Device Information"""

    @property
    def section_number(self) -> str:
        return "2"

    @property
    def section_title(self) -> str:
        return "DEVICE INFORMATION"

    def _add_content(self, data: dict) -> None:
        """Add device information table."""
        self._create_info_table(
            [
                ("Device Model:", data.get("Device_Model", "N/A")),
                ("Serial Number:", data.get("Device_Serial", "N/A")),
            ]
        )
