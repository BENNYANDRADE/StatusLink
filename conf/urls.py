"""URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include(('apps.users.urls', 'users'), namespace='users')),   
	path('', include(('apps.administrators.urls', 'administrators'), namespace='administrators')),   
	# path('', include(('apps.regions.urls', 'regions'), namespace='regions')),   
	# path('', include(('apps.utils.urls', 'utils'), namespace='utils')),   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
	import debug_toolbar

	urlpatterns += [

		path('__debug__/', include(debug_toolbar.urls)),
	]

#Error Handling
handler500 = 'apps.utils.handler500'
handler404 = 'apps.utils.handler404'