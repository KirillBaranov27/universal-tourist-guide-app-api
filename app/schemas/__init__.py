from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.landmark import LandmarkBase, LandmarkCreate, LandmarkResponse, LandmarkUpdate, LandmarkListResponse, FiltersResponse, LandmarkWithDistance
from app.schemas.favorite import FavoriteBase, FavoriteCreate, FavoriteResponse, FavoriteListResponse, FavoriteWithLandmarkResponse
from app.schemas.review import ReviewBase, ReviewCreate, ReviewUpdate, ReviewResponse, ReviewListResponse, ReviewWithLandmarkResponse, LandmarkReviewSummary
from app.schemas.profile import UserProfileResponse, UserProfileUpdate, UserStatsResponse
from app.schemas.discussion import (
    DiscussionBase, DiscussionCreate, DiscussionUpdate, DiscussionResponse, DiscussionWithAnswersResponse,
    DiscussionAnswerBase, DiscussionAnswerCreate, DiscussionAnswerUpdate, DiscussionAnswerResponse,
    DiscussionListResponse, AnswerListResponse, HelpfulVote
)

__all__ = [
    # Существующие
    "UserCreate", "UserLogin", "UserResponse", "Token",
    "UserProfileResponse", "UserProfileUpdate", "UserStatsResponse",
    "LandmarkBase", "LandmarkCreate", "LandmarkResponse", "LandmarkUpdate", "LandmarkListResponse", "FiltersResponse", "LandmarkWithDistance",
    "FavoriteBase", "FavoriteCreate", "FavoriteResponse", "FavoriteListResponse", "FavoriteWithLandmarkResponse",
    "ReviewBase", "ReviewCreate", "ReviewUpdate", "ReviewResponse", "ReviewListResponse", "ReviewWithLandmarkResponse", "LandmarkReviewSummary",
    # Новые - обсуждения
    "DiscussionBase", "DiscussionCreate", "DiscussionUpdate", "DiscussionResponse", "DiscussionWithAnswersResponse",
    "DiscussionAnswerBase", "DiscussionAnswerCreate", "DiscussionAnswerUpdate", "DiscussionAnswerResponse",
    "DiscussionListResponse", "AnswerListResponse", "HelpfulVote"
]