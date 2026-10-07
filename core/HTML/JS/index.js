//список событий документа
document.addEventListener('DOMContentLoaded', () => {
    const logConsole = document.getElementById('log-console');
    const balanceAmount = document.getElementById('balance-amount');
    const paymentForm = document.getElementById('payment-form');
    let currentBalance = 50000;

    function addLog(message) {
        const timestamp = new Date().toLocaleTimeString();
        logConsole.innerHTML += `[${timestamp}] ${message}<br>`;
        logConsole.scrollTop = logConsole.scrollHeight;
    }
    //симуляция подключения к серверу
    async function fetchServerConfig() {
        try {
            addLog("Запрос конфигурации с SERVER_api_SELECTEL...");
            const response = await fetch('/api/config');
            const config = await response.json();
            addLog(`Сервер подключен к: ${config.server_url} (Окружение: ${config.environment})`);
        } catch (e) {
            addLog("Использование локальной эмуляции конфигурации сервера.");
        }
    }
    //подключение и обновление погоды
    async function updateWeather() {
        try {
            const response = await fetch('/api/weather');
            const data = await response.json();
            document.getElementById('weather-display').innerText = `Москва: ${data.temp}°C, ${data.condition}`;
            addLog("Данные Open_weather успешно обновлены.");
        } catch (e) {
            document.getElementById('weather-display').innerText = `Москва: +18°C, Облачно`;
        }
    }

    paymentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const bank = document.getElementById('bank-select').value;
        const amount = parseFloat(document.getElementById('amount-input').value);

        if (amount > currentBalance) {
            addLog(`Ошибка: Недостаточно средств для списания ${amount} ₽`);
            return;
        }

        addLog(`Инициализация шлюза API_Payment для ${bank}...`);
        
        try {
            const response = await fetch('/api/pay', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ bank, amount })
            });
            const result = await response.json();

            if (result.success) {
                currentBalance -= amount;
                balanceAmount.innerText = `${currentBalance.toLocaleString('ru-RU')}.00 ₽`;
                addLog(`Транзакция одобрена. ID: ${result.transaction_id}. Списано: ${amount} ₽ через ${result.gateway}`);
            } else {
                addLog(`Ошибка шлюза: ${result.message}`);
            }
        } catch (error) {
            currentBalance -= amount;
            balanceAmount.innerText = `${currentBalance.toLocaleString('ru-RU')}.00 ₽`;
            const mockId = Math.floor(Math.random() * 900000) + 100000;
            addLog(`[Эмуляция клиента] Успешный платеж через API_${bank}. ID: TX-${mockId}. Списано: ${amount} ₽`);
        }
        document.getElementById('amount-input').value = '';
    });

    fetchServerConfig();
    updateWeather();
});
