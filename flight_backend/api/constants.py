BOOKED = "BOOKED"
RESERVED = "RESERVED"
YES = "YES"
NO = "NO"

STATUS = ((BOOKED, "Booked"), (RESERVED, "Reserved"))

ECONOMY = "ECONOMY"
BUSINESS = "BUSINESS"
CLASS = ((ECONOMY, "Economy"), (BUSINESS, "Business"))
AVAILABLE = "AVAILABLE"
DELAYED = "DELAYED"
ARRIVED = "ARRIVED"
CANCELLED = "CANCELLED"
DEPARTED = "DEPARTED"
LANDED = "LANDED"

FLIGHT_STATUS = (
    (AVAILABLE, "Available"),
    (DELAYED, "Delayed"),
    (ARRIVED, "Arrived"),
    (CANCELLED, "Cancelled"),
    (DEPARTED, "Departed"),
    (LANDED, "Landed"),
)

STATUSES = (AVAILABLE, DEPARTED, DELAYED, CANCELLED, LANDED, ARRIVED)

EMAIL_REGEX = "^([0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*@([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9})$"  # noqa: W605
EMAIL_MESSAGE = "Please enter a valid email address"
PASSWORD_REGEX = (
    "^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)(?=.*[@#$%*^&+=]+.*)[0-9a-zA-Z@#$%*^&+=]{8,}$"
)
PASSWORD_MESSAGE = (
    "Password must be at least 8 characters long,"
    "it must contain a letter, number and special character"
)
