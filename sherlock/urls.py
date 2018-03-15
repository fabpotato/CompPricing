from django.conf.urls import patterns, url

from sherlock.views import Homepage, Calculate

urlpatterns = patterns(
	'',

	url(r"^index/", Homepage.as_view(), name='homepage'),
	url(r"^do_stuff/", Calculate.as_view(), name='calculate')
)