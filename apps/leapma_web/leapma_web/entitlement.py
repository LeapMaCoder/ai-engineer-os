"""Entitlement — free core loop must never be paywalled (AC-04 / D-031)."""

from __future__ import annotations

FREE_CORE_CAPABILITIES = frozenset(
    {
        "orientation",
        "action",
        "feedback",
        "progress",
    }
)


def ensure_core_allowed(capability: str, *, is_paid: bool = False) -> None:
    """Raise only if someone mistakenly gates a free-core capability behind pay.

    Unpaid and paid users both get FREE_CORE_CAPABILITIES. Paid flag is ignored
    for core capabilities (enhancements are Later / out of this slice).
    """
    if capability in FREE_CORE_CAPABILITIES:
        return
    if not is_paid:
        raise PermissionError(f"Capability '{capability}' is not in free core loop")
