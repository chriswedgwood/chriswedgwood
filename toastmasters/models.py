from django.db import models

# Create your models here.

class Club(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title



class Member(models.Model):
    full_name = models.CharField(max_length=30)
    club = models.ManyToManyField(to=Club)
    join_date = models.DateField()
    es_id = models.IntegerField()

    def __str__(self):
        return f'{self.full_name} '


class Role(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Meeting(models.Model):
    
    date = models.DateField(unique=True)
   

    def __str__(self):
        return str(self.date)


class Pathway(models.Model):
    title = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class PathwayLevel(models.Model):
    title = models.CharField(max_length=1000)
    pathway = models.ForeignKey(to=Pathway,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + str(self.pathway)


class PathwaySpeech(models.Model):
    title = models.CharField(max_length=1000)
    level = models.ForeignKey(to=PathwayLevel,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.level)



class MemberSpeech(models.Model):
    title = models.CharField(max_length=500)
    meeting = models.ForeignKey(to=Meeting,on_delete=models.CASCADE)
    pathway_speech = models.ForeignKey(to=PathwaySpeech,on_delete=models.CASCADE)
    member = models.ForeignKey(to=Member,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title



class MemberRole(models.Model):
    member = models.ForeignKey(to=Member,on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role,on_delete=models.CASCADE)
    meeting = models.ForeignKey(to=Meeting,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member)








