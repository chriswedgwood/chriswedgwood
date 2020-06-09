from toastmasters.models import Member,Role,MemberRole,Meeting,Pathway,PathwayLevel,PathwaySpeech,MemberSpeech

class MemberPipeline(object):
      def process_item(self, item, spider):
          print('bnbnbnbn')
          member, created = Member.objects.update_or_create(es_id=item['es_id'],defaults=item)
          print(member)
          print(created)
          return member

class RolePipeline(object):
      def process_item(self, item, spider):
          print('bnbnbnbn')
          role, _ = Role.objects.get_or_create(title=item['role'])
          meeting, _ = Meeting.objects.get_or_create(date=item['role_date'])
          member = Member.objects.get(es_id=item['es_id'])
          role,_ = MemberRole.objects.get_or_create(member=member,role=role,meeting=meeting)
          return role
class SpeechPipeline(object):
      def process_item(self, item, spider):
          pathway = item['pathway']
          level = item['level']
          assignment = item['assignment']
          speech_title = item['speech_title']
          completed_date = item['completed_date']
          
          
          member = Member.objects.get(es_id=item['es_id'])
          
          
          pathway, _ = Pathway.objects.get_or_create(title=pathway)
          pathway_level, _ = PathwayLevel.objects.get_or_create(title=level,pathway=pathway)
          pathway_speech, _ = PathwaySpeech.objects.get_or_create(title=speech_title,level=pathway_level)
          meeting, _ = Meeting.objects.get_or_create(date=completed_date)
          member_speech, _ = MemberSpeech.objects.get_or_create(title=speech_title,meeting=meeting,pathway_speech=pathway_speech,member=member)
          
          
          return member_speech


class MeetingPipeline(object):
      def process_item(self, item, spider):
          print('bnbnbnbn')
        #   role, _ = Role.objects.get_or_create(title=item['role'])
        #   meeting, _ = Meeting.objects.get_or_create(date=item['role_date'])
        #   member = Member.objects.get(es_id=item['es_id'])
        #   role,_ = MemberRole.objects.get_or_create(member=member,role=role,meeting=meeting)
        #   return role
