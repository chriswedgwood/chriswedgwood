from toastmasters.models import Member

class MemberPipeline(object):
      def process_item(self, item, spider):
          print('bnbnbnbn')
          #member, created = Member.objects.update_or_create(code=item['code'],defaults=item)
          #print(meeting)
          #print(created)
          #return meeting