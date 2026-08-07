import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "database"))
from bank_database import get_connection  # noqa: E402


# ---------- STEP 1: PRIMARY KEYWORD CHECK ----------
scam_keywords = {
    "urgent": 10,"verify now": 20,"suspended": 15,"click here": 25,"limited time": 10,"act now": 10,"otp": 25,"immediately": 10,"blocked": 15,"unusual activity": 20,"final notice": 15,"act immediately": 15,
}


def keyword_check(message_body):

    matched = []
    score = 0

    text = message_body.lower()

    for keyword, weight in scam_keywords.items():
        if keyword in text:
            matched.append(keyword)
            score += weight

    score = min(score, 100)

    return matched, score


# ---------- STEP 2: DATABASE CROSS-VERIFICATION ----------
def verify_with_bank(message_id, customer_id, department, phone_number=None, timestamp=None):
    conn = get_connection()
    cursor = conn.cursor()

    # ---------- Check using Message ID ----------
    if message_id:
        cursor.execute(
            "SELECT * FROM messages WHERE message_id = ?",
            (message_id,)
        )

        row = cursor.fetchone()

        if row is None:
            conn.close()
            return {
                "verified": False,
                "reason": "Message ID not found in bank records."
            }

        # message_id, department, sent_time,
        # customer_id, phone_number, subject, status
        db_department = row[1]
        db_sent_time = row[2]
        db_customer_id = row[3]
        db_phone = row[4]

        if customer_id and customer_id != db_customer_id:
            conn.close()
            return {
                "verified": False,
                "reason": "Customer ID does not match bank records."
            }

        if department and department.lower() != db_department.lower():
            conn.close()
            return {
                "verified": False,
                "reason": "Department mismatch with bank records."
            }

        if phone_number and phone_number != db_phone:
            conn.close()
            return {
                "verified": False,
                "reason": "Phone number does not match bank records."
            }

        conn.close()
        return {
            "verified": True,
            "reason": f"Confirmed sent by {db_department} on {db_sent_time}."
        }

    # ---------- Fallback: Customer + Department ----------
    if customer_id and department:

        if phone_number:
            cursor.execute(
                """
                SELECT * FROM messages
                WHERE customer_id = ?
                AND department = ?
                AND phone_number = ?
                """,
                (customer_id, department, phone_number)
            )
        else:
            cursor.execute(
                """
                SELECT * FROM messages
                WHERE customer_id = ?
                AND department = ?
                """,
                (customer_id, department)
            )

        rows = cursor.fetchall()

        conn.close()

        if not rows:
            return {
                "verified": False,
                "reason": "No matching record found for this customer/department."
            }

        return {
            "verified": True,
            "reason": f"Matched a record from {department} for this customer."
        }

    conn.close()

    return {
        "verified": False,
        "reason": "Not enough information to cross-verify."
    }

# ---------- FULL PIPELINE ----------
def full_verification(
    message_body,
    sender_id,
    phone_number,
    timestamp,
    message_id=None,
    customer_id=None,
    department=None,
):
    """
    Combines AI analysis with database verification.
    """

    keyword_hits, ai_risk = keyword_check(message_body)

    db_result = verify_with_bank(
        message_id,
        customer_id,
        department,
        phone_number,
        timestamp
    )

    # Database verification takes precedence
    if db_result["verified"]:
        final_verdict = "VERIFIED"
        confidence_score = 99

    else:
        if ai_risk >= 80:
            final_verdict = "BLOCKED"
            confidence_score = 99

        elif ai_risk >= 60:
            final_verdict = "BLOCKED"
            confidence_score = 95

        elif ai_risk >= 40:
            final_verdict = "SUSPICIOUS"
            confidence_score = 80

        elif ai_risk >= 20:
            final_verdict = "SUSPICIOUS"
            confidence_score = 65

        else:
            final_verdict = "SUSPICIOUS"
            confidence_score = 50

    return {
        "keyword_hits": keyword_hits,
        "ai_risk_score": ai_risk,
        "confidence_score": confidence_score,
        "db_check": db_result,
        "final_verdict": final_verdict,
    }