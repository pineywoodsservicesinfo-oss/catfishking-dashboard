#!/usr/bin/env python3
"""
Catfish King - Object Storage Manager
Handles file uploads, storage, and retrieval with security checks
"""

import sqlite3
import os
import shutil
import hashlib
import uuid
import mimetypes
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from werkzeug.utils import secure_filename

DATABASE = 'catfishking.db'
STORAGE_BASE = Path('storage')
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {
    'pdf', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx', 'xls', 'xlsx',
    'txt', 'csv', 'zip'
}


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


class StorageManager:
    """Handles file storage operations with database tracking."""

    def __init__(self, storage_base: str = 'storage'):
        self.storage_base = Path(storage_base)
        self.storage_base.mkdir(exist_ok=True)

    def _generate_uuid(self) -> str:
        """Generate unique file identifier."""
        return f"doc_{uuid.uuid4().hex[:16]}"

    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA-256 checksum of file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _get_storage_path(self, store_id: Optional[int], folder: str, filename: str) -> Path:
        """Determine physical storage path based on organization."""
        if store_id:
            base = self.storage_base / f"store_{store_id:03d}" / folder
        else:
            base = self.storage_base / "corporate" / folder
        base.mkdir(parents=True, exist_ok=True)
        return base / filename

    def _is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed."""
        ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
        return ext in ALLOWED_EXTENSIONS

    def upload_file(
        self,
        file_obj,
        folder: str,
        store_id: Optional[int] = None,
        uploaded_by: int = None,
        description: str = None,
        linked_type: str = None,
        linked_id: int = None
    ) -> Dict:
        """
        Upload and store a file.

        Args:
            file_obj: File object (e.g., Flask request.files['file'])
            folder: Target folder (e.g., 'invoices', 'disciplinary')
            store_id: Store ID for per-store files, None for corporate
            uploaded_by: User ID uploading the file
            description: Optional description
            linked_type: Optional linked record type ('transmittals', etc.)
            linked_id: Optional linked record ID

        Returns:
            Dict with file metadata or error
        """
        # Validate
        if not file_obj:
            return {'success': False, 'error': 'No file provided'}

        filename = secure_filename(file_obj.filename)
        if not filename:
            return {'success': False, 'error': 'Invalid filename'}

        if not self._is_allowed_file(filename):
            return {
                'success': False,
                'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }

        # Check file size
        file_obj.seek(0, 2)  # Seek to end
        file_size = file_obj.tell()
        file_obj.seek(0)  # Reset to beginning

        if file_size > MAX_FILE_SIZE:
            return {
                'success': False,
                'error': f'File too large. Max size: {MAX_FILE_SIZE // 1024 // 1024}MB'
            }

        # Generate storage details
        file_uuid = self._generate_uuid()
        ext = filename.rsplit('.', 1)[-1] if '.' in filename else ''
        stored_filename = f"{file_uuid}.{ext}" if ext else file_uuid

        # Determine mime type
        mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        # Physical storage path
        storage_path = self._get_storage_path(store_id, folder, stored_filename)

        try:
            # Save file
            file_obj.save(storage_path)

            # Compute checksum
            checksum = self._compute_checksum(storage_path)

            # Store metadata in database
            conn = get_db()
            c = conn.cursor()

            c.execute('''
                INSERT INTO object_storage (
                    uuid, original_filename, stored_filename, mime_type,
                    file_size, checksum, store_id, folder,
                    linked_record_type, linked_record_id,
                    storage_backend, storage_path, uploaded_by, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_uuid, filename, stored_filename, mime_type,
                file_size, checksum, store_id, folder,
                linked_type, linked_id,
                'local', str(storage_path.relative_to(self.storage_base)),
                uploaded_by, description
            ))

            file_db_id = c.lastrowid
            conn.commit()

            return {
                'success': True,
                'file_id': file_db_id,
                'uuid': file_uuid,
                'filename': filename,
                'size': file_size,
                'mime_type': mime_type,
                'url': f"/api/files/{file_uuid}"
            }

        except Exception as e:
            # Clean up if database insert fails
            if storage_path.exists():
                storage_path.unlink()
            return {'success': False, 'error': str(e)}

        finally:
            if 'conn' in locals():
                conn.close()

    def get_file(self, file_uuid: str, user_id: int = None) -> Optional[Dict]:
        """
        Retrieve file metadata and path.

        Args:
            file_uuid: The file UUID
            user_id: User requesting access (for permission check)

        Returns:
            Dict with file info or None if not found/access denied
        """
        conn = get_db()
        c = conn.cursor()

        c.execute('''
            SELECT o.*, s.name as store_name
            FROM object_storage o
            LEFT JOIN stores s ON o.store_id = s.id
            WHERE o.uuid = ? AND o.deleted_at IS NULL
        ''', (file_uuid,))

        row = c.fetchone()
        if not row:
            conn.close()
            return None

        file_info = dict(row)

        # Permission check (simplified - expand based on your auth logic)
        if user_id:
            c.execute('SELECT role, store_id FROM users WHERE id = ?', (user_id,))
            user = c.fetchone()

            if user:
                # Corporate can access all
                if user['role'] in ['corporate', 'district_manager', 'admin']:
                    pass
                # Store manager can only access their store
                elif user['role'] == 'store_manager':
                    if file_info.get('store_id') and file_info['store_id'] != user['store_id']:
                        conn.close()
                        return None

        # Log access
        c.execute('''
            INSERT INTO file_access_log (file_id, user_id, access_type, accessed_at)
            VALUES (?, ?, 'view', CURRENT_TIMESTAMP)
        ''', (file_info['id'], user_id))
        conn.commit()
        conn.close()

        # Build full path
        file_path = self.storage_base / file_info['storage_path']
        file_info['full_path'] = str(file_path.absolute())

        return file_info

    def delete_file(self, file_uuid: str, deleted_by: int) -> bool:
        """
        Soft delete a file.

        Args:
            file_uuid: File to delete
            deleted_by: User ID performing deletion

        Returns:
            True if successful
        """
        conn = get_db()
        c = conn.cursor()

        c.execute('''
            UPDATE object_storage
            SET deleted_at = CURRENT_TIMESTAMP,
                deleted_by = ?
            WHERE uuid = ? AND deleted_at IS NULL
        ''', (deleted_by, file_uuid))

        success = c.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def list_files(
        self,
        folder: str = None,
        store_id: int = None,
        linked_type: str = None,
        linked_id: int = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """List files with filters."""
        conn = get_db()
        c = conn.cursor()

        query = '''
            SELECT o.*, u.first_name || ' ' || u.last_name as uploaded_by_name,
                   s.name as store_name
            FROM object_storage o
            LEFT JOIN users u ON o.uploaded_by = u.id
            LEFT JOIN stores s ON o.store_id = s.id
            WHERE o.deleted_at IS NULL
        '''
        params = []

        if folder:
            query += ' AND o.folder = ?'
            params.append(folder)
        if store_id is not None:
            query += ' AND o.store_id = ?'
            params.append(store_id)
        if linked_type:
            query += ' AND o.linked_record_type = ?'
            params.append(linked_type)
        if linked_id:
            query += ' AND o.linked_record_id = ?'
            params.append(linked_id)

        query += ' ORDER BY o.uploaded_at DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])

        c.execute(query, params)
        rows = c.fetchall()

        conn.close()
        return [dict(row) for row in rows]

    def get_store_files_summary(self, store_id: int) -> Dict:
        """Get file count and size summary for a store."""
        conn = get_db()
        c = conn.cursor()

        c.execute('''
            SELECT folder, COUNT(*) as count, SUM(file_size) as total_size
            FROM object_storage
            WHERE store_id = ? AND deleted_at IS NULL
            GROUP BY folder
        ''', (store_id,))

        rows = c.fetchall()
        conn.close()

        summary = {}
        total_files = 0
        total_size = 0

        for row in rows:
            summary[row['folder']] = {
                'count': row['count'],
                'size_mb': round(row['total_size'] / 1024 / 1024, 2)
            }
            total_files += row['count']
            total_size += row['total_size']

        return {
            'folders': summary,
            'total_files': total_files,
            'total_size_mb': round(total_size / 1024 / 1024, 2)
        }

    def cleanup_expired_files(self, days: int = 30) -> int:
        """Hard delete files soft-deleted more than X days ago."""
        conn = get_db()
        c = conn.cursor()

        cutoff = datetime.now() - timedelta(days=days)

        c.execute('''
            SELECT uuid, storage_path
            FROM object_storage
            WHERE deleted_at < ?
        ''', (cutoff,))

        files = c.fetchall()
        deleted_count = 0

        for row in files:
            file_path = self.storage_base / row['storage_path']
            if file_path.exists():
                file_path.unlink()
                deleted_count += 1

        # Delete from database
        c.execute('DELETE FROM object_storage WHERE deleted_at < ?', (cutoff,))
        conn.commit()
        conn.close()

        return deleted_count


# Singleton instance
storage = StorageManager()


# Flask-compatible functions
def init_storage(app):
    """Initialize storage for Flask app."""
    app.storage = StorageManager()


def save_uploaded_file(*args, **kwargs):
    """Convenience function for views."""
    return storage.upload_file(*args, **kwargs)


def get_file_info(*args, **kwargs):
    """Convenience function for views."""
    return storage.get_file(*args, **kwargs)


if __name__ == '__main__':
    print("Storage Manager Test")
    print("="*60)
    print(f"Storage base: {STORAGE_BASE}")
    print(f"Max file size: {MAX_FILE_SIZE / 1024 / 1024}MB")
    print(f"Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
