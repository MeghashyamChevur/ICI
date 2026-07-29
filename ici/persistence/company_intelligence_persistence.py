from pathlib import Path

from ici.models import CompanyIntelligence


class CompanyIntelligencePersistence:
    """
    Persists CompanyIntelligence objects.
    """

    def save(
        self,
        intelligence: list[CompanyIntelligence],
        output_path: Path,
    ) -> None:
        """
        Save company intelligence data.
        """
        pass