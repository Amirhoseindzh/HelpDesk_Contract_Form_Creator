from .base_section import BaseSection


class ProblemSection(BaseSection):
    """Section 3: Reported Problem"""

    @property
    def section_number(self) -> str:
        return "3"

    @property
    def section_title(self) -> str:
        return "REPORTED PROBLEM"

    def _add_content(self, data: dict) -> None:
        """Add problem description in a styled box."""
        problem_text = data.get("Device_Problem", "No problem description provided.")
        # Now _add_text_box is inherited from BaseSection!
        self._add_text_box(problem_text, "⚠️ Issue Reported:")


class ServiceSection(BaseSection):
    """Section 4: Service Description"""

    @property
    def section_number(self) -> str:
        return "4"

    @property
    def section_title(self) -> str:
        return "SERVICE DESCRIPTION & WORK PERFORMED"

    def _add_content(self, data: dict) -> None:
        """Add service description in a styled box."""
        # Support both 'Description' and 'description' keys
        service_text = data.get("Description") or data.get("description", "N/A")
        self._add_text_box(service_text, "🔧 Work Details:")
