techu.views
===========

.. automodule:: techu.views
   :members:
   
   .. py:function:: home(request)
   
     :param request: Request object

     Home/Index page view
   
   .. py:function:: constants()
     
      |  Read all constants values from the database and associate via a 2-level dictionary;
      |  1st level contains *name_of_table_name_of_field* keys and the 2nd level contains the constant value.

   .. py:function:: option_list(request)

      :param request: Request object

      |  Return a list of all available configuration options.
      |  Accepts the *data* parameter with a JSON object containing:

      1. *section* [1, 2, 3, 4] (see *constants* table for value meaning)
      2. *name* filter options by matching the start of their name with this value
      
      Example call::

        curl -k --compressed 'https://techu/option/list/?pretty=1' --data-urlencode data='{ "section" : 4, "name" : "sql_attr" }'
      
      |  Returns all options belonging to datasources starting with "sql_attr".


   .. py:function:: option(request, section, section_instance_id)
   
      :param request: Request object
      :param section: one of ['searchd', 'index', 'source']
      :param section_instance_id: instance identifier *sp_indexes.id*, *sp_searchd.id*, *sp_sources.id*

       
      |  Connect options with searchd, indexes & sources and store their values.
      |  Receives a JSON object with the *data* parameter containing options (keys) and their values.
      |  You can group parameters and assign values with a list.
      
      Example call::

        curl -k --compressed 'https://techu/option/searchd/6/' --data-urlencode data='{
          "listen" : [
            "9312",
            "9306:mysql41"
            ],
          "workers" : "threads",
          "pid_file" : "/var/run/stackoverfow_searchd.pid",
          "max_matches" : 1000
        }'
       
   .. py:function:: index(request, [index_id=0])

      :param request: Request object
      :param index_id: index identifier (*sp_indexes.id*) to be updated

      |  Add or modify information for an index.
      |  It can be associated with a configuration entity with the *configuration_id* parameter.
      
      Example call::
        
        curl -k --compressed 'https://techu/index/' --data-urlencode name='so_posts_rt' --data-urlencode configuration_id='25'

