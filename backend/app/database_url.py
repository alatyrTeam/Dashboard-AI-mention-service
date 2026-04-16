from __future__ import annotations

import typing

from sqlalchemy.engine import make_url


def normalize_postgresql_url(database_url: str, *, port: typing.Optional[int] = None) -> str:
    url = make_url(database_url)
    if url.get_backend_name() != "postgresql":
        return database_url

    if not url.drivername.startswith("postgresql+psycopg"):
        url = url.set(drivername="postgresql+psycopg")

    if port is not None and url.host is not None:
        url = url.set(port=port)

    return url.render_as_string(hide_password=False)
