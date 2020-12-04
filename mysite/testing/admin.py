from django.contrib import admin
from .models import AllTests, Tests, Answers,Test_complete

admin.site.register(AllTests)
admin.site.register(Tests)
admin.site.register(Answers)
admin.site.register(Test_complete)
