from mcp.server.fastmcp import FastMCP  # type: ignore[reportMissingImports]
import json

mcp = FastMCP("WanderBot Booking Tools")

BOOKINGS = {
    "BK-1001": {
        "booking_ref": "BK-1001",
        "customer": "Alice Johnson",
        "email": "alice@example.com",
        "flight": "HZ-101",
        "route": "LHR → CDG",
        "date": "2026-03-15",
        "cabin": "Economy Flex",
        "fare_usd": 189.99,
        "status": "CONFIRMED",
    },
    "BK-1002": {
        "booking_ref": "BK-1002",
        "customer": "Alice Johnson",
        "email": "alice@example.com",
        "flight": "HZ-450",
        "route": "BCN → FCO",
        "date": "2026-03-20",
        "cabin": "Economy Lite",
        "fare_usd": 145.00,
        "status": "CONFIRMED",
    },
    "BK-1003": {
        "booking_ref": "BK-1003",
        "customer": "Bob Smith",
        "email": "bob@example.com",
        "flight": "HZ-311",
        "route": "JFK → LAX",
        "date": "2026-03-15",
        "cabin": "Business",
        "fare_usd": 349.00,
        "status": "CONFIRMED",
    },
}


@mcp.tool()
def get_booking(booking_ref: str) -> str:
    """Retrieve full details for a booking reference."""
    booking = BOOKINGS.get(booking_ref.upper())

    if not booking:
        return f"No booking found with reference {booking_ref}."

    return json.dumps(booking)


@mcp.tool()
def list_bookings_by_email(email: str) -> str:
    """List all bookings associated with a customer email."""
    matches = [
        booking
        for booking in BOOKINGS.values()
        if booking["email"].lower() == email.lower()
    ]

    if not matches:
        return f"No bookings found for {email}."

    return json.dumps({
        "email": email,
        "bookings": matches
    })


if __name__ == "__main__":
    mcp.run(transport="stdio")
