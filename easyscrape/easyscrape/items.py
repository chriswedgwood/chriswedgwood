from scrapy_djangoitem import DjangoItem
from blog.models import BlogPage
from toastmasters.models import Member
class MemberItem(DjangoItem):
    django_model = Member