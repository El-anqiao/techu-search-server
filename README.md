Techu v0.1-beta
===============

RESTful search server built on top of Sphinx full-text search engine. 

- Organize your Sphinx configurations with Techu database schema
- Reuse index and searchd configurations
- Automatically regenerate configurations and restart searchd
- Easy document indexing using HTTP calls and passing data in JSON format
- Asynchronous execution of statements, using Redis as a buffer
- Bulk insert feature for fast index rebuilding
- Perform full-text search fast using JSON to provide attribute filters, sorting parameters and grouping
- Retrieve highlighted excerpts (snippets) from documents, compliant with the search query syntax
- Cache search results and excerpts directly to Redis

Components:
* Realtime indexes
* Django Framework
* Nginx web server
* Redis in-memory key-value storage
* MySQL

Take a look at the [overview page](http://georgepsarakis.github.io/techu-search-server/).

-----

Still a beta version and requires a lot of work to be done (and much more documentation as well, especially regarding the */search* request!). I am also preparing some benchmarks. I would be very thankful for any constructive criticism and anyone willing to test it!

Stay tuned!

TODO
----
- Complete caching w/ monitoring index changes. 
  * Invalidate all entries on index change (naive approach).
  * Each subsequent request may be returned from cache if no doc_id is changed in the resultset.
  * If records are inserted then perform search from the max doc_id from request time and on (no updates & no deletes).
- Parallelize applier based on doc_id
- Revisions for configuration options


