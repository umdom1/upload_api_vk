import requests


class loadingVK:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version

    def upload_photos(self):
        url = self.base_url + 'photos.get'
        params = {'user_id': self.id, 'access_token': self.token, 'v': self.version, 'owner_id': self.id,
                  'album_id': 'wall', 'extended': 1}
        response = requests.get(url, params=params)
        print('Получен список фото\n')
        return response.json()

    def safe_photo(self):
        file_photos = []
        url_list = []

        res = self.upload_photos()
        for el in res['response']['items']:
            url_list.append(el['sizes'])
        for li in url_list:
            url = li[-1]['url']

            response = requests.get(url)

            name = str(li[-1]['height'])
            type = str(li[-1]['type'])

            with open((f'{name}.jpg'), 'wb') as f:
                f.write(response.content)

            file_photos.append({"file_name": (f'{name}.jpg'), "size": type})
        with open('1.json', 'w') as file:
            file.write(str(file_photos))
        print('Все фото скачаны и сохранены на ПК\n')
        return (file_photos)


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_heders(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    # создание папки
    def create_folder(self, disk_file_path_home):
        headers = self.get_heders()
        params = {'path': disk_file_path_home}
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=headers, params=params)
        if response.status_code == 201:
            print("Папка на Я.Диске созданна успешно\n")

    def get_upload_files(self, url, filename):
        self.create_folder(disk_file_path_home)
        for el in filename:
            filename_upload = el['file_name']
            disk_file_path = f'/{disk_file_path_home}/{filename_upload}'
            headers = self.get_heders()
            params = {"path": disk_file_path, "overwrite": "true"}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            href = (data['href'])

            response = requests.put(href, data=open(filename_upload, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Файлы загружены успешно")


if __name__ == '__main__':
    access_token = 'token'
    user_id = 'user_id'
    vk = loadingVK(access_token, user_id)
    filename = vk.safe_photo()

    disk_file_path_home = "photo"  # Наименование создаваемой папки
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    token = 'token'
    uploader = YandexDisk(token)
    result = uploader.get_upload_files(url, filename)



