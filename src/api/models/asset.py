"""
asset upload, listing, and project linkage
"""
import os
import uuid
from typing import List, Dict, Any, Optional

from flask import url_for

from werkzeug.utils import secure_filename

from google.cloud import storage

from api.models.db import get_connection
from api.models.config import ASSET_BACKEND, ASSET_BUCKET


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
        file_obj: Any,
        asset_name: str,
        is_public: bool,
        user_id: Optional[int],
    ) -> int:
        """
        insert an asset row, return its generated ID.

        - if cloud stream to Google Cloud Storage bucket
        - if local write to static/ folder.
        """
        if ASSET_BACKEND == "cloud":
            return AssetService._upload_to_cloud(
                asset_type, file_obj, asset_name, is_public, user_id
            )
        else:
            return AssetService._upload_locally(
                asset_type, file_obj, asset_name, is_public, user_id
            )

    @staticmethod
    def _upload_locally(
        asset_type: str,
        file_obj: Any,
        asset_name: str,
        is_public: bool,
        user_id: Optional[int],
    ) -> int:
        """write to static/assets/<type>/ """
        upload_folder = os.path.join(
            os.path.dirname(__file__), "..", "..", "static", "assets", f"{asset_type}s"
        )
        os.makedirs(upload_folder, exist_ok=True)

        if not os.path.splitext(asset_name)[1]:  # no extension, generate uuid
            asset_name = f"{uuid.uuid4().hex}{uuid.filesafe}.tmp"

        filename = secure_filename(asset_name)
        save_path = os.path.join(upload_folder, filename)

        with open(save_path, "wb") as dst:
            for chunk in file_obj.stream.iter_chunks():
                dst.write(chunk)

        asset_url = filename

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO assets (asset_url, asset_type, asset_name, user_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (asset_url, asset_type, asset_name, None if is_public else user_id),
                )
                conn.commit()
                return cur.lastrowid

    @staticmethod
    def _upload_to_cloud(
        asset_type: str,
        file_obj: Any,
        asset_name: str,
        is_public: bool,
        user_id: Optional[int],
    ) -> int:
        """ stream to Cloud Storage """
        if not ASSET_BUCKET:
            raise RuntimeError("ASSET_BUCKET env‑var is required for cloud backend")

        client = storage.Client()
        bucket = client.bucket(ASSET_BUCKET)

        object_name = f"uploads/{uuid.uuid4().hex}"
        if asset_name and not os.path.isdir(asset_name):
            object_name = f"uploads/{uuid.clean_name(asset_name)}"

        blob = bucket.blob(object_name)
        blob.upload_from_file(file_obj.stream, content_type="application/octet-stream")

        if is_public:
            blob.make_public()

        asset_url = object_name
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO assets (asset_url, asset_type, asset_name, user_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (asset_url, asset_type, asset_name, None if is_public else user_id),
                )
                conn.commit()
                return cur.lastrowid

    @staticmethod
    def get_download_url(identifier: str, asset_type: str) -> str:
        """
        return a URL that can be used to download the asset.

        - when cloud, gen signed URL (valid for 5 minutes).
        - when local, return static path
        """
        if ASSET_BACKEND == "cloud":
            client = storage.Client()
            bucket = client.bucket(ASSET_BUCKET)
            blob = bucket.blob(identifier)
            return blob.generate_signed_url(
                expiration=300, method="GET"
            )
        else:
            return url_for(
                "static",
                filename=f"assets/{asset_type}s/{identifier}",
                _external=True,
            )