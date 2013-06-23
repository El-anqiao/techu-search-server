from django.db import models

class Constants(models.Model):
  '''
  Table constants: various constants (ENUM replacement).
  '''
  table_name = models.CharField()
  table_field = models.CharField()
  constant_name = models.CharField()
  constant_value = models.CharField()
  constant_type = models.CharField()

  def save(self, *args, **kwargs):
    raise NotImplementedError("constants table cannot be edited")
  
  class Meta:
    db_table = "constants"
          
class Configuration(models.Model):
  '''
  Table sp_configurations: stores Sphinx Configurations.
  '''
  name = models.CharField(max_length = 50)
  hash = models.CharField(max_length = 32)
  description = models.TextField()
  is_active = models.PositiveSmallIntegerField(default = 1)
  date_inserted = models.DateTimeField(auto_now_add = True)

  class Meta:
    db_table = "sp_configurations"

class Option(models.Model):
  '''
  Table sp_options: stores available options.
  '''
  name = models.CharField(max_length = 30)
  description = models.TextField()
  possible_values = models.TextField()
  section = models.PositiveSmallIntegerField()

  class Meta:
    db_table = "sp_options"    

class Index(models.Model):
  '''
  Table sp_indexes: stores indexes.
  '''
  name = models.CharField(max_length = 30)
  index_type = models.PositiveSmallIntegerField(default = 1) # 1 -> realtime, 2 -> distributed
  is_active = models.PositiveSmallIntegerField(default = 1)
  parent_id = models.PositiveIntegerField(default = 0)
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_indexes"        

class ConfigurationIndex(models.Model):
  '''
  Table *sp_configuration_index*: stores the connections between configurations and indexes.
  '''
  is_active = models.PositiveSmallIntegerField(default = 1)
  sp_index_id = models.PositiveIntegerField()
  sp_configuration_id = models.PositiveIntegerField()
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_configuration_index"        

class IndexOption(models.Model):
  '''
  Table *sp_index_option*: stores the connections between options and indexes.
  '''
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
  '''
  Table *sp_sources*: stores datasource entities.
  '''
  name = models.CharField(max_length = 30)
  is_active = models.PositiveSmallIntegerField(default = 1)
  parent_id = models.PositiveIntegerField(default = 0)
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_sources"

class Searchd(models.Model):
  '''
  Table *sp_searchd*: stores searchd entities.
  '''
  name = models.CharField(max_length = 30)
  is_active = models.PositiveSmallIntegerField(default = 1)
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)
  date_modified = models.DateTimeField(auto_now = True, auto_now_add = True)

  class Meta:
    db_table = "sp_searchd"
 
class ConfigurationSource(models.Model):
  '''
  Table *sp_configuration_source*: stores the connections between configurations and datasource entities.
  '''
  sp_configuration_id = models.PositiveIntegerField()
  sp_source_id = models.PositiveIntegerField()
  class Meta:
    db_table = "sp_configuration_source"

class ConfigurationSearchd(models.Model):
  '''
  Table *sp_configuration_searchd*: stores the connections between configurations and searchd entities.
  '''
  sp_configuration_id = models.PositiveIntegerField()
  sp_searchd_id = models.PositiveIntegerField()

  class Meta:
    db_table = "sp_configuration_searchd"

class SourceOption(models.Model):
  '''
  Table *sp_source_option*: stores the connections between datasource entities and options.
  '''
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
  '''
  Table *sp_searchd_option*: stores the connections between searchd entities and options.
  '''
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
  '''
  Table *authentication*: stores consumer key/secret pairs for authenticated requests.
  '''
  consumer_key = models.CharField(primary_key = True, max_length = 8)
  secret = models.CharField(max_length = 16)
  date_inserted = models.DateTimeField(auto_now = False, auto_now_add = True)

  class Meta:
    db_table = "authentication"
