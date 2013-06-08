from django.db import models

class Configuration(models.Model):
  name = models.CharField(max_length = 50)
  hash = models.CharField(max_length = 32)
  description = models.TextField()
  is_active = models.PositiveSmallIntegerField(default = 1)
  date_inserted = models.DateTimeField(auto_now_add = True)

  class Meta:
    db_table = "sp_configurations"

class Option(models.Model):
  name = models.CharField(max_length = 30)
  description = models.TextField()
  possible_values = models.TextField()
  section = models.PositiveSmallIntegerField()

  class Meta:
    db_table = "sp_options"    

class Index(models.Model):
  name = models.CharField(max_length = 30)
  index_type = models.PositiveSmallIntegerField(default = 1) # 1 -> realtime, 2 -> distributed
  is_active = models.PositiveSmallIntegerField(default = 1)
  parent_id = models.PositiveIntegerField(default = 0)
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_indexes"        

class ConfigurationIndex(models.Model):
  is_active = models.PositiveSmallIntegerField(default = 1)
  sp_index_id = models.PositiveIntegerField()
  sp_configuration_id = models.PositiveIntegerField()
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_configuration_index"        

class IndexOption(models.Model):
  sp_index_id = models.PositiveIntegerField()
  sp_option_id = models.PositiveIntegerField()
  value = models.TextField()
  value_hash = models.CharField(max_length = 32)
  is_active = models.PositiveSmallIntegerField()
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_index_option"
 
class Sources(models.Model):
  name = models.CharField(max_length = 30)
  is_active = models.PositiveSmallIntegerField(default = 1)
  parent_id = models.PositiveIntegerField(default = 0)
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_sources"

class Searchd(models.Model):
  name = models.CharField(max_length = 30)
  is_active = models.PositiveSmallIntegerField(default = 1)
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_searchd"
 
class ConfigurationSource(models.Model):
  sp_configuration_id = models.PositiveIntegerField()
  sp_source_id = models.PositiveIntegerField()
  class Meta:
    db_table = "sp_configuration_source"

class ConfigurationSearchd(models.Model):
  sp_configuration_id = models.PositiveIntegerField()
  sp_searchd_id = models.PositiveIntegerField()

  class Meta:
    db_table = "sp_configuration_searchd"

class SourceOption(models.Model):
  sp_source_id = models.PositiveIntegerField()
  sp_option_id = models.PositiveIntegerField()
  value = models.TextField()
  value_hash = models.CharField(max_length = 32)
  is_active = models.PositiveSmallIntegerField()
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_source_option"
 
class SearchdOption(models.Model):
  sp_searchd_id = models.PositiveIntegerField()
  sp_option_id = models.PositiveIntegerField()
  value = models.TextField()
  value_hash = models.CharField(max_length = 32)
  is_active = models.PositiveSmallIntegerField()
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_searchd_option"

class Authentication(models.Model):
  consumer_key = models.CharField(primary_key = True, max_length = 8)
  secret = models.CharField(max_length = 16)
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)

  class Meta:
    db_table = "authentication"
