"""Camada de persistência SQLite para o MVP do I³ APS."""

from __future__ import annotations

import hashlib
import secrets
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

DB_PATH = Path("data") / "i3_aps.db"
PBKDF2_ROUNDS = 200_000


@contextmanager
def get_connection() -> sqlite3.Connection:
    """Retorna conexão SQLite com Row Factory habilitado."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Cria tabelas necessárias, caso não existam."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_uso TEXT NOT NULL,
                infraestrutura TEXT NOT NULL,
                instituicao_nome TEXT NOT NULL,
                instituicao_tipo TEXT NOT NULL,
                finalidade TEXT NOT NULL,
                escopo_dados TEXT NOT NULL,
                uso_ia TEXT NOT NULL,
                data_inicio TEXT NOT NULL,
                data_fim TEXT NOT NULL,
                responsavel_nome TEXT NOT NULL,
                responsavel_email TEXT NOT NULL,
                concorda_lgpd INTEGER NOT NULL,
                concorda_etica INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Em análise',
                notas_admin TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                institution TEXT NOT NULL,
                user_type TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        request_columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(requests)").fetchall()
        }
        if "project_name" not in request_columns:
            conn.execute(
                "ALTER TABLE requests ADD COLUMN project_name TEXT NOT NULL DEFAULT ''"
            )
        conn.commit()


def _normalize_email(email: str) -> str:
    """Normaliza email para persistência e comparação."""
    return email.strip().lower()


def _hash_password(password: str, salt: str | None = None) -> str:
    """Gera hash seguro no formato salt$hash."""
    raw_salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        raw_salt.encode("utf-8"),
        PBKDF2_ROUNDS,
    )
    return f"{raw_salt}${digest.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    """Valida senha com comparação em tempo constante."""
    try:
        salt, expected = stored_hash.split("$", maxsplit=1)
    except ValueError:
        return False
    candidate = _hash_password(password, salt=salt).split("$", maxsplit=1)[1]
    return secrets.compare_digest(candidate, expected)


def create_user(
    *,
    name: str,
    email: str,
    institution: str,
    user_type: str,
    password: str,
) -> tuple[bool, str]:
    """Cria usuário na base e retorna status + mensagem de erro opcional."""
    normalized_email = _normalize_email(email)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (normalized_email,),
        ).fetchone()
        if existing:
            return False, "Este email já está cadastrado."

        conn.execute(
            """
            INSERT INTO users (name, email, institution, user_type, password_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name.strip(),
                normalized_email,
                institution.strip(),
                user_type.strip(),
                _hash_password(password),
                created_at,
            ),
        )
        conn.commit()
    return True, ""


def authenticate_user(email: str, password: str) -> sqlite3.Row | None:
    """Autentica usuário por email e senha."""
    normalized_email = _normalize_email(email)
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, name, email, institution, user_type, password_hash
            FROM users
            WHERE email = ?
            """,
            (normalized_email,),
        ).fetchone()

    if not row:
        return None
    if not _verify_password(password, row["password_hash"]):
        return None
    return row


def create_request(payload: dict[str, Any]) -> int:
    """Insere solicitação e retorna ID gerado."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO requests (
                project_name, tipo_uso, infraestrutura, instituicao_nome, instituicao_tipo,
                finalidade, escopo_dados, uso_ia, data_inicio, data_fim,
                responsavel_nome, responsavel_email, concorda_lgpd,
                concorda_etica, status, notas_admin, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.get("project_name", "").strip(),
                payload["tipo_uso"],
                payload["infraestrutura"],
                payload["instituicao_nome"],
                payload["instituicao_tipo"],
                payload["finalidade"],
                payload["escopo_dados"],
                payload["uso_ia"],
                payload["data_inicio"],
                payload["data_fim"],
                payload["responsavel_nome"],
                payload["responsavel_email"],
                int(payload["concorda_lgpd"]),
                int(payload["concorda_etica"]),
                "Em análise",
                payload.get("notas_admin", ""),
                created_at,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def list_requests(
    status: str | None = None,
    user_email: str | None = None,
) -> list[sqlite3.Row]:
    """Lista solicitações com filtros opcionais por status e usuário."""
    query = "SELECT * FROM requests"
    conditions: list[str] = []
    params: list[Any] = []

    if status and status != "Todos":
        conditions.append("status = ?")
        params.append(status)
    if user_email:
        conditions.append("LOWER(responsavel_email) = ?")
        params.append(_normalize_email(user_email))

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        rows = conn.execute(query, tuple(params)).fetchall()
    return rows


def get_request_by_id(request_id: int) -> sqlite3.Row | None:
    """Busca solicitação por ID."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM requests WHERE id = ?", (request_id,)).fetchone()
    return row


def update_request_status(request_id: int, status: str, notes: str) -> None:
    """Atualiza status e observações administrativas."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE requests SET status = ?, notas_admin = ? WHERE id = ?",
            (status, notes, request_id),
        )
        conn.commit()


def get_metrics() -> dict[str, int]:
    """Retorna métricas simples para a home."""
    with get_connection() as conn:
        total_requests = conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
        total_institutions = conn.execute(
            "SELECT COUNT(DISTINCT instituicao_nome) FROM requests"
        ).fetchone()[0]

    return {
        "total_requests": int(total_requests),
        "total_institutions": int(total_institutions),
    }
