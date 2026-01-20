from app.crud.landmark_crud import (
    get_landmark,
    get_landmarks,
    create_landmark,
    update_landmark,
    delete_landmark,
    get_cities,
    get_categories,
    get_landmarks_near_location
)

from app.crud.favorite_crud import (
    get_favorite,
    get_user_favorites,
    create_favorite,
    delete_favorite,
    is_landmark_favorite
)

from app.crud.review_crud import (
    get_review,
    get_reviews_by_landmark,
    get_reviews_by_user,
    create_review,
    update_review,
    delete_review,
    get_landmark_rating_summary
)

from app.crud.user_crud import (
    get_user_profile,
    update_user_profile,
    get_user_stats
)

from app.crud.discussion_crud import (
    get_discussion,
    get_discussions,
    create_discussion,
    update_discussion,
    delete_discussion,
    get_answer,
    get_answers_by_discussion,
    create_answer,
    update_answer,
    delete_answer,
    vote_helpful,
    get_discussion_stats
)

__all__ = [
    "get_landmark",
    "get_landmarks", 
    "create_landmark",
    "update_landmark",
    "delete_landmark",
    "get_cities",
    "get_categories",
    "get_landmarks_near_location",
    "get_favorite",
    "get_user_favorites", 
    "create_favorite",
    "delete_favorite",
    "is_landmark_favorite",
    "get_review",
    "get_reviews_by_landmark",
    "get_reviews_by_user",
    "create_review",
    "update_review",
    "delete_review",
    "get_landmark_rating_summary",
    "get_user_profile",
    "update_user_profile",
    "get_user_stats",
    # Новые - обсуждения
    "get_discussion",
    "get_discussions",
    "create_discussion",
    "update_discussion",
    "delete_discussion",
    "get_answer",
    "get_answers_by_discussion",
    "create_answer",
    "update_answer",
    "delete_answer",
    "vote_helpful",
    "get_discussion_stats",
    "get_city_profile",
    "get_city_stats", 
    "get_cities_with_stats",
    "get_filtered_landmarks_by_city",
    "get_city_categories"
]