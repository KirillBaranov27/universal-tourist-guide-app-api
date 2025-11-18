import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_auth():
    print("🧪 Тестирование системы аутентификации...")
    
    # Используем очень простой пароль для диагностики
    register_data = {
        "email": "test@example.com",
        "password": "12345678",  # Простейший пароль
        "full_name": "Test User"
    }
    
    try:
        print("📝 Тестируем регистрацию...")
        print(f"Отправляемые данные: email={register_data['email']}, password_length={len(register_data['password'])}")
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Статус код: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Регистрация работает!")
            user_data = response.json()
            print(f"   Создан пользователь: {user_data['email']}")
        elif response.status_code == 400:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            print(f"ℹ️  Ошибка клиента: {error_detail}")
            if "уже зарегистрирован" in error_detail:
                print("   Пользователь уже существует, продолжаем тест...")
        else:
            print(f"❌ Ошибка регистрации: {response.status_code}")
            print(f"   Ответ сервера: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при регистрации: {e}")
    
    # Тест входа
    login_data = {
        "email": "test@example.com",
        "password": "12345678"  # Тот же простой пароль
    }
    
    try:
        print("\n🔐 Тестируем вход...")
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"Статус код: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Вход работает!")
            print(f"   Получен токен: {token_data['access_token'][:20]}...")
        else:
            print(f"❌ Ошибка входа: {response.status_code}")
            print(f"   Ответ сервера: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при входе: {e}")

if __name__ == "__main__":
    test_auth()