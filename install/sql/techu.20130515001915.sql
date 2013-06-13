-- MySQL dump 10.13  Distrib 5.5.29, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: techu
-- ------------------------------------------------------
-- Server version	5.5.29-0ubuntu0.12.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `constants`
--

DROP TABLE IF EXISTS `constants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `constants` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `table_name` varchar(30) DEFAULT NULL,
  `table_field` varchar(30) DEFAULT NULL,
  `constant_name` varchar(30) DEFAULT NULL,
  `constant_value` varchar(30) DEFAULT NULL,
  `constant_type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `constants`
--

LOCK TABLES `constants` WRITE;
/*!40000 ALTER TABLE `constants` DISABLE KEYS */;
INSERT INTO `constants` VALUES (1,'sp_options','section','OPTION_SECTION_INDEXER','1','int'),(2,'sp_options','section','OPTION_SECTION_INDEX','2','int'),(3,'sp_options','section','OPTION_SECTION_SEARCHD','3','int'),(4,'sp_options','section','OPTION_SECTION_DATASOURCE','4','int');
/*!40000 ALTER TABLE `constants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_configuration_index`
--

DROP TABLE IF EXISTS `sp_configuration_index`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_configuration_index` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sp_configuration_id` int(10) unsigned DEFAULT NULL,
  `sp_index_id` int(10) unsigned DEFAULT NULL,
  `is_active` tinyint(3) unsigned DEFAULT '0',
  `date_inserted` timestamp NULL DEFAULT NULL,
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_configuration_index`
--

LOCK TABLES `sp_configuration_index` WRITE;
/*!40000 ALTER TABLE `sp_configuration_index` DISABLE KEYS */;
INSERT INTO `sp_configuration_index` VALUES (1,1,22,1,'2013-04-27 13:36:10','2013-04-27 13:36:10'),(2,9,23,1,'2013-04-27 14:09:09','2013-04-27 14:09:09');
/*!40000 ALTER TABLE `sp_configuration_index` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_configuration_searchd`
--

DROP TABLE IF EXISTS `sp_configuration_searchd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_configuration_searchd` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sp_configuration_id` int(10) unsigned DEFAULT NULL,
  `sp_searchd_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sp_configuration_id` (`sp_configuration_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_configuration_searchd`
--

LOCK TABLES `sp_configuration_searchd` WRITE;
/*!40000 ALTER TABLE `sp_configuration_searchd` DISABLE KEYS */;
INSERT INTO `sp_configuration_searchd` VALUES (1,9,1);
/*!40000 ALTER TABLE `sp_configuration_searchd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_configuration_source`
--

DROP TABLE IF EXISTS `sp_configuration_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_configuration_source` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sp_configuration_id` int(10) unsigned DEFAULT NULL,
  `sp_source_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sp_configuration_id` (`sp_configuration_id`,`sp_source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_configuration_source`
--

LOCK TABLES `sp_configuration_source` WRITE;
/*!40000 ALTER TABLE `sp_configuration_source` DISABLE KEYS */;
/*!40000 ALTER TABLE `sp_configuration_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_configurations`
--

DROP TABLE IF EXISTS `sp_configurations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_configurations` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `hash` char(32) DEFAULT NULL,
  `description` text,
  `is_active` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `last_generated` timestamp NULL DEFAULT NULL,
  `date_inserted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_configurations`
--

LOCK TABLES `sp_configurations` WRITE;
/*!40000 ALTER TABLE `sp_configurations` DISABLE KEYS */;
INSERT INTO `sp_configurations` VALUES (9,'test','b1a4f059a55cf2f63e7996fe06adf199','',1,NULL,'2013-04-27 14:06:11'),(25,'stackoverflow','46ee0a09bcbb064b49b224a9e8efd39a','StackOverflow Posts Indexing Configuration',1,NULL,'2013-05-14 16:29:49');
/*!40000 ALTER TABLE `sp_configurations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_group_options`
--

DROP TABLE IF EXISTS `sp_group_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_group_options` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_group_options`
--

LOCK TABLES `sp_group_options` WRITE;
/*!40000 ALTER TABLE `sp_group_options` DISABLE KEYS */;
/*!40000 ALTER TABLE `sp_group_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_index_option`
--

DROP TABLE IF EXISTS `sp_index_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_index_option` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sp_index_id` int(10) unsigned NOT NULL,
  `sp_option_id` smallint(5) unsigned NOT NULL,
  `value` text,
  `value_hash` char(32) DEFAULT NULL,
  `is_active` tinyint(3) unsigned DEFAULT '1',
  `date_inserted` timestamp NULL DEFAULT NULL,
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sp_index_id` (`sp_index_id`,`sp_option_id`,`value_hash`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_index_option`
--

LOCK TABLES `sp_index_option` WRITE;
/*!40000 ALTER TABLE `sp_index_option` DISABLE KEYS */;
INSERT INTO `sp_index_option` VALUES (1,23,53,'title',NULL,1,NULL,'2013-05-07 07:23:53'),(2,23,53,'content',NULL,1,NULL,'2013-05-07 07:24:02'),(3,23,3,'/usr/local/sphinx/data/rt',NULL,1,NULL,'2013-05-07 07:24:26'),(4,23,1,'rt',NULL,1,NULL,'2013-05-07 07:24:45'),(5,23,54,'gid',NULL,1,NULL,'2013-05-07 07:25:11');
/*!40000 ALTER TABLE `sp_index_option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_indexes`
--

DROP TABLE IF EXISTS `sp_indexes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_indexes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `index_type` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `parent_id` int(10) unsigned DEFAULT '0',
  `is_active` tinyint(3) unsigned DEFAULT '0',
  `date_inserted` timestamp NULL DEFAULT NULL,
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_indexes`
--

LOCK TABLES `sp_indexes` WRITE;
/*!40000 ALTER TABLE `sp_indexes` DISABLE KEYS */;
INSERT INTO `sp_indexes` VALUES (23,'rt',1,0,1,'2013-04-27 14:09:09','2013-05-06 18:29:48');
/*!40000 ALTER TABLE `sp_indexes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_options`
--

DROP TABLE IF EXISTS `sp_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_options` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `description` text,
  `section` tinyint(3) unsigned NOT NULL DEFAULT '1',
  `sp_group_option_id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `possible_values` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=189 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_options`
--

LOCK TABLES `sp_options` WRITE;
/*!40000 ALTER TABLE `sp_options` DISABLE KEYS */;
INSERT INTO `sp_options` VALUES (1,'type',NULL,2,0,''),(2,'source',NULL,2,0,''),(3,'path',NULL,2,0,''),(4,'docinfo',NULL,2,0,''),(5,'mlock',NULL,2,0,''),(6,'morphology',NULL,2,0,''),(7,'dict',NULL,2,0,''),(8,'index_sp',NULL,2,0,''),(9,'index_zones',NULL,2,0,''),(10,'min_stemming_len',NULL,2,0,''),(11,'stopwords',NULL,2,0,''),(12,'wordforms',NULL,2,0,''),(13,'embedded_limit',NULL,2,0,''),(14,'exceptions',NULL,2,0,''),(15,'min_word_len',NULL,2,0,''),(16,'charset_type',NULL,2,0,''),(17,'charset_table',NULL,2,0,''),(18,'ignore_chars',NULL,2,0,''),(19,'min_prefix_len',NULL,2,0,''),(20,'min_infix_len',NULL,2,0,''),(21,'max_substring_len',NULL,2,0,''),(22,'prefix_fields',NULL,2,0,''),(23,'infix_fields',NULL,2,0,''),(24,'enable_star',NULL,2,0,''),(25,'ngram_len',NULL,2,0,''),(26,'ngram_chars',NULL,2,0,''),(27,'phrase_boundary',NULL,2,0,''),(28,'phrase_boundary_step',NULL,2,0,''),(29,'html_strip',NULL,2,0,''),(30,'html_index_attrs',NULL,2,0,''),(31,'html_remove_elements',NULL,2,0,''),(32,'local',NULL,2,0,''),(33,'agent',NULL,2,0,''),(34,'agent_persistent',NULL,2,0,''),(35,'agent_blackhole',NULL,2,0,''),(36,'agent_connect_timeout',NULL,2,0,''),(37,'agent_query_timeout',NULL,2,0,''),(38,'preopen',NULL,2,0,''),(39,'ondisk_dict',NULL,2,0,''),(40,'inplace_enable',NULL,2,0,''),(41,'inplace_hit_gap',NULL,2,0,''),(42,'inplace_docinfo_gap',NULL,2,0,''),(43,'inplace_reloc_factor',NULL,2,0,''),(44,'inplace_write_factor',NULL,2,0,''),(45,'index_exact_words',NULL,2,0,''),(46,'overshort_step',NULL,2,0,''),(47,'stopword_step',NULL,2,0,''),(48,'hitless_words',NULL,2,0,''),(49,'expand_keywords',NULL,2,0,''),(50,'blend_chars',NULL,2,0,''),(51,'blend_mode',NULL,2,0,''),(52,'rt_mem_limit',NULL,2,0,''),(53,'rt_field',NULL,2,0,''),(54,'rt_attr_uint',NULL,2,0,''),(55,'rt_attr_bigint',NULL,2,0,''),(56,'rt_attr_float',NULL,2,0,''),(57,'rt_attr_multi',NULL,2,0,''),(58,'rt_attr_multi_64',NULL,2,0,''),(59,'rt_attr_timestamp',NULL,2,0,''),(60,'rt_attr_string',NULL,2,0,''),(61,'rt_attr_json',NULL,2,0,''),(62,'ha_strategy',NULL,2,0,''),(63,'bigram_freq_words',NULL,2,0,''),(64,'bigram_index',NULL,2,0,''),(65,'index_field_lengths',NULL,2,0,''),(66,'regexp_filter',NULL,2,0,''),(67,'stopwords_unstemmed',NULL,2,0,''),(68,'global_idf',NULL,2,0,''),(70,'sql_host',NULL,4,0,''),(71,'sql_port',NULL,4,0,'INT'),(72,'sql_user',NULL,4,0,''),(73,'sql_pass',NULL,4,0,''),(74,'sql_db',NULL,4,0,''),(75,'sql_sock',NULL,4,0,'PATH'),(76,'json_autoconv_numbers',NULL,4,0,'FLAG'),(77,'json_autoconv_keynames',NULL,4,0,'OMIT|lowercase'),(78,'on_json_attr_error',NULL,4,0,'ignore_attr,fail_index'),(79,'mysql_connect_flags',NULL,4,0,'INT'),(80,'mysql_ssl_cert',NULL,4,0,'PATH'),(81,'mysql_ssl_key',NULL,4,0,'PATH'),(82,'mysql_ssl_ca',NULL,4,0,'PATH'),(83,'odbc_dsn',NULL,4,0,''),(84,'sql_query_pre',NULL,4,0,'SQL'),(85,'sql_query',NULL,4,0,'SQL'),(86,'sql_joined_field',NULL,4,0,'SQL_MIXED'),(87,'sql_query_range',NULL,4,0,'SQL'),(88,'sql_range_step',NULL,4,0,'INT'),(89,'sql_query_killlist',NULL,4,0,'SQL'),(90,'sql_attr_uint',NULL,4,0,'FIELD'),(91,'sql_attr_bool',NULL,4,0,'FIELD'),(92,'sql_attr_bigint',NULL,4,0,'FIELD'),(93,'sql_attr_timestamp',NULL,4,0,'FIELD'),(94,'sql_attr_str2ordinal',NULL,4,0,'FIELD'),(95,'sql_attr_float',NULL,4,0,'FIELD'),(96,'sql_attr_multi',NULL,4,0,'SQL_MIXED'),(97,'sql_attr_string',NULL,4,0,'FIELD'),(98,'sql_attr_json',NULL,4,0,'FIELD'),(99,'sql_attr_str2wordcount',NULL,4,0,'FIELD'),(100,'sql_column_buffers',NULL,4,0,'BYTESIZE'),(101,'sql_field_string',NULL,4,0,'FIELD'),(102,'sql_field_str2wordcount',NULL,4,0,'FIELD'),(103,'sql_file_field',NULL,4,0,'FIELD'),(104,'sql_query_post',NULL,4,0,'SQL'),(105,'sql_query_post_index',NULL,4,0,'SQL'),(106,'sql_ranged_throttle',NULL,4,0,'INT'),(107,'sql_query_info',NULL,4,0,'SQL'),(108,'xmlpipe_command',NULL,4,0,''),(109,'xmlpipe_field',NULL,4,0,''),(110,'xmlpipe_field_string',NULL,4,0,''),(111,'xmlpipe_field_wordcount',NULL,4,0,''),(112,'xmlpipe_attr_uint',NULL,4,0,''),(113,'xmlpipe_attr_bigint',NULL,4,0,''),(114,'xmlpipe_attr_bool',NULL,4,0,''),(115,'xmlpipe_attr_timestamp',NULL,4,0,''),(116,'xmlpipe_attr_str2ordinal',NULL,4,0,''),(117,'xmlpipe_attr_float',NULL,4,0,''),(118,'xmlpipe_attr_multi',NULL,4,0,''),(119,'xmlpipe_attr_multi_64',NULL,4,0,''),(120,'xmlpipe_attr_string',NULL,4,0,''),(121,'xmlpipe_attr_wordcount',NULL,4,0,''),(122,'xmlpipe_attr_json',NULL,4,0,''),(123,'xmlpipe_fixup_utf8',NULL,4,0,''),(124,'mssql_winauth',NULL,4,0,''),(125,'mssql_unicode',NULL,4,0,''),(126,'unpack_zlib',NULL,4,0,''),(127,'unpack_mysqlcompress',NULL,4,0,''),(128,'unpack_mysqlcompress_maxsize',NULL,4,0,''),(129,'mem_limit',NULL,1,0,''),(130,'max_iops',NULL,1,0,''),(131,'max_iosize',NULL,1,0,''),(132,'max_xmlpipe2_field',NULL,1,0,''),(133,'write_buffer',NULL,1,0,''),(134,'max_file_field_buffer',NULL,1,0,''),(135,'on_file_field_error',NULL,1,0,''),(136,'lemmatizer_base',NULL,1,0,''),(137,'lemmatizer_cache',NULL,1,0,''),(138,'listen',NULL,3,0,''),(139,'address',NULL,3,0,''),(140,'port',NULL,3,0,''),(141,'log',NULL,3,0,''),(142,'query_log',NULL,3,0,''),(143,'query_log_format',NULL,3,0,''),(144,'read_timeout',NULL,3,0,''),(145,'client_timeout',NULL,3,0,''),(146,'max_children',NULL,3,0,''),(147,'pid_file',NULL,3,0,''),(148,'max_matches',NULL,3,0,''),(149,'seamless_rotate',NULL,3,0,''),(150,'preopen_indexes',NULL,3,0,''),(151,'unlink_old',NULL,3,0,''),(152,'attr_flush_period',NULL,3,0,''),(153,'ondisk_dict_default',NULL,3,0,''),(154,'max_packet_size',NULL,3,0,''),(155,'mva_updates_pool',NULL,3,0,''),(156,'crash_log_path',NULL,3,0,''),(157,'max_filters',NULL,3,0,''),(158,'max_filter_values',NULL,3,0,''),(159,'listen_backlog',NULL,3,0,''),(160,'read_buffer',NULL,3,0,''),(161,'read_unhinted',NULL,3,0,''),(162,'max_batch_queries',NULL,3,0,''),(163,'subtree_docs_cache',NULL,3,0,''),(164,'subtree_hits_cache',NULL,3,0,''),(165,'workers',NULL,3,0,''),(166,'dist_threads',NULL,3,0,''),(167,'binlog_path',NULL,3,0,''),(168,'binlog_flush',NULL,3,0,''),(169,'binlog_max_log_size',NULL,3,0,''),(170,'snippets_file_prefix',NULL,3,0,''),(171,'collation_server',NULL,3,0,''),(172,'collation_libc_locale',NULL,3,0,''),(173,'plugin_dir',NULL,3,0,''),(174,'mysql_version_string',NULL,3,0,''),(175,'rt_flush_period',NULL,3,0,''),(176,'thread_stack',NULL,3,0,''),(177,'expansion_limit',NULL,3,0,''),(178,'compat_sphinxql_magics',NULL,3,0,''),(179,'watchdog',NULL,3,0,''),(180,'prefork_rotation_throttle',NULL,3,0,''),(181,'sphinxql_state',NULL,3,0,''),(182,'ha_ping_interval',NULL,3,0,''),(183,'ha_period_karma',NULL,3,0,''),(184,'persistent_connections_limit',NULL,3,0,''),(185,'rt_merge_iops',NULL,3,0,''),(186,'rt_merge_maxiosize',NULL,3,0,''),(187,'predicted_time_costs',NULL,3,0,''),(188,'sphinx_host','The host of the Sphinx server',0,0,NULL);
/*!40000 ALTER TABLE `sp_options` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_searchd`
--

DROP TABLE IF EXISTS `sp_searchd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_searchd` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `is_active` tinyint(3) unsigned DEFAULT '0',
  `date_inserted` timestamp NULL DEFAULT NULL,
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_searchd`
--

LOCK TABLES `sp_searchd` WRITE;
/*!40000 ALTER TABLE `sp_searchd` DISABLE KEYS */;
INSERT INTO `sp_searchd` VALUES (1,'test-searchd',1,NULL,'2013-05-07 07:17:17');
/*!40000 ALTER TABLE `sp_searchd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_searchd_option`
--

DROP TABLE IF EXISTS `sp_searchd_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_searchd_option` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sp_searchd_id` int(10) unsigned NOT NULL,
  `sp_option_id` smallint(5) unsigned NOT NULL,
  `value` text,
  `value_hash` char(32) DEFAULT NULL,
  `is_active` tinyint(3) unsigned DEFAULT '1',
  `date_inserted` timestamp NULL DEFAULT NULL,
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sp_searchd_id` (`sp_searchd_id`,`sp_option_id`,`value_hash`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_searchd_option`
--

LOCK TABLES `sp_searchd_option` WRITE;
/*!40000 ALTER TABLE `sp_searchd_option` DISABLE KEYS */;
INSERT INTO `sp_searchd_option` VALUES (1,1,138,'9312',NULL,1,NULL,'2013-05-07 07:18:33'),(2,1,138,'9306:mysql41',NULL,1,NULL,'2013-05-08 20:17:47'),(3,1,141,'/var/log/sphinxsearch/searchd.log',NULL,1,NULL,'2013-05-07 07:21:02'),(4,1,142,'/var/log/sphinxsearch/query.log',NULL,1,NULL,'2013-05-07 07:21:10'),(5,1,165,'threads',NULL,1,NULL,'2013-05-07 07:21:32'),(6,1,147,'/var/run/searchd.pid',NULL,1,NULL,'2013-05-07 07:21:57'),(7,1,148,'1000',NULL,1,NULL,'2013-05-07 07:22:10');
/*!40000 ALTER TABLE `sp_searchd_option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_source_option`
--

DROP TABLE IF EXISTS `sp_source_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_source_option` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sp_source_id` int(10) unsigned NOT NULL,
  `sp_option_id` smallint(5) unsigned NOT NULL,
  `value` text,
  `value_hash` char(32) DEFAULT NULL,
  `is_active` tinyint(3) unsigned DEFAULT '1',
  `date_inserted` timestamp NULL DEFAULT NULL,
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sp_source_id` (`sp_source_id`,`sp_option_id`,`value_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_source_option`
--

LOCK TABLES `sp_source_option` WRITE;
/*!40000 ALTER TABLE `sp_source_option` DISABLE KEYS */;
/*!40000 ALTER TABLE `sp_source_option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sp_sources`
--

DROP TABLE IF EXISTS `sp_sources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sp_sources` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `parent_id` int(10) unsigned DEFAULT '0',
  `is_active` tinyint(3) unsigned DEFAULT '0',
  `date_inserted` timestamp NULL DEFAULT NULL,
  `date_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sp_sources`
--

LOCK TABLES `sp_sources` WRITE;
/*!40000 ALTER TABLE `sp_sources` DISABLE KEYS */;
/*!40000 ALTER TABLE `sp_sources` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-05-15  0:19:15
