import requests

BASE_URL = "http://127.0.0.1:8000"

def test_argon2():
    print("🧪 Тестирование с Argon2...")
    
    # Тест с длинным паролем
    register_data = {
        "email": "argon2@test.com",
        "password": "оченьдлинныйпаролькоторыйточнобольше72байтидажебольше100символовчтобыпроверитьработуаргона",
        "full_name": "Argon2 User"
    }
    
    print("📝 Регистрация с длинным паролем...")
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print(f"Статус: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ РЕГИСТРАЦИЯ С ДЛИННЫМ ПАРОЛЕМ РАБОТАЕТ!")
        user_data = response.json()
        print(f"Создан пользователь: {user_data['email']}")
    else:
        print(f"❌ Ошибка: {response.text}")
        return
    
    # Тест входа
    login_data = {
        "email": "argon2@test.com",
        "password": "оченьдлинныйпаролькоторыйточнобольше72байтидажебольше100символовчтобыпроверитьработуаргона"
    }
    
    print("\n🔐 Вход с длинным паролем...")
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Статус: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print("✅ ВХОД С ДЛИННЫМ ПАРОЛЕМ РАБОТАЕТ!")
        print(f"Токен: {token_data['access_token'][:30]}...")
    else:
        print(f"❌ Ошибка входа: {response.text}")

if __name__ == "__main__":
    test_argon2()