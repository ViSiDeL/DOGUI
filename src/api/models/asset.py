"""
asset upload, listing, and project linkage
"""
import os
from typing import List, Dict, Any
from api.models.db import get_connection


ALLOWED_EXTENSIONS = {
    "model": ["stl", "obj", "blend", "gltf", "glb"],
    "drawing": ["dwg", "dxf", "step", "iges", "blend"],
    "image": ["png", "jpg", "jpeg", "gif"],
}


def _allowed_type(filename: str, asset_type: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS.get(asset_type, [])


class AssetService:
    @staticmethod
    def list_user_assets(username: str) -> List[Dict[str, Any]]:
        """return a list of assets visible to username (owns or public)."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT asset_url, asset_type, asset_name, user_id
                    FROM assets
                    WHERE user_id = %s OR user_id IS NULL
                    ORDER BY created_at DESC
                    """,
                    (None,)
                )
                rows = cur.fetchall()
                columns = [_desc[0] for _desc in cur.description]
                return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def upload_asset(
        asset_type: str,
        filename: str,
        asset_name: str,
        is_public: bool,
        user_id: int | None,
    ) -> int:
        """
        insert an asset row, return its generated ID.
        - if is_public, user_id will be None (public asset)
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO assets (asset_url, asset_type, asset_name, user_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (filename, asset_type, asset_name, None if is_public else user_id),
                )
                conn.commit()
                return cur.lastrowid

    @staticmethod
    def add_asset_to_project(project_id: int, asset_id: int) -> None:
        """create a row in ``project_assets`` linking the two entities."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO project_assets (project_id, asset_id) VALUES (%s, %s)",
                    (project_id, asset_id),
                )
                conn.commit()

    @staticmethod
    def get_download_path(asset_type: str, filename: str) -> str:
        """return the static folder path used for serving the asset."""
        return os.path.join("static", "assets", f"{asset_type}s", filename)