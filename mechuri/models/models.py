from django.db import models


class CommentReport(models.Model):
    reporter = models.ForeignKey('User', models.DO_NOTHING)
    comment = models.ForeignKey('RecipeComment', models.DO_NOTHING)
    type = models.IntegerField()
    reported_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment_report'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Friend(models.Model):
    accepted_at = models.DateTimeField()
    requestor = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    receiver = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friend'


class FriendRequest(models.Model):
    requested_at = models.DateTimeField()
    requestor = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    receiver = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friend_request'


class Group(models.Model):
    group_uuid = models.CharField(max_length=36, db_collation='utf8_bin')
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField()
    owner = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group'


class GroupKnnLoc(models.Model):
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    menu = models.ForeignKey('Menu', models.DO_NOTHING, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_knn_loc'


class GroupKnnWeather(models.Model):
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    menu = models.ForeignKey('Menu', models.DO_NOTHING, blank=True, null=True)
    temp = models.FloatField()
    precip = models.FloatField()
    humid = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_knn_weather'


class GroupMenuInteraction(models.Model):
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    menu = models.ForeignKey('Menu', models.DO_NOTHING, blank=True, null=True)
    rating = models.DecimalField(max_digits=10, decimal_places=9, blank=True, null=True)
    last_interacted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_menu_interaction'


class GroupRequest(models.Model):
    group_uuid = models.CharField(max_length=36, db_collation='utf8_bin')
    requested_at = models.DateTimeField()
    requestor = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    receiver = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_request'


class GroupUser(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_user'


class Menu(models.Model):
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=7)
    major = models.CharField(max_length=30, blank=True, null=True)
    middle = models.CharField(max_length=30, blank=True, null=True)
    meal_type = models.CharField(max_length=30, blank=True, null=True)
    nutrient = models.ForeignKey('Nutrient', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu'


class Nutrient(models.Model):
    energy = models.FloatField()
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    sugar = models.FloatField()
    sodium = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nutrient'


class PersonalKnnLoc(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    menu = models.ForeignKey(Menu, models.DO_NOTHING, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_knn_loc'


class PersonalKnnWeather(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    menu = models.ForeignKey(Menu, models.DO_NOTHING, blank=True, null=True)
    temp = models.FloatField()
    precip = models.FloatField()
    humid = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_knn_weather'


class PersonalMenuInteraction(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    menu = models.ForeignKey(Menu, models.DO_NOTHING, blank=True, null=True)
    rating = models.DecimalField(max_digits=10, decimal_places=9, blank=True, null=True)
    last_interacted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_menu_interaction'


class Recipe(models.Model):
    recipe_uuid = models.CharField(unique=True, max_length=36, blank=True, null=True)
    writer = models.ForeignKey('User', models.DO_NOTHING)
    menu = models.ForeignKey(Menu, models.DO_NOTHING)
    title = models.CharField(max_length=45)
    intro_content = models.CharField(max_length=45, blank=True, null=True)
    photh_url = models.CharField(max_length=8192, blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    views = models.SmallIntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe'


class RecipeComment(models.Model):
    recipe_comment_uuid = models.CharField(unique=True, max_length=36, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)
    content = models.TextField()
    commented_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe_comment'


class RecipeLike(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_like'


class RecipeReport(models.Model):
    reporter = models.ForeignKey('User', models.DO_NOTHING)
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)
    type = models.IntegerField()
    reported_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe_report'


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)
    step_no = models.IntegerField()
    content = models.TextField()
    photo_url = models.CharField(max_length=8192, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipe_step'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, models.DO_NOTHING)
    tag = models.ForeignKey('Tag', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_tag'


class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tag'


class User(models.Model):
    user_uuid = models.CharField(unique=True, max_length=36)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=150)
    nickname = models.CharField(unique=True, max_length=15)
    joined_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
