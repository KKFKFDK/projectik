import random

class TBankPayGateway:
    def __init__(self):
        self.gateway_name = "T-Bank OpenAPI"

    def process_payment(self, amount: float) -> dict:
        tx_id = f"T-BANK-{random.randint(100000, 999999)}"
        return {
            "success": True,
            "transaction_id": tx_id,
            "gateway": self.gateway_name,
            "amount": amount
        }
