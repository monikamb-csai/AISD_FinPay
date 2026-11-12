from database import get_connection

class PaymentService:
    """Business rules for demo transfers. No real money is moved."""

    def transfer(self, sender_id, recipient_email, amount):
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")
        if round(amount, 2) != amount:
            raise ValueError("Enter an amount with at most two decimal places.")

        with get_connection() as conn:
            conn.execute("BEGIN IMMEDIATE")
            sender = conn.execute(
                "SELECT id, balance FROM users WHERE id = ?", (sender_id,)
            ).fetchone()
            receiver = conn.execute(
                "SELECT id FROM users WHERE email = ?", (recipient_email,)
            ).fetchone()

            if not sender or not receiver:
                raise ValueError("Sender or recipient account was not found.")
            if sender_id == receiver["id"]:
                raise ValueError("You cannot transfer money to your own account.")
            if sender["balance"] < amount:
                raise ValueError("Insufficient demo balance.")

            conn.execute("UPDATE users SET balance = balance - ? WHERE id = ?",
                         (amount, sender_id))
            conn.execute("UPDATE users SET balance = balance + ? WHERE id = ?",
                         (amount, receiver["id"]))
            conn.execute("""
                INSERT INTO transactions(sender_id, receiver_id, amount, note)
                VALUES (?, ?, ?, ?)
            """, (sender_id, receiver["id"], amount, "FinPay demo transfer"))

        return "Demo transfer completed successfully."
