from datetime import date
from typing import Annotated

from pydantic import Field

from mcp_instance import mcp
from domain_types import EventRef


@mcp.tool
def create_calendar_event(
    title: Annotated[
        str,
        Field(description="Titre de l'événement (ex: 'Présentation de Léa à l'équipe')."),
    ],
    event_date: Annotated[
        date,
        Field(description="Date de l'événement, au format ISO YYYY-MM-DD."),
    ],
    duration_minutes: Annotated[
        int,
        Field(description="Durée de l'événement en minutes (ex: 30, 60). Doit être positif."),
    ],
    attendees: Annotated[
        list[str],
        Field(
            description=(
                "Liste des noms ou emails des participants à inviter "
                "(ex: ['Léa Martin', 'manager@entreprise.com'])."
            )
        ),
    ],
) -> EventRef:
    """Crée un événement calendrier (fichier .ics), typiquement pour une
    réunion d'accueil ou une présentation d'équipe. À utiliser seulement
    si l'intention mentionne explicitement un besoin de réunion, de
    rendez-vous, ou de présentation — pas systématiquement pour tout
    onboarding. Retourne l'identifiant de l'événement créé."""
    raise NotImplementedError
