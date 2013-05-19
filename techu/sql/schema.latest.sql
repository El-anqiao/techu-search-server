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

CREATE DATABASE `techu` DEFAULT CHARACTER SET UTF8;
USE `techu`;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-05-19  8:50:55
