from scrapy_djangoitem import DjangoItem
from toastmasters.models import Member
class MemberItem(DjangoItem):
    django_model = Member