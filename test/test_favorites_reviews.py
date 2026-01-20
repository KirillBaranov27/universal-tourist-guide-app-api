import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_favorites_and_reviews():
    print("🧪 Тестирование системы избранного и отзывов...")
    
    # Сначала получаем токен
    auth_data = {
        "email": "test@example.com", 
        "password": "testpassword123"
    }
    
    try:
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

    # Получаем ID первой достопримечательности для тестов
    response = requests.get(f"{BASE_URL}/api/landmarks?limit=1")
    if response.status_code != 200:
        print("❌ Не удалось получить достопримечательности")
        return
        
    landmark_id = response.json()["items"][0]["id"]
    landmark_name = response.json()["items"][0]["name"]
    print(f"✅ Используем достопримечательность: {landmark_name} (ID: {landmark_id})")

    # Тест 1: Добавление в избранное
    try:
        print("\n1. ❤️ Добавление в избранное...")
        response = requests.post(
            f"{BASE_URL}/api/favorites",
            json={"landmark_id": landmark_id},
            headers=headers
        )
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Успешно добавлено в избранное")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 2: Проверка статуса избранного
    try:
        print("\n2. 🔍 Проверка статуса избранного...")
        response = requests.get(
            f"{BASE_URL}/api/favorites/check/{landmark_id}",
            headers=headers
        )
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ В избранном: {data['is_favorite']}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 3: Получение списка избранного
    try:
        print("\n3. 📋 Получение списка избранного...")
        response = requests.get(f"{BASE_URL}/api/favorites", headers=headers)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ В избранном: {data['total']} достопримечательностей")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 4: Добавление отзыва
    try:
        print("\n4. ⭐ Добавление отзыва...")
        review_data = {
            "landmark_id": landmark_id,
            "rating": 5,
            "comment": "Очень красивое место! Рекомендую к посещению."
        }
        response = requests.post(
            f"{BASE_URL}/api/reviews",
            json=review_data,
            headers=headers
        )
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Отзыв успешно добавлен")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 5: Получение отзывов для достопримечательности
    try:
        print("\n5. 💬 Получение отзывов для достопримечательности...")
        response = requests.get(f"{BASE_URL}/api/reviews/landmark/{landmark_id}")
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Найдено {data['total']} отзывов")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 6: Получение сводки по рейтингам
    try:
        print("\n6. 📊 Получение сводки по рейтингам...")
        response = requests.get(f"{BASE_URL}/api/reviews/landmark/{landmark_id}/summary")
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Средний рейтинг: {data['average_rating']}, всего отзывов: {data['total_reviews']}")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 7: Получение отзывов пользователя
    try:
        print("\n7. 👤 Получение отзывов пользователя...")
        response = requests.get(f"{BASE_URL}/api/reviews/user", headers=headers)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Пользователь оставил {data['total']} отзывов")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # Тест 8: Удаление из избранного
    try:
        print("\n8. 🗑️ Удаление из избранного...")
        response = requests.delete(
            f"{BASE_URL}/api/favorites/{landmark_id}",
            headers=headers
        )
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Успешно удалено из избранного")
        else:
            print(f"   ❌ Ошибка: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")


if __name__ == "__main__":
    test_favorites_and_reviews()