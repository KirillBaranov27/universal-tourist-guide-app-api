from .user import User, UserCreate, UserLogin, UserInDB, UserUpdate, UserResponse
from .landmark import (
    Landmark, LandmarkCreate, LandmarkUpdate, LandmarkResponse,
    LandmarkListResponse, FiltersResponse, LandmarkWithDistance
)
from .favorite import Favorite, FavoriteCreate, FavoriteResponse
from .review import Review, ReviewCreate, ReviewUpdate, ReviewResponse
from .discussion import (
    Discussion, DiscussionCreate, DiscussionUpdate, DiscussionResponse,
    AnswerCreate, AnswerUpdate, AnswerResponse, VoteCreate
)
from .city import (
    CityBase, CityProfileResponse, CityFilters, CityStatsResponse, 
    PopularCityResponse, CategoryStat
)
from .notification import (
    NotificationBase, NotificationCreate, NotificationUpdate, 
    NotificationResponse, UnreadCountResponse, NotificationListResponse,
    NotificationType
)
from app.schemas.city import CityBase, CityProfileResponse, CityFilters, CityStatsResponse, PopularCityResponse
from app.schemas.notification import (
    NotificationBase, NotificationCreate, NotificationUpdate, NotificationResponse,
    NotificationListResponse, NotificationStatsResponse, MarkAsReadRequest, MarkAsReadResponse
)

__all__ = [
<<<<<<< Updated upstream
    # Существующие
    "UserCreate", "UserLogin", "UserResponse", "Token",
    "UserProfileResponse", "UserProfileUpdate", "UserStatsResponse",
    "LandmarkBase", "LandmarkCreate", "LandmarkResponse", "LandmarkUpdate", "LandmarkListResponse", "FiltersResponse", "LandmarkWithDistance",
    "FavoriteBase", "FavoriteCreate", "FavoriteResponse", "FavoriteListResponse", "FavoriteWithLandmarkResponse",
    "ReviewBase", "ReviewCreate", "ReviewUpdate", "ReviewResponse", "ReviewListResponse", "ReviewWithLandmarkResponse", "LandmarkReviewSummary",
    # Новые - обсуждения
    "DiscussionBase", "DiscussionCreate", "DiscussionUpdate", "DiscussionResponse", "DiscussionWithAnswersResponse",
    "DiscussionAnswerBase", "DiscussionAnswerCreate", "DiscussionAnswerUpdate", "DiscussionAnswerResponse",
    "DiscussionListResponse", "AnswerListResponse", "HelpfulVote",
    # Города
    "CityBase", "CityProfileResponse", "CityFilters", "CityStatsResponse", "PopularCityResponse",
    # Уведомления
    "NotificationBase", "NotificationCreate", "NotificationUpdate", "NotificationResponse",
    "NotificationListResponse", "NotificationStatsResponse", "MarkAsReadRequest", "MarkAsReadResponse"
=======
    # User
    "User", "UserCreate", "UserLogin", "UserInDB", "UserUpdate", "UserResponse",
    # Landmark
    "Landmark", "LandmarkCreate", "LandmarkUpdate", "LandmarkResponse",
    "LandmarkListResponse", "FiltersResponse", "LandmarkWithDistance",
    # Favorite
    "Favorite", "FavoriteCreate", "FavoriteResponse",
    # Review
    "Review", "ReviewCreate", "ReviewUpdate", "ReviewResponse",
    # Discussion
    "Discussion", "DiscussionCreate", "DiscussionUpdate", "DiscussionResponse",
    "AnswerCreate", "AnswerUpdate", "AnswerResponse", "VoteCreate",
    # City
    "CityBase", "CityProfileResponse", "CityFilters", "CityStatsResponse", 
    "PopularCityResponse", "CategoryStat",
    # Notification
    "NotificationBase", "NotificationCreate", "NotificationUpdate", 
    "NotificationResponse", "UnreadCountResponse", "NotificationListResponse",
    "NotificationType",
>>>>>>> Stashed changes
]