# подключаем нужные модули системы
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

# добавляем папку проекта в пути поиска
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# подключаем платежи погоду и сервер
from moduls.API_Payment.API_SBER import SberPayGateway
from moduls.API_Payment.API_T import TBankPayGateway
from moduls.Open_weather.API_Weather import WeatherMonitor
from moduls.SERVER_api_SELECTEL.connect import SelectelServerConnector

# обработчик запросов к локальному серверу
class BankSimulatorHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # разрешаем доступ с любой страницы
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        # отдача настроек сервера
        if self.path == '/api/config':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            connector = SelectelServerConnector()
            self.wfile.write(json.dumps(connector.load_configuration()).encode('utf-8'))
        # отдача текущей погоды
        elif self.path == '/api/weather':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            monitor = WeatherMonitor()
            self.wfile.write(json.dumps(monitor.get_current_weather()).encode('utf-8'))
        else:
            # главная страница сайта
            if self.path == '/' or self.path == '':
                self.path = '/core/HTML/HTML/index.html'
            elif self.path.startswith('/core/HTML/'):
                pass
            else:
                # ищем файлы стилей и скриптов
                cleaned_path = self.path.lstrip('/')
                if os.path.exists(os.path.join('core', 'HTML', cleaned_path)):
                    self.path = f'/core/HTML/{cleaned_path}'
            return super().do_GET()

    def do_POST(self):
        # обработка платежа с формы
        if self.path == '/api/pay':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            bank = data.get('bank')
            amount = float(data.get('amount', 0))

            # выбираем банк для оплаты
            if bank == 'SBER':
                gateway = SberPayGateway()
                result = gateway.process_payment(amount)
            elif bank == 'TINKOFF':
                gateway = TBankPayGateway()
                result = gateway.process_payment(amount)
            else:
                result = {"success": False, "message": "Unknown gateway"}

            # отправляем ответ клиенту
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=BankSimulatorHandler, port=8000):
    # запускаем сервер на порту 8000
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер симулятора банка запущен на http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

# старт программы если файл запущен напрямую
if __name__ == '__main__':
    run()
