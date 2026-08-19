import os
from datetime import date
from typing import Annotated

import httpx
from pydantic import Field

from mcp_instance import mcp
from domain_types import IssueRef

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
GITHUB_API_BASE = "https://api.github.com"


@mcp.tool
async def create_onboarding_issue(
    employee_name: Annotated[
        str,
        Field(description="Nom complet du nouveau collaborateur (ex: 'Léa Martin')."),
    ],
    start_date: Annotated[
        date,
        Field(description="Date d'arrivée du collaborateur, au format ISO YYYY-MM-DD."),
    ],
    checklist: Annotated[
        list[str],
        Field(
            description=(
                "Liste des tâches à accomplir avant ou pendant l'arrivée "
                "(ex: ['Créer le compte', 'Préparer le poste de travail', "
                "'Badge d'accès']). Au moins un élément."
            )
        ),
    ],
) -> IssueRef:
    """Crée un ticket de suivi (issue GitHub) pour tracer l'ensemble des
    tâches d'onboarding d'un nouveau collaborateur. À utiliser dès qu'un
    plan d'onboarding est lancé, pour centraliser le suivi des tâches
    associées dans le tracker de l'équipe. Retourne l'URL de l'issue créée."""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        raise RuntimeError(
            "GITHUB_TOKEN et GITHUB_REPO doivent être définis dans l'environnement "
            "(voir .env.example)."
        )

    checklist_md = "\n".join(f"- [ ] {item}" for item in checklist)
    body = (
        f"## Onboarding — {employee_name}\n\n"
        f"**Date d'arrivée** : {start_date.isoformat()}\n\n"
        f"### Checklist\n{checklist_md}\n"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/issues",
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            json={
                "title": f"Onboarding — {employee_name}",
                "body": body,
            },
        )
        response.raise_for_status()
        data = response.json()

    return data["html_url"]
