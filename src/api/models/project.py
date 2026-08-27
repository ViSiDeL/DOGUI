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

    @staticmethod
    def update_project(
        project_id: int,
        username: str,
        *,
        project_name: str | None = None,
        description: str | None = None,
        phase: str | None = None,
        init: int | None = None,
    ) -> bool:
        """ update supplied fields for a project, returns True if row was updated """
        with get_connection() as conn:
            with conn.cursor() as cur:
                set_clause_parts = []
                params = []

                if project_name is not None:
                    set_clause_parts.append("projectName = %s")
                    params.append(project_name)

                if description is not None:
                    set_clause_parts.append("description = %s")
                    params.append(description)

                if phase is not None:
                    set_clause_parts.append("phase = %s")
                    params.append(phase)

                if init is not None:
                    set_clause_parts.append("init = %s")
                    params.append(init)

                if not set_clause_parts:          # nothing to change
                    return False

                params.extend([project_id, username])

                query = (
                    f"UPDATE projects SET {', '.join(set_clause_parts)} "
                    "WHERE ID = %s AND username = %s"
                )
                cur.execute(query, params)
                conn.commit()

                return cur.rowcount == 1

    @staticmethod
    def get_contexts(
        project_id: int, username: str
    ) -> List[Dict[str, Any]]:
        """
        Return all contexts belonging to ``project_id`` that belong to ``username``.
        Result is a list of dicts: ``{'id': <context_id>, 'text': <context_text>}``,
        ordered by creation date (newest first).
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT context_id, context_text
                    FROM contexts
                    WHERE project_id = %s AND username = %s
                    ORDER BY created_at DESC
                    """,
                    (project_id, username)
                )
                rows = cur.fetchall()
                return [{"id": r["context_id"], "text": r["context_text"]} for r in rows]

    @staticmethod
    def update_context(context_id: int, context_text: str) -> bool:
        """
        Update the ``context_text`` for a given ``context_id``.
        Returns ``True`` if exactly one row was modified, otherwise ``False``.
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE contexts SET context_text = %s WHERE context_id = %s",
                    (context_text, context_id)
                )
                conn.commit()
                return cur.rowcount == 1

    @staticmethod
    def is_context_owned(context_id: int, username: str) -> bool:
        """
        Verify that the given ``context_id`` belongs to a project owned by ``username``.
        Returns ``True`` if the context exists and is owned by the user, otherwise ``False``.
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT 1 FROM contexts c
                    JOIN projects p ON c.project_id = p.ID
                    WHERE c.context_id = %s AND p.username = %s
                    """
                    , (context_id, username))
                return cur.fetchone() is not None