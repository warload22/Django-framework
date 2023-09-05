from datetime import datetime

import requests
from authapp.models import PlayerProfile
from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    url_method = 'https://api.vk.com/method/'
    access_token = response.get('access_token')
    fields = ','.join(['sex', 'about', 'bdate'])

    api_url = f'{url_method}users.get?fields={fields}&access_token={access_token}&v=5.131'

    response = requests.get(api_url)

    if response.status_code != 200:
        return

    data = response.json()['response'][0]

    if data['sex']:
        if data['sex'] == 2:
            user.playerprofile.gender = PlayerProfile.male
        elif data['sex'] == 1:
            user.playerprofile.gender = PlayerProfile.female

    if data['about']:
        user.playerprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = datetime.now().date().year - bdate.year

        if age > 100:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.age = age

    user.save()

