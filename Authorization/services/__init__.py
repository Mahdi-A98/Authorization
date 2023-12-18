# In the name of GOD

from .account_service import AccountService
from .notification_service import NotificationService
from .podcast_service import PodcastService

SERVICE_CLASSES = { 
    "account" : AccountService,
    "notification" : NotificationService,
    "podcast" : PodcastService
    }