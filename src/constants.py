from __future__ import annotations

from typing import Literal

MCP_SERVER_NAME = "mcp-gateway"

LEAVE_API_BASE_URL = (
    "https://leave-management-api-493458094930.asia-south1.run.app"
)
HTTP_DEFAULT_TIMEOUT = 30.0

AUTH_HEADER = "Authorization"
BEARER_SCHEME = "Bearer"
ACCESS_TOKEN_KEY = "access_token"

class Routes:
    """Leave Management API paths. Templates use ``str.format(...)``."""

    REGISTER = "/auth/register"
    LOGIN = "/auth/login"

    LEAVES = "/leaves"
    LEAVE_SUMMARY = "/leaves/summary"

    ADMIN_CREATE_FOR_USER = "/leaves/admin/create-for-user"
    ADMIN_PENDING = "/leaves/admin/pending"
    ADMIN_APPROVE = "/leaves/admin/{leave_id}/approve"
    ADMIN_REJECT = "/leaves/admin/{leave_id}/reject"
    ADMIN_MAKE_ADMIN = "/leaves/admin/users/{user_email}/make-admin"
    ADMIN_USERS = "/leaves/admin/users"
    ADMIN_USER_BALANCES = "/leaves/admin/user-balances"
    ADMIN_USER_BALANCE = "/leaves/admin/user-balances/{user_email}"


LeaveType = Literal["CL", "SL", "EL"]
DayType = Literal["full_day", "half_day"]
HalfDaySlot = Literal["first_half", "second_half"]


BALANCE_CL = "CL"
BALANCE_SL = "SL"
BALANCE_EL = "EL"
