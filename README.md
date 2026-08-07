## ZeroTrust

ZeroTrust is a prototype developed to help users verify whether a bank SMS is genuine before acting on it.

Instead of asking users to judge a message based on grammar, links, or visual appearance, ZeroTrust verifies whether the bank actually sent the notification by comparing extracted metadata with the bank's records.

Our goal is simple:

Don't guess whether a message looks real. Verify whether it actually is.

## Problem Statement

SMS phishing (Smishing) has become increasingly difficult to detect.

Modern scam messages often:
- use perfect grammar
- imitate official bank sender names
- create urgency
- closely resemble genuine banking notifications

As AI-generated scams become more convincing, traditional advice like "look for spelling mistakes" is becoming less effective.

## Our Solution

ZeroTrust follows a multi-layer verification approach.

1. User shares or pastes a suspicious SMS.
2. The application extracts available metadata and structured information.
3. A primary AI risk check searches for suspicious language.
4. The extracted metadata is cross-verified against the bank's notification records.
5. The system combines both results to produce:
   - VERIFIED
   - SUSPICIOUS
   - BLOCKED

A confidence score is also generated to indicate how certain the system is about its decision so that we are transparent with our user.

## How the Prototype Works

For demonstration purposes, the prototype uses:

- HTML
- CSS
- JavaScript
- Python
- Flask
- SQLite

The SQLite database simulates the notification records maintained by a bank.
Instead of connecting to a real bank, our prototype verifies messages against this mock database.
## Technologies Used

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- SQLite
## Future Implementation

In a production deployment:

- Users would share suspicious SMS directly from their messaging application.
- ZeroTrust would automatically extract available metadata (such as sender ID and timestamp) after receiving user permission.
- Verification would occur through a secure Bank Verification API instead of direct database access.
- The bank would return only a simple **Yes/No** verification response without exposing customer information.


## What Makes ZeroTrust Different?

Most existing SMS fraud detection solutions rely primarily on:

- AI text classification
- spam keyword detection
- URL analysis
- sender reputation
- machine learning models

These methods estimate whether a message **looks suspicious**.
ZeroTrust takes a different approach.

Instead of asking:

"Does this message look genuine?"

we ask:

"Did the bank actually send this notification?"

This shifts verification from appearance-based detection to direct confirmation using trusted banking records.

Even if scammers create a message that looks identical to a genuine bank notification, the system can still detect it because the bank cannot verify that it originated from its own records.

## Privacy

ZeroTrust is designed with privacy in mind.

- Only the minimum information required for verification is processed.
- The prototype does not permanently store user phone numbers or message content.
- In a real deployment, verification would be performed over an encrypted API connection.
- Customer data would remain inside the bank's infrastructure.

---

## Limitations

This project is a proof-of-concept prototype.

Current limitations include:

- Uses a simulated bank database.
- Uses a rule-based keyword detector instead of a trained AI model.
- Metadata extraction is demonstrated using structured sample messages.
- Does not yet integrate directly with mobile SMS applications.

These limitations are expected to be addressed in future development.

---

## Team

**Team LenY**

International Innovation Challenge (IIC)

Project: **ZeroTrust**
