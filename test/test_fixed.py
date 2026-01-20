import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def quick_test():
    print("🧪 Быстрый тест после исправлений...")
    
    # Даем серверу время запуститься
    time.sleep(2)
    
    # Тест 1: Проверка здоровья
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
    except:
        print("❌ Сервер не отвечает")
        return
    
    # Тест 2: Логин
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Логин работает")
        else:
            print(f"❌ Логин не работает: {response.text}")
            return
    except Exception as e:
        print(f"❌ Ошибка логина: {e}")
        return
    
    # Тест 3: Получение достопримечательностей
    try:
        response = requests.get(f"{BASE_URL}/api/landmarks")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Достопримечательности: {data['total']} шт.")
        else:
            print(f"❌ Ошибка достопримечательностей: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    quick_test()