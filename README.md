Techu v0.1-beta
===============

RESTful search server built on top of Sphinx full-text engine. Uses realtime indexes, Django, Nginx &amp; Redis.


TODO
----
- Complete caching w/ monitoring index changes. 
  * Invalidate all entries on index change (naive approach).
  * Each subsequent request may be returned from cache if no doc_id is changed in the resultset.
  * If records are inserted then perform search from the max doc_id from request time and on (no updates & no deletes).
- Parallelize applier based on doc_id

NOTES
----
* Indexes Backup
  http://sphinxsearch.com/blog/2011/11/18/backing-up-rt-indexes/
* Clustering
  Testing on add/remove node, check node health

