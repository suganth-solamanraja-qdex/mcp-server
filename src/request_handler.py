"""Async HTTP client for the Leave Management REST API.

Holds the JWT obtained from ``/auth/login`` and attaches it as
``Authorization: Bearer <token>`` on subsequent authenticated calls.
"""

from __future__ import annotations

from typing import Any

import httpx

from constants import (
    AUTH_HEADER,
    BEARER_SCHEME,
    HTTP_DEFAULT_TIMEOUT,
    LEAVE_API_BASE_URL,
)


class LeaveAPIError(RuntimeError):
    """Raised when the upstream Leave Management API returns a non-2xx response."""

    def __init__(self, status_code: int, detail: Any) -> None:
        super().__init__(f"Leave API {status_code}: {detail}")
        self.status_code = status_code
        self.detail = detail


class LeaveAPIClient:
    """Thin wrapper around ``httpx.AsyncClient`` with JWT auth."""

    def __init__(
        self,
        base_url: str = LEAVE_API_BASE_URL,
        timeout: float = HTTP_DEFAULT_TIMEOUT,
    ) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)
        self._token: str | None = None

    async def aclose(self) -> None:
        await self._client.aclose()

    # ---- auth ----

    def set_token(self, token: str | None) -> None:
        self._token = token

    def _auth_headers(self) -> dict[str, str]:
        if not self._token:
            return {}
        return {AUTH_HEADER: f"{BEARER_SCHEME} {self._token}"}

    # ---- core ----

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        auth: bool = True,
    ) -> Any:
        headers = self._auth_headers() if auth else {}
        response = await self._client.request(method, path, json=json, headers=headers)

        if response.is_error:
            try:
                detail: Any = response.json()
            except ValueError:
                detail = response.text
            raise LeaveAPIError(response.status_code, detail)

        if response.status_code == 204 or not response.content:
            return None

        if "application/json" in response.headers.get("content-type", ""):
            return response.json()
        return response.text

    # ---- convenience verbs ----

    async def get(self, path: str, *, auth: bool = True) -> Any:
        return await self.request("GET", path, auth=auth)

    async def post(
        self, path: str, *, json: Any | None = None, auth: bool = True
    ) -> Any:
        return await self.request("POST", path, json=json, auth=auth)

    async def patch(
        self, path: str, *, json: Any | None = None, auth: bool = True
    ) -> Any:
        return await self.request("PATCH", path, json=json, auth=auth)


api = LeaveAPIClient()
