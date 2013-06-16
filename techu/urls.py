from django.conf.urls import patterns, include, url

urlpatterns = patterns('techu.views',
  url(r'^configuration[/]*$', 'configuration', name = 'configuration_insert'),
  url(r'^configuration/list[/]*$', 'configuration_list', name = 'configuration_list'),
  url(r'^configuration/(?P<configuration_id>\d+)[/]*$', 'configuration', name = 'configuration'),
  url(r'^searchd[/]*(?P<searchd_id>\d+)[/]*$', 'searchd', name = 'searchd'),
  url(r'^searchd[/]*$', 'searchd', name = 'searchd'),
  url(r'^option/list[/]*$', 'option_list', name = 'option_list'),
  url(r'^option/(?P<section>[a-z]+)/(?P<section_instance_id>\d+)[/]*$', 'option', name = 'option'),
  url(r'^index[/]*$', 'index', name = 'index_insert'),
  url(r'^index/(?P<index_id>\d+)[/]*$', 'index', name = 'index'),
  url(r'^index/list[/]*$', 'index_list', name = 'index_list'),
  url(r'^indexer/(?P<action>[a-z]+)/(?P<index_id>\d+)[/]*$', 'indexer', name = 'indexer'),
  url(r'^indexer/(?P<action>[a-z]+)/(?P<index_id>\d+)[/]*(?P<doc_id>\d+)[/]*$', 'indexer', name = 'indexer'),
  url(r'^search/(?P<index_id>\d+)[/]*$', 'search', name = 'search'),
  url(r'^excerpts/(?P<index_id>\d+)[/]*$', 'excerpts', name = 'excerpts'),
  url(r'^generate/(?P<configuration_id>\d+)[/]*$', 'generate', name = 'generate'),
  url(r'^batch/(?P<action>[a-z]+)/(?P<index_id>\d+)[/]*$', 'batch_indexer', name = 'batch_indexer'),
  url(r'^[/]*$', 'home', name = 'home'),
)

urlpatterns += patterns('techu.admin.views',
  url(r'^admin[/]*$', 'home', name = 'admin_home'),
  url(r'^admin/api-playground/(?P<request_type>[a-z]+)[/]*$', 'api_playground', name = 'admin_api_playground'),
  url(r'^admin/api-playground[/]*$', 'api_playground', name = 'admin_api_playground'),
  url(r'^admin/api[/]*$', 'fetch_api', name = 'fetch_api'),
  url(r'^admin/highlighter[/]*$', 'highlighter', name = 'highlighter'),
)
