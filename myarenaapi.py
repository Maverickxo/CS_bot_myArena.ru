import requests

base_url = "https://www.myarena.ru/api.php"


class MyApiArena:
    def __init__(self, token):
        self.base_url = base_url
        self.token = token

    def auth_server_user(self, query_param):
        url = f"{self.base_url}?query={query_param}&token={self.token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к API: {e}")
            return None

    def get_server_info(self):
        user_count = 1
        result = self.auth_server_user('status')

        if result:
            server_data = result.get('data', {}).get('s', {})
            online, server_id, server_address, server_location, server_type = (
                result.get('online'),
                result.get('server_id'),
                result.get('server_address'),
                result.get('server_location'),
                result.get('server_type')
            )

            status_message = (
                "offline" if online == 0
                else "online" if online == 1
                else "Запускается или завис"
            )

            server_info = (
                "Информация о сервере:\n\n"
                f"ID сервера: {server_id}\n"
                f"Статус сервера: {status_message}\n"
                f"Адрес сервера: {server_address}\n"
                f"Название Локации: {server_location}\n"
                f"Текущая карта: {server_data.get('map')}\n"
                f"Название сервера: {server_data.get('name')}\n"
                f"Играют на сервере: {server_data.get('players')}\n\n"

            )

            players_list = result.get('data', {}).get('p', [])

            if players_list:
                for player in players_list:
                    player_name = player.get('name')
                    player_score = player.get('score')
                    player_time = player.get('time')
                    server_info += (
                        f"{user_count}.Ник: {player_name}, Счет: {player_score}, Время игры: {player_time}\n"
                        # f"Выделенные ресурсы: {server_type}\n"
                    )
                    user_count += 1
            else:
                server_info += "\n"  # На сервере нет игроков.

            print(server_info)
            return server_info
        else:
            print("Не удалось получить информацию о сервере.")
            return "Не удалось получить информацию о сервере."

    def get_server_resources(self):
        result = self.auth_server_user('getresources')
        if result:
            cpu_proc, mem_used, mem_quota, mem_proc, players, disk_used, disk_quota, disk_proc, players_max, = (
                result.get('cpu_proc'),
                result.get('mem_used'),
                result.get('mem_quota'),
                result.get('mem_proc'),
                result.get('players'),
                result.get('disk_used'),
                result.get('disk_quota'),
                result.get('disk_proc'),
                result.get('players_max')
            )

            output_info = (
                "Информация о ресурсах:\n\n"
                f"CPU: {cpu_proc}%\n"
                f"Использовано оперативной памяти (в мегабайтах): {mem_used} MB\n"
                f"Выделено оперативной памяти (в мегабайтах): {mem_quota} MB\n"
                f"Использование памяти в процентах: {mem_proc} %\n"
                f"Использовано дисковой квоты (в мегабайтах): {int(disk_used)} MB\n"
                f"Выделено дисковой квоты (в мегабайтах): {int(disk_quota)} MB\n"
                f"Использование дисковой квоты в процентах: {disk_proc} %\n"
                f"Количество игроков/Максимальное количество слотов: {players}/{players_max}\n\n"
            )

            print(output_info)
        else:
            print("Не удалось получить информацию о ресурсах.")

    def get_server_maps(self):
        result = self.auth_server_user('getmaps')
        if result:
            players_maps = result.get('maps')

            if players_maps:
                print("Карты на сервере:\n\n")
                output_info = ""
                for map_name in players_maps:
                    output_info += f"{map_name}\n"
                print(output_info)
                return output_info
            else:
                print("Список карт пуст.")
        else:
            print("Не удалось получить информацию о картах на сервере.")
            return "Не удалось получить информацию о картах на сервере."

    def change_level_server(self, query_param, map_name):
        url = f"{self.base_url}?query={query_param}&map={map_name}&token={self.token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса к API: {e}")
            return None
