from django.db import models
import pymongo


# my_client = pymongo.MongoClient('mongodb+srv://ryankeogh:KildareCBSTUD2020@coursifycluster.nlwdba1.mongodb.net/?retryWrites=true&w=majority')
# db_name = my_client['CoursifyData']
# collection_name = db_name['CourseData']
#
# res = collection_name.find({})
#

class Course(models.Model):
    code = models.CharField(max_length=100, db_column='code')
    title = models.CharField(max_length=100, db_column='Title1')
    college = models.CharField(max_length=100, db_column='college')
    duration = models.CharField(max_length=100, db_column='duration')
    description = models.CharField(max_length=100, db_column='description')
    career = models.CharField(max_length=100, db_column='career')
    trait = models.CharField(max_length=100, db_column='trait')
    trait2 = models.CharField(max_length=100, db_column='trait2')
    url = models.CharField(max_length=100, db_column='college_URL')
    title_url = models.CharField(max_length=100, db_column='Title_URL')


    class Meta:
        db_table = 'CourseData'


