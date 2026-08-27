"""
projects - contexts and asset associations
"""
from typing import List, Dict, Any
from pymysql import cursors
from api.models.db import get_connection


class ProjectService:
    @staticmethod
    def list_projects(username: str) -> List[Dict[str, Any]]:
        """return a list of projects belonging to username"""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT projectName, description, ID, phase, created_at, last_edited
                    FROM projects
                    WHERE username = %s
                    """,
                    (username,)
                )
                rows = cur.fetchall()
                columns = [_desc[0] for _desc in cur.description]
                return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def create_project(username: str, description: str = None) -> int:
        """insert new project, return the generated ID."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO projects (username, description) VALUES (%s, %s)",
                    (username, description or "")
                )
                conn.commit()
                return cur.lastrowid

    @staticmethod
    def add_context(project_id: int, context_text: str) -> int:
        """insert new context entry, return its ID."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO contexts (project_id, context_text) VALUES (%s, %s)",
                    (project_id, context_text)
                )
                conn.commit()
                return cur.lastrowid

    @staticmethod
    def get_project_with_contexts(
        project_id: int, username: str
    ) -> Dict[str, Any]:
        """ load a project with its contexts. """
        with get_connection() as conn:
            with conn.cursor(cursors.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT p.*,
                    GROUP_CONCAT(c.context_text, '|||', c.context_id SEPARATOR ';;;') AS contexts_data
                    FROM projects p
                    LEFT JOIN contexts c ON p.ID = c.project_id
                    WHERE p.ID = %s AND p.username = %s
                    GROUP BY p.ID
                    """,
                    (project_id, username)
                )
                project_data = cur.fetchone()
                if not project_data:
                    return {}

                # Parse the concatenated context data back into a list.
                contexts = []
                ctx_data = project_data.pop("contexts_data")
                if ctx_data:
                    for item in ctx_data.split(";;;"):
                        if "|||" in item:
                            cid, txt = item.split("|||")
                            contexts.append({"id": int(cid), "text": txt})

                # Populate a placeholder for assets – can be filled later.
                project_data.update(
                    {
                        "contexts": contexts,
                        "assets": [],
                        "available_assets": [],
                    }
                )
                return project_data

    @staticmethod
    def add_asset_to_project(project_id: int, asset_id: int) -> None:
        """Create a linking row in ``project_assets``."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO project_assets (project_id, asset_id) VALUES (%s, %s)",
                    (project_id, asset_id)
                )
                conn.commit()