from django.contrib import admin
from django.utils.html import format_html
from .models import *
# Register your models here.




# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'get_episode_link', 'podcast', 'published_at', 'created_at')
#     # search_fields = ('id', 'title', 'slug')
#     # readonly_fields = ('guid', )
#     list_filter = ['podcast']

#     # def get_episode_link(self, obj):
       
#     #     return format_html(f"<a href='/{self.pk}' target='_blank'>Link</a>")



admin.site.register(Item)
admin.site.register(User_details)
admin.site.register(Bidder)

