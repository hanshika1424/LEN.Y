import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bank_database.db")


def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            department TEXT NOT NULL,
            sent_time TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            subject TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    sample_data = [
        ("MSG001", "OTP Service", "2026-08-04 10:15", "C1023", "9876543210", "OTP Verification", "Sent"),
        ("MSG002", "Loans", "2026-08-04 11:20", "C4821", "9123456780", "Loan Approval", "Sent"),
        ("MSG003", "Credit Cards", "2026-08-04 12:05", "C9012", "9988776655", "Card Statement Ready", "Sent"),
        ("MSG004", "KYC", "2026-08-04 09:30", "C3345", "9871234560", "KYC Update Required", "Sent"),
        ("MSG005", "Fraud Alert", "2026-08-04 13:45", "C5567", "9012345678", "Suspicious Login Attempt", "Sent"),
        ("MSG006", "Account Services", "2026-08-04 14:10", "C6789", "9345678901", "Account Balance Update", "Sent"),
        ("MSG007", "Fund Transfer", "2026-08-04 15:00", "C7890", "9456789012", "Fund Transfer Confirmation", "Sent"),
        ("MSG008", "Password Reset", "2026-08-04 08:50", "C8901", "9567890123", "Password Reset Request", "Sent"),
        ("MSG009", "Insurance", "2026-08-04 16:20", "C1122", "9678901234", "Insurance Premium Due", "Sent"),
        ("MSG010", "Loyalty Program", "2026-08-04 17:05", "C2233", "9789012345", "Reward Points Credited", "Sent")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO messages
        (message_id, department, sent_time, customer_id, phone_number, subject, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_data)

    conn.commit()
    conn.close()


def get_connection():
    """Used by the backend to open a connection to the same database file."""
    return sqlite3.connect(DB_PATH)


if __name__ == "__main__":
    create_database()
    print(f"Database created/verified at: {DB_PATH}")
    print("Inserted 10 sample records.")