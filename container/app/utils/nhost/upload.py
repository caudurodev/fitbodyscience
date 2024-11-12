""" Utility functions for uploading files to Nhost storage. """

import os
import uuid
import json
import mimetypes
import requests
from requests.structures import CaseInsensitiveDict
from ..config import settings, logger


def get_file_content_and_type(file_path):
    """Get file content and MIME type, handling both URLs and local file paths."""
    if is_url(file_path):
        response = requests.get(file_path, timeout=15)
        if response.status_code == 200:
            content = response.content
        else:
            response.raise_for_status()
    else:
        with open(file_path, "rb") as file:
            content = file.read()

    mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    return content, mime_type


def upload_files_to_nhost(bucket_id, file_paths, user_id=None):
    """Upload files (from URLs or local paths) to Nhost storage bucket."""
    # ##logger.info("Uploading files to Nhost bucket %s", bucket_id)
    # ##logger.info("Uploading files: %s", file_paths)
    # ##logger.info("User ID: %s", user_id)
    storage_url = f"{settings.STORAGE_URL}/files"

    multipart_form_data = []
    try:
        for file_path in file_paths:
            file_content, mime_type = get_file_content_and_type(file_path)
            filename = os.path.basename(file_path)
            unique_filename = f"{uuid.uuid4()}_{filename}"

            multipart_form_data.extend(
                [
                    ("file[]", (unique_filename, file_content, mime_type)),
                    (
                        "metadata[]",
                        (
                            None,
                            json.dumps(
                                {
                                    "id": str(uuid.uuid4()),
                                    "name": unique_filename,
                                    "metadata": {
                                        "uploadedByUserId": user_id or "admin"
                                    },
                                }
                            ),
                            "application/json",
                        ),
                    ),
                ]
            )

        multipart_form_data.append(("bucket-id", (None, bucket_id)))
        multipart_form_data.append(("uploadedByUserId", (None, user_id or "admin")))

        headers = CaseInsensitiveDict(
            {
                "x-hasura-admin-secret": settings.HASURA_ADMIN_SECRET,
            }
        )

        response = requests.post(
            storage_url, files=multipart_form_data, headers=headers, timeout=10
        )
        # logger.info("upload_files_to_nhost Response: %s", response)

        if response.ok:
            response_data = response.json()
            processed_files = response_data.get("processedFiles", [])
            # ##logger.info("Successfully uploaded files: %s", processed_files)
            return processed_files
        else:
            logger.error("Failed to upload files: %s", response.text)
            response.raise_for_status()
    except Exception as e:
        logger.error("Error uploading files: %s", e)
        return []  # Return an empty list to ensure the return type is consistent

    return []  # Ensure consistent return type


def download_file_from_url(url):
    """Download a file from a given URL."""
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
        return response.content
    else:
        response.raise_for_status()


def is_url(path):
    """Check if the given path is a URL."""
    return path.startswith("http://") or path.startswith("https://")
