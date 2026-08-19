from typing import Annotated, Literal

from pydantic import Field

from mcp_instance import mcp
from domain_types import DocumentRef


@mcp.tool
def generate_handbook(
    employee_id: Annotated[
        str,
        Field(description="Identifiant de la fiche employé, retourné par create_employee_record."),
    ],
    template: Annotated[
        Literal["welcome_pack", "mission_letter"],
        Field(
            description=(
                "Gabarit à utiliser : 'welcome_pack' pour un livret d'accueil général "
                "(présentation de l'équipe, pratiques internes, accès) — à utiliser par "
                "défaut pour un onboarding standard. 'mission_letter' pour une lettre de "
                "mission détaillant les objectifs et responsabilités du poste — à utiliser "
                "si le rôle ou les missions ont été précisées dans la demande."
            )
        ),
    ],
) -> DocumentRef:
    """Génère un document PDF (livret d'accueil ou lettre de mission) à
    remettre au nouveau collaborateur. Nécessite que la fiche employé ait
    déjà été créée (voir create_employee_record). Retourne le chemin du
    fichier généré."""
    raise NotImplementedError
