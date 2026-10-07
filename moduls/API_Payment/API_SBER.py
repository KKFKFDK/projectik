# подключаем случайные числа
import random

# шлюз оплаты через Сбер
class SberPayGateway:
    def __init__(self):
        # имя шлюза для ответа
        self.gateway_name = "SberBank API v2.4"

    def process_payment(self, amount: float) -> dict:
        # проверка лимита суммы
        if amount > 100000:
            # отказ если сумма слишком большая
            return {"success": False, "message": "Limit exceeded for Sber anonymized gateway"}

        # создаем номер операции
        tx_id = f"SBER-{random.randint(100000, 999999)}"
        # собираем успешный ответ
        return {
            # платеж прошел
            "success": True,
            # номер транзакции
            "transaction_id": tx_id,
            # через какой шлюз прошло
            "gateway": self.gateway_name,
            # сколько списали
            "amount": amount
        }
