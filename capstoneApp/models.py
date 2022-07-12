from django.db import models


class userinfo(models.Model):
    username = models.CharField(max_length=30, null=False)
    userid = models.CharField(max_length=30, null=False, primary_key=True)
    password = models.CharField(max_length=30, null=False)


    class Meta:
        #정렬
        #ordering = ('userid',)
        db_table = 'userinfo'

    def __str__(self):
        return self.userid


#재료_list , 직접 수기로 만들어줘야함
class item_list(models.Model):
    item_id = models.IntegerField(null=False, primary_key=True)
    item_name = models.CharField(max_length=100, null=False)


    class Meta:
        db_table = 'item_list'


#냉장고DB
class refrigerator_item(models.Model):
    userid = models.ForeignKey('userinfo', on_delete=models.CASCADE, db_column='userid')
    item_id = models.ForeignKey('item_list', on_delete=models.CASCADE, db_column='item_id')


    class Meta:
        db_table = 'refrigerator_item'



#레시피_LIst , 직접수기로 만들어줘야함
class recipe_list(models.Model):
    recipe_id = models.IntegerField(null=False, primary_key=True)
    recipe_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'recipe_list'


#레시피재료_list , 직접 수기로 만들어줘야함
class recipe_item_list(models.Model):
    recipe_id = models.ForeignKey('recipe_list', on_delete=models.CASCADE, db_column='recipe_id')
    item_id = models.ForeignKey('item_list', on_delete=models.CASCADE, db_column='item_id')
    item_importance = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'recipe_item_list'


#레시피과정&순서 , 직접 수기로 만들어줘야함
class recipe_process(models.Model):
    recipe_id = models.ForeignKey('recipe_list', on_delete=models.CASCADE, db_column='recipe_id')
    order = models.IntegerField(null=False)
    process = models.CharField(max_length=2000, null=False)

    class Meta:
        db_table = 'recipe_process'