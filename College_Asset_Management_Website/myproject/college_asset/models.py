from django.db import models

# Create your models here.

class RegisteredAsset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    asset_name = models.CharField(max_length=255)

    def __str__(self):
        return self.asset_name

class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    classroom_no = models.IntegerField()
    classroom_name = models.CharField(max_length=255)
    division = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.classroom_name} ({self.division})"

class ClassroomAsset(models.Model):
    classroom_asset_id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    asset = models.ForeignKey(RegisteredAsset, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    inactive_quantity = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.asset.asset_name} in {self.classroom.classroom_name}"