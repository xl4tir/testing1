from django.db import models
import datetime

class AllTests(models.Model):
    testname = models.CharField('Назва тесту', max_length = 200)
    author = models.CharField('Автор тесту', max_length = 200)
    date = models.DateTimeField("Дата публікації")
    testcode = models.IntegerField('Код тесту', null=True)
    number_passed = models.IntegerField('Кількість пройдено', null=True, default = 0)

    def __str__(self):
         return self.testname

    class Meta:
         verbose_name = 'Тест'
         verbose_name_plural = 'Всі тести'

class Tests(models.Model):
    test = models.ForeignKey(AllTests, on_delete = models.CASCADE)
    ques_num= models.IntegerField('Номер питання', null=True)
    testcode = models.IntegerField('Код тесту', null=True)
    ques = models.CharField("Питання", max_length = 200, default = 0)



    class Meta:
         verbose_name = 'Питання до тесту'
         verbose_name_plural = 'Питання до тестів'

class Answers(models.Model):
    test = models.ForeignKey(Tests, on_delete = models.CASCADE)
    ques_num = models.IntegerField("Номер питання")
    ans = models.CharField("Відповідь", max_length = 200, default = 0)
    testcode = models.IntegerField('Код тесту', null=True)
    ans_value = models.CharField("Чи правильна Відповідь", max_length = 200, default = 0)
    ans_num = models.IntegerField("Номер відповіді", default = 0)

    class Meta:
         verbose_name = 'Відповідь до тесту'
         verbose_name_plural = 'Відповіді до тестів'


class Tests_complete(models.Model):
    test = models.ForeignKey(AllTests, on_delete = models.CASCADE)
    ques_num= models.IntegerField('Номер питання', null=True)
    testcode = models.IntegerField('Код тесту', null=True)
    token = models.CharField("Токен тестування", max_length = 200, default = 0)
    author = models.CharField('Той хто проходить', max_length = 200)
    date = models.DateTimeField("Дата проходження тесту", default=datetime.datetime.now())


    class Meta:
         verbose_name = 'Виконане питання'
         verbose_name_plural = 'Виконані питання'

class Answers_complete(models.Model):
    test = models.ForeignKey(AllTests, on_delete = models.CASCADE)
    ques_num = models.IntegerField("Номер питання")
    ans = models.CharField("Відповідь того хто прозодить", max_length = 200, default = 0)
    testcode = models.IntegerField('Код тесту', null=True)
    token = models.CharField("Токен тестування", max_length = 200, default = 0)
    correct = models.CharField("Правильно?", max_length = 200, default = 0)

    class Meta:
         verbose_name = 'Введена відповідь'
         verbose_name_plural = 'Введені відповіді'


class Test_complete(models.Model):
    testname = models.CharField('Назва тесту', max_length = 200, default=" ")
    test = models.ForeignKey(AllTests, on_delete = models.CASCADE)
    author = models.CharField('Автор тесту', max_length = 200)
    testcode = models.IntegerField('Код тесту', null=True)
    date = models.DateTimeField("Дата проходження тесту" , default =datetime.datetime.now())
    token = models.CharField("Токен тестування", max_length = 200, default = 0)

    class Meta:
         verbose_name = 'Пройдений тест'
         verbose_name_plural = 'Пройдені тести'
