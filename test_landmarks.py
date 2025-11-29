import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_landmarks():
    print("🧪 Тестирование системы достопримечательностей Санкт-Петербурга...")
    
    # Сначала получаем токен для аутентифицированных запросов
    auth_data = {
        "email": "test@example.com", 
        "password": "testpassword123"
    }
    
    try:
        # Логинимся
        response = requests.post(f"{BASE_URL}/api/auth/login", json=auth_data)
        if response.status_code != 200:
            print("❌ Не удалось получить токен для тестирования")
            return
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("✅ Получен токен для тестирования")
        
    except Exception as e:
        print(f"❌ Ошибка при получении токена: {e}")
        return

    # Тест 1: Получение всех достопримечательностей СПб
    try:
        print("\n1. 📋 Получение всех достопримечательностей Санкт-Петербурга...")
        response = requests.get(f"{BASE_URL}/api/landmarks")
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Успешно! Всего достопримечательностей в СПб: {data['total']}")
            
            # Проверяем что все достопримечательности из СПб
            all_spb = all(item['city'] == 'Санкт-Петербург' for item in data['items'])
            if all_spb:
                print("   ✅ Все достопримечательности из Санкт-Петербурга")
            else:
                print("   ❌ Найдены достопримечательности не из СПб")
                
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 2: Фильтрация по категориям СПб
    try:
        print("\n2. 🏛️ Фильтрация музеев Санкт-Петербурга...")
        response = requests.get(f"{BASE_URL}/api/landmarks?category=Музей")
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            museum_count = data['total']
            print(f"   ✅ Найдено {museum_count} музеев в Санкт-Петербурге")
            
            # Выводим названия музеев
            if museum_count > 0:
                museum_names = [item['name'] for item in data['items']]
                print(f"   🎭 Музеи: {', '.join(museum_names)}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 3: Поиск конкретной достопримечательности
    try:
        print("\n3. 🔍 Поиск 'Эрмитаж' в Санкт-Петербурге...")
        response = requests.get(f"{BASE_URL}/api/landmarks?search=Эрмитаж")
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Найдено {data['total']} результатов по запросу 'Эрмитаж'")
            if data['total'] > 0:
                print(f"   📍 Найден: {data['items'][0]['name']}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 4: Получение фильтров для СПб
    try:
        print("\n4. 🎯 Получение доступных фильтров Санкт-Петербурга...")
        response = requests.get(f"{BASE_URL}/api/filters/all")
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Категории в СПб: {', '.join(data['categories'])}")
            
            # Проверяем что Санкт-Петербург в списке городов
            if 'Санкт-Петербург' in data['cities']:
                print("   ✅ Санкт-Петербург присутствует в списке городов")
            else:
                print("   ❌ Санкт-Петербург не найден в списке городов")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 5: Геолокационный поиск в центре СПб
    try:
        print("\n5. 📍 Поиск достопримечательностей near Дворцовая площадь...")
        response = requests.get(
            f"{BASE_URL}/api/landmarks/nearby",
            params={
                "latitude": 59.9398,  # Дворцовая площадь
                "longitude": 30.3146,
                "radius": 2,  # 2 км радиус
                "limit": 5
            }
        )
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Найдено {len(data)} достопримечательностей поблизости")
            for landmark in data[:3]:  # Показываем первые 3
                distance = landmark.get('distance', 'N/A')
                print(f"      📍 {landmark['name']} (~{distance:.1f} км)")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")


if __name__ == "__main__":
    test_landmarks()