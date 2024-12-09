-- MySQL dump 10.13  Distrib 8.0.40, for Linux (x86_64)
--
-- Host: localhost    Database: bp_db
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `api_answer`
--

DROP TABLE IF EXISTS `api_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_answer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `answer` varchar(255) NOT NULL,
  `example_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_answer_example_id_0d2becad` (`example_id`),
  CONSTRAINT `api_answer_example_id_0d2becad_fk_api_example_id` FOREIGN KEY (`example_id`) REFERENCES `api_example` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_answer`
--

LOCK TABLES `api_answer` WRITE;
/*!40000 ALTER TABLE `api_answer` DISABLE KEYS */;
INSERT INTO `api_answer` VALUES (3,'2.4',3),(4,'3.8',4),(5,'\\frac{6}{5}',5),(6,'\\frac{5}{3}',6),(7,'a=2;',7),(8,'c=0;',8),(9,'x\\in(1;+\\infty)',9),(10,'x\\in(-\\infty;-3)',10),(11,'13,4',11),(12,'65,25',12),(13,'9,42',13),(14,'0,44',14),(15,'20,625',15),(16,'0,06',16),(17,'0,6',17),(18,'0,0004',18),(19,'15',19),(20,'1,9 ',20),(21,'\\frac{8}{9}',21);
/*!40000 ALTER TABLE `api_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_example`
--

DROP TABLE IF EXISTS `api_example`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_example` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `example` varchar(255) NOT NULL,
  `input_type` varchar(255) NOT NULL,
  `task_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_example_task_id_db065479_fk_api_task_id` (`task_id`),
  CONSTRAINT `api_example_task_id_db065479_fk_api_task_id` FOREIGN KEY (`task_id`) REFERENCES `api_task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_example`
--

LOCK TABLES `api_example` WRITE;
/*!40000 ALTER TABLE `api_example` DISABLE KEYS */;
INSERT INTO `api_example` VALUES (3,'1.6+0.8','INLINE',2),(4,'4.3-0.5','INLINE',2),(5,'\\frac{2}{5}+\\frac{4}{5}','FRAC',3),(6,'\\frac{7}{3}-\\frac{2}{3}','FRAC',3),(7,'4a-5=3(3-a)','VAR',4),(8,'2=2(5c+1)','VAR',4),(9,'4x+1 >2x+3','SET',5),(10,'7x-1 < 4x-10','SET',5),(11,'3,25+10,15','INLINE',6),(12,'65,07+0,18','INLINE',6),(13,'7,42+2','INLINE',6),(14,'0,4+0,04','INLINE',6),(15,'17,6+3,025','INLINE',6),(16,'0,3 \\cdot 0,2','INLINE',7),(17,'30 \\cdot 0,02','INLINE',7),(18,'0,02 \\cdot 0,02','INLINE',7),(19,'50\\cdot0,3','INLINE',7),(20,'1,4 + 0,5','INLINE',8),(21,'\\frac{4}{6}:\\frac{3}{4}','FRAC',9);
/*!40000 ALTER TABLE `api_example` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_exampleskill`
--

DROP TABLE IF EXISTS `api_exampleskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_exampleskill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `example_id` bigint NOT NULL,
  `skill_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_exampleskill_example_id_91586a5c_fk_api_example_id` (`example_id`),
  KEY `api_exampleskill_skill_id_2d0bbbeb_fk_api_skill_id` (`skill_id`),
  CONSTRAINT `api_exampleskill_example_id_91586a5c_fk_api_example_id` FOREIGN KEY (`example_id`) REFERENCES `api_example` (`id`),
  CONSTRAINT `api_exampleskill_skill_id_2d0bbbeb_fk_api_skill_id` FOREIGN KEY (`skill_id`) REFERENCES `api_skill` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_exampleskill`
--

LOCK TABLES `api_exampleskill` WRITE;
/*!40000 ALTER TABLE `api_exampleskill` DISABLE KEYS */;
INSERT INTO `api_exampleskill` VALUES (1,3,2),(2,4,2),(3,5,9),(4,6,9),(5,7,5),(6,8,5),(7,9,7),(8,10,7),(9,11,2),(10,12,2),(11,13,2),(12,14,2),(13,15,2),(14,16,3),(15,17,3),(16,18,3),(17,19,3),(18,20,2),(19,21,11);
/*!40000 ALTER TABLE `api_exampleskill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_skill`
--

DROP TABLE IF EXISTS `api_skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_skill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `parent_skill_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_skill_parent_skill_id_4f71e207_fk_api_skill_id` (`parent_skill_id`),
  CONSTRAINT `api_skill_parent_skill_id_4f71e207_fk_api_skill_id` FOREIGN KEY (`parent_skill_id`) REFERENCES `api_skill` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_skill`
--

LOCK TABLES `api_skill` WRITE;
/*!40000 ALTER TABLE `api_skill` DISABLE KEYS */;
INSERT INTO `api_skill` VALUES (1,'Desetinná čísla',NULL),(2,'Sčítání a odčítání desetinných čísel',1),(3,'Násobení a dělení desetinných čísel',1),(4,'Rovnice',NULL),(5,'Lineární rovnice s jednou neznámou',4),(6,'Nerovnice',NULL),(7,'Lineární nerovnice',6),(8,'Zlomky',NULL),(9,'Sčítání a odčítání zlomků',8),(10,'Násobení zlomků',8),(11,'Dělení zlomků',8),(12,'Lomené výrazy',NULL),(13,'Krácení lomených výrazů',12),(14,'Sčítání a odčítání lomených výrazů',12),(15,'Násobení lomených výrazů',12),(16,'Dělení lomených výrazů',12);
/*!40000 ALTER TABLE `api_skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_student`
--

DROP TABLE IF EXISTS `api_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `passphrase` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_student`
--

LOCK TABLES `api_student` WRITE;
/*!40000 ALTER TABLE `api_student` DISABLE KEYS */;
INSERT INTO `api_student` VALUES (1,'student','heslo');
/*!40000 ALTER TABLE `api_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_studentexample`
--

DROP TABLE IF EXISTS `api_studentexample`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_studentexample` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `duration` int NOT NULL,
  `example_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  `attempts` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_student_example_date` (`student_id`,`example_id`,`date`),
  KEY `api_studentexample_example_id_11753758_fk_api_example_id` (`example_id`),
  CONSTRAINT `api_studentexample_example_id_11753758_fk_api_example_id` FOREIGN KEY (`example_id`) REFERENCES `api_example` (`id`),
  CONSTRAINT `api_studentexample_student_id_fdab9eb2_fk_api_student_id` FOREIGN KEY (`student_id`) REFERENCES `api_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_studentexample`
--

LOCK TABLES `api_studentexample` WRITE;
/*!40000 ALTER TABLE `api_studentexample` DISABLE KEYS */;
INSERT INTO `api_studentexample` VALUES (21,'2024-12-04 15:59:56.808467',4,3,1,2),(22,'2024-12-04 16:00:01.589486',11,4,1,2),(23,'2024-12-04 16:00:13.004742',8,11,1,1),(24,'2024-12-04 16:00:21.749820',14,12,1,3),(25,'2024-12-04 16:00:36.311341',7,13,1,1),(26,'2024-12-04 16:00:43.677568',5,14,1,1),(27,'2024-12-04 16:00:49.050285',5,15,1,1),(28,'2024-12-04 20:54:05.960439',0,3,1,2),(29,'2024-12-04 20:54:22.011668',0,3,1,1),(30,'2024-12-04 20:54:26.848655',0,3,1,1),(31,'2024-12-04 20:55:06.398642',0,3,1,1),(32,'2024-12-04 20:55:11.070848',0,3,1,3),(33,'2024-12-04 20:55:43.623850',0,3,1,1),(34,'2024-12-05 09:44:50.848141',4,16,1,1),(35,'2024-12-05 09:44:55.149778',9,17,1,2),(36,'2024-12-05 09:45:05.033872',3,18,1,1),(37,'2024-12-05 09:45:08.559036',2,19,1,1),(38,'2024-12-08 21:28:01.558629',2,3,1,1),(39,'2024-12-08 21:28:04.351885',0,4,1,1),(40,'2024-12-08 22:44:16.910564',0,3,1,1),(41,'2024-12-09 13:00:03.814407',0,3,1,1),(42,'2024-12-09 13:00:09.630780',1,3,1,1),(43,'2024-12-09 13:00:11.627018',0,4,1,1),(44,'2024-12-09 15:51:36.686767',0,3,1,1),(45,'2024-12-09 15:58:25.459715',0,21,1,1),(46,'2024-12-09 16:40:22.119984',0,21,1,1);
/*!40000 ALTER TABLE `api_studentexample` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_task`
--

DROP TABLE IF EXISTS `api_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_task`
--

LOCK TABLES `api_task` WRITE;
/*!40000 ALTER TABLE `api_task` DISABLE KEYS */;
INSERT INTO `api_task` VALUES (1,'Test 1'),(2,'Test 2'),(3,'Test 3'),(4,'Test 4'),(5,'Test 5'),(6,'Desetinná čísla I'),(7,'Násobení des. č.'),(8,'test post'),(9,'Testovaci priklady');
/*!40000 ALTER TABLE `api_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add example',7,'add_example'),(26,'Can change example',7,'change_example'),(27,'Can delete example',7,'delete_example'),(28,'Can view example',7,'view_example'),(29,'Can add task',8,'add_task'),(30,'Can change task',8,'change_task'),(31,'Can delete task',8,'delete_task'),(32,'Can view task',8,'view_task'),(33,'Can add skill',9,'add_skill'),(34,'Can change skill',9,'change_skill'),(35,'Can delete skill',9,'delete_skill'),(36,'Can view skill',9,'view_skill'),(37,'Can add example skill',10,'add_exampleskill'),(38,'Can change example skill',10,'change_exampleskill'),(39,'Can delete example skill',10,'delete_exampleskill'),(40,'Can view example skill',10,'view_exampleskill'),(41,'Can add answer',11,'add_answer'),(42,'Can change answer',11,'change_answer'),(43,'Can delete answer',11,'delete_answer'),(44,'Can view answer',11,'view_answer'),(45,'Can add student',12,'add_student'),(46,'Can change student',12,'change_student'),(47,'Can delete student',12,'delete_student'),(48,'Can view student',12,'view_student'),(49,'Can add student example',13,'add_studentexample'),(50,'Can change student example',13,'change_studentexample'),(51,'Can delete student example',13,'delete_studentexample'),(52,'Can view student example',13,'view_studentexample');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(11,'api','answer'),(7,'api','example'),(10,'api','exampleskill'),(9,'api','skill'),(12,'api','student'),(13,'api','studentexample'),(8,'api','task'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-11-09 14:02:53.116604'),(2,'auth','0001_initial','2024-11-09 14:02:54.308895'),(3,'admin','0001_initial','2024-11-09 14:02:54.590017'),(4,'admin','0002_logentry_remove_auto_add','2024-11-09 14:02:54.614968'),(5,'admin','0003_logentry_add_action_flag_choices','2024-11-09 14:02:54.634830'),(7,'api','0002_skill_parent_skill','2024-11-09 14:02:55.241649'),(8,'contenttypes','0002_remove_content_type_name','2024-11-09 14:05:54.024993'),(9,'auth','0002_alter_permission_name_max_length','2024-11-09 14:05:54.156467'),(10,'auth','0003_alter_user_email_max_length','2024-11-09 14:05:54.249139'),(11,'auth','0004_alter_user_username_opts','2024-11-09 14:05:54.276498'),(12,'auth','0005_alter_user_last_login_null','2024-11-09 14:05:54.417960'),(13,'auth','0006_require_contenttypes_0002','2024-11-09 14:05:54.423719'),(14,'auth','0007_alter_validators_add_error_messages','2024-11-09 14:05:54.454119'),(15,'auth','0008_alter_user_username_max_length','2024-11-09 14:05:54.612470'),(16,'auth','0009_alter_user_last_name_max_length','2024-11-09 14:05:54.809100'),(17,'auth','0010_alter_group_name_max_length','2024-11-09 14:05:54.866347'),(18,'auth','0011_update_proxy_permissions','2024-11-09 14:05:54.891841'),(19,'auth','0012_alter_user_first_name_max_length','2024-11-09 14:05:55.037956'),(20,'sessions','0001_initial','2024-11-09 14:05:55.120959'),(21,'api','0001_initial','2024-11-10 19:20:57.613069'),(22,'api','0002_alter_answer_unique_together_remove_answer_step_num','2024-11-10 19:20:57.754494'),(23,'api','0003_student_studentexample','2024-11-14 09:38:13.530828'),(24,'api','0004_studentexample_attempts_and_more','2024-12-03 12:14:54.467292'),(25,'api','0005_alter_studentexample_duration','2024-12-04 10:20:56.463521');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-09 23:31:21
