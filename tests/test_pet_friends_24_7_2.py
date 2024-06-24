import os

from api import PetFriends

from settings import valid_email, valid_password, invalid_email, invalid_password
from dotenv import load_dotenv
load_dotenv()

pf = PetFriends()

# 1 Тестирование авторизации. Получение ключа API
# 1.1 Валидный ввод email и невалидный ввод password

def test_get_api_key_invalid_password(email=valid_email, password= invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

# 1.2 Невалидный ввод email и валидный ввод password
def test_get_api_key_invalid_email(email=invalid_email, password= valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

# 1.3 Невалидный ввод email и невалидный ввод password
def test_get_api_key_invalid_user(email=invalid_email, password= invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


# 2 Добовление питомца с неккоректными данными:
# 2.1 Добовление питомца с неккоректным именем
def test_successful_add_inform_put_invalid_name(name='#%##%%4463', animal_type= 'кошка', age= '2',  pet_photo='images/seal-birman-cat.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)"""
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# 2.2 Добовление питомца с неккоректным типом животного
def test_successful_add_inform_put_invalid_type(name='Музя', animal_type= '";%№%1146', age= '1', pet_photo='images/seal-birman-cat.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)"""
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == animal_type

# 2.3 Добовление питомца без данных о имени, типе животного и возрасте
def test_successful_add_no_inform_put_with_photo(name='', animal_type= '', age= '', pet_photo='images/seal-birman-cat.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)"""
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == animal_type


# 2.4 Добовление питомца с неккоректными симвалами в строке возраст животного
def test_successful_add_inform_put_invalid_age(name='Путик', animal_type= 'шиншилла', age= '№%:;%;Полаен', pet_photo='images/orig.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)"""
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age

# 2.5 Добовление питомца с неккоректными возрастом домашнего животного
def test_successful_add_invalid_age(name='Путик', animal_type= 'шиншилла', age= '4500000000000000000000', pet_photo='images/orig.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    """pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)"""
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age


# 2.6 Добовление питомца без данных
def test_successful_add_no_inform_put(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_inform_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

# 2.7 Добовление питомца только по одному имени
def test_successful_add_inform_put_only_name(name='Тумка', animal_type= '', age= ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_inform_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

# 2.8 Добовление питомца только по одному возрасту
def test_successful_add_inform_put_only_age(name='', animal_type= '', age= '59'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_inform_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200


# 2.9 Добовление питомца только по несуществующему виду животного
def test_successful_add_inform_put_only_type(name='', animal_type= 'слонопес', age= ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_inform_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200

# 3.0 Обновление информации о питомце неволидными данными
def test_successful_put_pet(name='@$#%%', animal_type='4y6r', age='2222222222'):
    """Проверяем возможность изменения(обновления) информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.Update_information_about_pet(auth_key, my_pets['pets'][3]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# 3.1 Добовление фотографии питомца, у которого уже есть фотография
def test_successful_add_photo_of_pet(pet_photo = 'images/gagaru-club-85.jpg'):
    """Проверяем, что можно добавить фотографию для питомца по указанному ID """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    """pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)"""

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][4]['id'], pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("Нет питомца для добовления фотографии")





