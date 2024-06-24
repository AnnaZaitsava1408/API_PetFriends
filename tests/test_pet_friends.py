import os

from api import PetFriends

from settings import valid_email, valid_password
from dotenv import load_dotenv
load_dotenv()

pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_new_pets_with_valid_data(name='Тими', animal_type='Карликовая домашняя свинья', age='0', pet_photo='images/porosenok-krasivo-4.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    '''pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)'''
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert 'pet_photo' in result


def test_successful_delete_pet( ):
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Тими', 'Карликовая домашняя свинья', '3', 'images/porosenok-krasivo-4.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][2]['id']
    status, _ = pf.Delete_pet_from_database(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_put_pet(name='Том', animal_type='Карликовая свинья', age='7'):
    """Проверяем возможность изменения(обновления) информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.Update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_add_inform_put_without_photo(name='Пип', animal_type= 'кошка', age= '2'):
    """Проверить добавление нформации о новом домашнем животном без фотографии"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_inform_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_successful_add_photo_of_pet(pet_photo = 'images/seal-birman-cat.jpg'):
    """Проверяем, что можно добавить фотографию для питомца по указанному ID """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    """pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)"""

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("Нет питомца для добовления фотографии")














