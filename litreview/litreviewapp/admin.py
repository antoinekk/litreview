from django.contrib import admin
from litreviewapp.models import User, Ticket, Review, UserFollows

# Register your models here.

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollows)
