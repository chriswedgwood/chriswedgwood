from django.db import models

# Create your models here.

class Club(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title



class Member(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    club = models.ManyToManyField(to=Club)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Role(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Meeting(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.title


class Pathway(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class PathwayLevel(models.Model):
    title = models.CharField(max_length=30)
    pathway = models.ForeignKey(to=Pathway,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PathwaySpeech(models.Model):
    title = models.CharField(max_length=30)
    level = models.ForeignKey(to=PathwayLevel,on_delete=models.CASCADE)

    def __str__(self):
        return self.title



class MemberSpeech(models.Model):
    title = models.CharField(max_length=30)
    meeting = models.ForeignKey(to=Meeting,on_delete=models.CASCADE)
    pathway_speech = models.ForeignKey(to=PathwaySpeech,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title



class MemberRole(models.Model):
    member = models.ForeignKey(to=Member,on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role,on_delete=models.CASCADE)
    meeting = models.ForeignKey(to=Meeting,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member)








