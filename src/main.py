"""MCP Gateway for the Leave Management REST API.

Each ``@mcp.tool()`` wraps a single upstream endpoint. ``login_user`` captures
the JWT returned by the API so every subsequent authenticated call attaches
the correct ``Authorization`` header automatically.
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from constants import (
    ACCESS_TOKEN_KEY,
    BALANCE_CL,
    BALANCE_EL,
    BALANCE_SL,
    MCP_SERVER_NAME,
    DayType,
    HalfDaySlot,
    LeaveType,
    Routes,
)
from request_handler import api

mcp = FastMCP(MCP_SERVER_NAME)



@mcp.tool()
async def register_user(name: str, email: str, password: str) -> Any:
    """Register a new employee account (default balances CL=12, SL=10, EL=15)."""
    return await api.post(
        Routes.REGISTER,
        json={"name": name, "email": email, "password": password},
        auth=False,
    )


@mcp.tool()
async def login_user(login: str, password: str) -> Any:
    """Authenticate with email/username and cache the JWT for later calls."""
    result = await api.post(
        Routes.LOGIN,
        json={"login": login, "password": password},
        auth=False,
    )
    if isinstance(result, dict) and result.get(ACCESS_TOKEN_KEY):
        api.set_token(result[ACCESS_TOKEN_KEY])
    return result


@mcp.tool()
async def apply_leave(
    start_date: str,
    end_date: str,
    reason: str,
    leave_type: LeaveType,
    day_type: DayType,
    half_day_slot: HalfDaySlot | None = None,
) -> Any:
    """Submit a new leave request (pending) for the current user."""
    return await api.post(
        Routes.LEAVES,
        json={
            "start_date": start_date,
            "end_date": end_date,
            "reason": reason,
            "leave_type": leave_type,
            "day_type": day_type,
            "half_day_slot": half_day_slot,
        },
    )


@mcp.tool()
async def list_my_leaves() -> Any:
    """List all leave requests belonging to the current user."""
    return await api.get(Routes.LEAVES)


@mcp.tool()
async def get_leave_summary() -> Any:
    """Get the current user's available balances and full leave history."""
    return await api.get(Routes.LEAVE_SUMMARY)



@mcp.tool()
async def admin_create_leave_for_user(
    user_email: str,
    start_date: str,
    end_date: str,
    reason: str,
    leave_type: LeaveType,
    day_type: DayType,
    half_day_slot: HalfDaySlot | None = None,
) -> Any:
    """Admin: create an already-approved leave on behalf of another user."""
    return await api.post(
        Routes.ADMIN_CREATE_FOR_USER,
        json={
            "user_email": user_email,
            "start_date": start_date,
            "end_date": end_date,
            "reason": reason,
            "leave_type": leave_type,
            "day_type": day_type,
            "half_day_slot": half_day_slot,
        },
    )


@mcp.tool()
async def admin_list_pending_leaves() -> Any:
    """Admin: list every pending leave request across all users."""
    return await api.get(Routes.ADMIN_PENDING)


@mcp.tool()
async def admin_approve_leave(leave_id: str) -> Any:
    """Admin: approve a pending leave request and deduct balance."""
    return await api.patch(Routes.ADMIN_APPROVE.format(leave_id=leave_id))


@mcp.tool()
async def admin_reject_leave(leave_id: str) -> Any:
    """Admin: reject a pending leave request."""
    return await api.patch(Routes.ADMIN_REJECT.format(leave_id=leave_id))


@mcp.tool()
async def admin_make_user_admin(user_email: str) -> Any:
    """Admin: promote an existing user to the admin role."""
    return await api.patch(Routes.ADMIN_MAKE_ADMIN.format(user_email=user_email))


@mcp.tool()
async def admin_list_users() -> Any:
    """Admin: list every user's email, name, and role."""
    return await api.get(Routes.ADMIN_USERS)


@mcp.tool()
async def admin_list_user_balances() -> Any:
    """Admin: list every non-admin user's remaining leave balances."""
    return await api.get(Routes.ADMIN_USER_BALANCES)


@mcp.tool()
async def admin_update_user_balance(
    user_email: str, cl: float, sl: float, el: float
) -> Any:
    """Admin: overwrite a user's CL/SL/EL balances with absolute values."""
    return await api.patch(
        Routes.ADMIN_USER_BALANCE.format(user_email=user_email),
        json={
            "leave_balance": {
                BALANCE_CL: cl,
                BALANCE_SL: sl,
                BALANCE_EL: el,
            }
        },
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
