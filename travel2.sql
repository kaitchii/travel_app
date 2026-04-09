/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.5-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: travel
-- ------------------------------------------------------
-- Server version	11.8.5-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `budget`
--

DROP TABLE IF EXISTS `budget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `budget` (
  `budget_id` int(11) NOT NULL AUTO_INCREMENT,
  `min_budget` int(11) NOT NULL,
  `max_budget` int(11) NOT NULL,
  `place_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`budget_id`),
  KEY `budget_rec_travel_FK` (`place_id`),
  CONSTRAINT `budget_rec_travel_FK` FOREIGN KEY (`place_id`) REFERENCES `rec_travel` (`place_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budget`
--

LOCK TABLES `budget` WRITE;
/*!40000 ALTER TABLE `budget` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `budget` VALUES
(1,200,800,1),
(2,1500,4000,2),
(3,800,2500,3),
(4,100,500,4),
(5,300,1200,5),
(6,100,400,6);
/*!40000 ALTER TABLE `budget` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `rec_travel`
--

DROP TABLE IF EXISTS `rec_travel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `rec_travel` (
  `place_id` int(11) NOT NULL AUTO_INCREMENT,
  `place_name` varchar(100) NOT NULL,
  `place_descript` varchar(100) NOT NULL,
  `place_image` varchar(300) NOT NULL,
  `rating` float NOT NULL,
  `openning_hr` varchar(100) NOT NULL,
  `style_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`place_id`),
  KEY `rec_travel_style_travel_FK` (`style_id`),
  CONSTRAINT `rec_travel_style_travel_FK` FOREIGN KEY (`style_id`) REFERENCES `style_travel` (`style_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec_travel`
--

LOCK TABLES `rec_travel` WRITE;
/*!40000 ALTER TABLE `rec_travel` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `rec_travel` VALUES
(1,'Wat Phra Kaew','Famous temple with Emerald Buddha','https://static.thairath.co.th/media/dFQROr7oWzulq5FZUEh3MRrERXP2ZCRNt1ty78Z5HuJ2mEG4frJaJLYSmi7PuWvciU0.jpg',4.8,'08:00-15:30',3),
(2,'Phi Phi Islands','Beaytiful tropical islands with clear water','https://www.trip-attractive.com/wp-content/uploads/2017/04/phi-phi-island-960x530.jpg',4.7,'All day',2),
(3,'Doi Inthanon','Highest mountain in Thailand with waterfalls','https://s.isanook.com/tr/0/ud/282/1412729/4-3_1.jpg?ip/crop/w670h402/q80/jpg',4.6,'05:30-18:00',1),
(4,'Yaowarat Road','Famous street food area in Bangkok','https://image-tc.galaxy.tf/wijpeg-4m5dshpuly1fenuvicn3nn496/chinatown_standard.jpg?crop=92%2C0%2C1416%2C1062',4.5,'17:00-0:00',6),
(5,'Ayutthaya Historical Park','Ancient Ruins and temples','https://static.thairath.co.th/media/FcvsRgKyX10OHanMl6mNNVzVGVPChFw6wMYUCzdyuts1LUtU5Lhw2klN0Q.jpg',4.6,'08:00-18:00',5),
(6,'Em En Ville','A stylish cafe on Phraeng Nakhon Road','https://media.readthecloud.co/wp-content/uploads/2023/08/29040422/im-en-ville-feature.webp',4.6,'09:00-21:00',4);
/*!40000 ALTER TABLE `rec_travel` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `style_travel`
--

DROP TABLE IF EXISTS `style_travel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `style_travel` (
  `style_id` int(11) NOT NULL AUTO_INCREMENT,
  `style_name` varchar(100) NOT NULL,
  PRIMARY KEY (`style_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `style_travel`
--

LOCK TABLES `style_travel` WRITE;
/*!40000 ALTER TABLE `style_travel` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `style_travel` VALUES
(1,'nature'),
(2,'beach'),
(3,'temple'),
(4,'cafe&food'),
(5,'culture'),
(6,'city');
/*!40000 ALTER TABLE `style_travel` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `transportation`
--

DROP TABLE IF EXISTS `transportation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `transportation` (
  `tran_id` int(11) NOT NULL AUTO_INCREMENT,
  `tran_name` varchar(100) NOT NULL,
  `tran_time` int(11) NOT NULL,
  `tran_cost` int(11) NOT NULL,
  `place_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`tran_id`),
  KEY `transportation_rec_travel_FK` (`place_id`),
  CONSTRAINT `transportation_rec_travel_FK` FOREIGN KEY (`place_id`) REFERENCES `rec_travel` (`place_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transportation`
--

LOCK TABLES `transportation` WRITE;
/*!40000 ALTER TABLE `transportation` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `transportation` VALUES
(1,'car',160,500,3),
(2,'bus',45,15,1),
(3,'moterbike',15,20,6),
(4,'train',90,20,5),
(5,'boat',30,14,6),
(6,'MRT',10,30,4),
(7,'taxi',30,150,1),
(8,'van',60,70,5),
(9,'ferry',120,400,2),
(10,'tour van',90,800,3),
(11,'speed boat',60,900,2),
(12,'taxi',20,120,4);
/*!40000 ALTER TABLE `transportation` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `user_travel`
--

DROP TABLE IF EXISTS `user_travel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_travel` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_travel`
--

LOCK TABLES `user_travel` WRITE;
/*!40000 ALTER TABLE `user_travel` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `user_travel` VALUES
('pui','eiei',1),
('nil','1234',2),
('aus','hahaha',3),
('kait','password',4);
/*!40000 ALTER TABLE `user_travel` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-03-26  2:44:55
