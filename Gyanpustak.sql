-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: Gyanpustak
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.3

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
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrator` (
  `emp_id` int NOT NULL,
  `firstname` varchar(20) DEFAULT NULL,
  `lastname` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  `aadhaar` varchar(13) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  `phoneno` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrator`
--

LOCK TABLES `administrator` WRITE;
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
INSERT INTO `administrator` VALUES (4,'Neha','Singh','Female',50000.00,'123456789015','neha@gmail.com','admin123','Delhi','9876500004'),(5,'Karan','Patel','Male',52000.00,'123456789016','karan@gmail.com','admin123','Ahmedabad','9876500005'),(9,'Pardhiv','naidu','Male',30000.00,'547259628429','pardhiv@gmail.com','vizag','admin123','9876543218'),(10,'Prabhas','Moravineni','Male',30000.00,'547259628430','prabhas@gmail.com','Tirupati','admin123','9876543219');
/*!40000 ALTER TABLE `administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `author` (
  `author_id` int NOT NULL AUTO_INCREMENT,
  `author_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`author_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author`
--

LOCK TABLES `author` WRITE;
/*!40000 ALTER TABLE `author` DISABLE KEYS */;
INSERT INTO `author` VALUES (1,'Cormen'),(2,'Thomas H. Cormen'),(3,'Dennis Ritchie'),(4,'Bjarne Stroustrup'),(5,'Andrew Tanenbaum'),(6,'Herbert Schildt'),(7,'Robert Lafore'),(8,'E. Balagurusamy'),(9,'Billy wellman');
/*!40000 ALTER TABLE `author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_author`
--

DROP TABLE IF EXISTS `book_author`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_author` (
  `author_id` int NOT NULL,
  `isbn` varchar(15) NOT NULL,
  PRIMARY KEY (`isbn`,`author_id`),
  KEY `bka_author` (`author_id`),
  CONSTRAINT `bk_auth` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`),
  CONSTRAINT `bka_author` FOREIGN KEY (`author_id`) REFERENCES `author` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_author`
--

LOCK TABLES `book_author` WRITE;
/*!40000 ALTER TABLE `book_author` DISABLE KEYS */;
INSERT INTO `book_author` VALUES (1,'ISBN001'),(2,'ISBN001'),(2,'ISBN004'),(3,'ISBN002'),(4,'ISBN004'),(5,'ISBN003'),(5,'ISBN007'),(6,'ISBN005'),(7,'ISBN006'),(8,'ISBN006'),(9,'ISBN009');
/*!40000 ALTER TABLE `book_author` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_course`
--

DROP TABLE IF EXISTS `book_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_course` (
  `isbn` varchar(15) NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`isbn`,`course_id`),
  KEY `fk3` (`course_id`),
  CONSTRAINT `fk2` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`),
  CONSTRAINT `fk3` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_course`
--

LOCK TABLES `book_course` WRITE;
/*!40000 ALTER TABLE `book_course` DISABLE KEYS */;
INSERT INTO `book_course` VALUES ('ISBN002',1),('ISBN001',2),('ISBN006',2),('ISBN001',3),('ISBN004',3),('ISBN005',3),('ISBN003',4),('ISBN007',4),('ISBN006',5),('ISBN007',6);
/*!40000 ALTER TABLE `book_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_keyword`
--

DROP TABLE IF EXISTS `book_keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_keyword` (
  `isbn` varchar(15) NOT NULL,
  `keyword_id` int NOT NULL,
  PRIMARY KEY (`isbn`,`keyword_id`),
  KEY `fk1` (`keyword_id`),
  CONSTRAINT `book_keyword_ibfk_1` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`),
  CONSTRAINT `fk1` FOREIGN KEY (`keyword_id`) REFERENCES `keyword` (`keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_keyword`
--

LOCK TABLES `book_keyword` WRITE;
/*!40000 ALTER TABLE `book_keyword` DISABLE KEYS */;
INSERT INTO `book_keyword` VALUES ('ISBN001',1),('ISBN002',2),('ISBN004',2),('ISBN004',3),('ISBN005',4),('ISBN001',5),('ISBN006',5),('ISBN003',6),('ISBN007',6),('ISBN007',7);
/*!40000 ALTER TABLE `book_keyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_subcategory`
--

DROP TABLE IF EXISTS `book_subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_subcategory` (
  `subcategory_id` int NOT NULL,
  `isbn` varchar(15) NOT NULL,
  PRIMARY KEY (`isbn`,`subcategory_id`),
  KEY `book_subcategory_ibfk_2` (`subcategory_id`),
  CONSTRAINT `book_subcategory_ibfk_1` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`),
  CONSTRAINT `book_subcategory_ibfk_2` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategory` (`subcategory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_subcategory`
--

LOCK TABLES `book_subcategory` WRITE;
/*!40000 ALTER TABLE `book_subcategory` DISABLE KEYS */;
INSERT INTO `book_subcategory` VALUES (1,'ISBN001'),(2,'ISBN002'),(2,'ISBN004'),(2,'ISBN005'),(3,'ISBN006'),(4,'ISBN003'),(5,'ISBN007'),(8,'ISBN009');
/*!40000 ALTER TABLE `book_subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `isbn` varchar(15) NOT NULL,
  `type` varchar(10) DEFAULT NULL,
  `options` varchar(10) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `title` varchar(40) DEFAULT NULL,
  `publisher` varchar(50) DEFAULT NULL,
  `publication_date` date DEFAULT NULL,
  `edition_no` int DEFAULT NULL,
  `language` varchar(30) DEFAULT NULL,
  `format` varchar(20) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`isbn`),
  KEY `fk` (`category_id`),
  CONSTRAINT `fk` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`),
  CONSTRAINT `books_chk_1` CHECK ((`type` in (_utf8mb4'new',_utf8mb4'used'))),
  CONSTRAINT `books_chk_2` CHECK ((`options` in (_utf8mb4'rent',_utf8mb4'buy'))),
  CONSTRAINT `books_chk_3` CHECK ((`format` in (_utf8mb4'electronic',_utf8mb4'softcover',_utf8mb4'hardcover')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES ('ISBN001','new','buy',599.99,10,'Algorithms','MIT Press','2009-07-31',3,'English','hardcover',1),('ISBN002','new','buy',499.50,8,'C Programming','Prentice Hall','1988-04-01',2,'English','softcover',1),('ISBN003','used','rent',650.00,5,'Operating Systems','Pearson','2001-01-15',2,'English','hardcover',1),('ISBN004','new','buy',700.00,7,'C++ Programming','Addison-Wesley','2013-05-19',4,'English','hardcover',1),('ISBN005','new','buy',450.75,6,'Java Programming','McGraw Hill','2010-06-10',5,'English','softcover',1),('ISBN006','new','rent',550.25,9,'Data Structures','Oxford Press','2012-09-21',3,'English','electronic',1),('ISBN007','used','buy',400.00,4,'Computer Networks','Pearson','2003-03-10',4,'English','hardcover',1),('ISBN008','New','Buy',750.00,3,'Elementary Mechanical Engineering','Namya press','2024-06-30',1,'English','Hardcover',2),('ISBN009','New','Rent',3000.00,4,'History of india','Mc grawhill','2023-12-13',2,'English','Softcover',7);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `date_created` date DEFAULT NULL,
  `date_last_updated` date DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`cart_id`),
  KEY `fk_cart_st` (`created_by`),
  CONSTRAINT `fk_cart_st` FOREIGN KEY (`created_by`) REFERENCES `student` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (7,'2026-04-17','2026-04-17',1),(8,'2026-04-20','2026-04-20',7);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_book`
--

DROP TABLE IF EXISTS `cart_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_book` (
  `cart_id` int NOT NULL,
  `isbn` varchar(15) NOT NULL,
  PRIMARY KEY (`cart_id`,`isbn`),
  KEY `fk_isbn` (`isbn`),
  CONSTRAINT `fk_cart` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`),
  CONSTRAINT `fk_isbn` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_book`
--

LOCK TABLES `cart_book` WRITE;
/*!40000 ALTER TABLE `cart_book` DISABLE KEYS */;
INSERT INTO `cart_book` VALUES (7,'ISBN001'),(7,'ISBN007'),(7,'ISBN008');
/*!40000 ALTER TABLE `cart_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `category_id` int NOT NULL,
  `category_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Computer Science'),(2,'Mechanical Engineering'),(3,'Electrical Engineering'),(4,'Civil Engineering'),(5,'Mathematics'),(6,'Physics'),(7,'History');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `course_id` int NOT NULL,
  `course_name` varchar(30) DEFAULT NULL,
  `cur_year` int DEFAULT NULL,
  `cur_sem` int DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Programming in C',1,1),(2,'Data Structures',1,2),(3,'Object Oriented Programming',2,1),(4,'Operating Systems',2,2),(5,'Database Management Systems',3,1),(6,'Computer Networks',3,2),(7,'Software Engineering',4,1);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_department`
--

DROP TABLE IF EXISTS `course_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_department` (
  `course_id` int NOT NULL,
  `dept_id` int NOT NULL,
  PRIMARY KEY (`course_id`,`dept_id`),
  KEY `fk_cour_dept2` (`dept_id`),
  CONSTRAINT `course_department_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  CONSTRAINT `course_department_ibfk_2` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`),
  CONSTRAINT `fk_cour_dept1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  CONSTRAINT `fk_cour_dept2` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_department`
--

LOCK TABLES `course_department` WRITE;
/*!40000 ALTER TABLE `course_department` DISABLE KEYS */;
INSERT INTO `course_department` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(4,3),(6,3);
/*!40000 ALTER TABLE `course_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_instructor`
--

DROP TABLE IF EXISTS `course_instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_instructor` (
  `course_id` int NOT NULL,
  `instr_id` int NOT NULL,
  PRIMARY KEY (`course_id`,`instr_id`),
  KEY `fk_cour_instr2` (`instr_id`),
  CONSTRAINT `course_instructor_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  CONSTRAINT `course_instructor_ibfk_2` FOREIGN KEY (`instr_id`) REFERENCES `instructor` (`instr_id`),
  CONSTRAINT `fk_cour_instr1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  CONSTRAINT `fk_cour_instr2` FOREIGN KEY (`instr_id`) REFERENCES `instructor` (`instr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_instructor`
--

LOCK TABLES `course_instructor` WRITE;
/*!40000 ALTER TABLE `course_instructor` DISABLE KEYS */;
INSERT INTO `course_instructor` VALUES (1,1),(2,1),(5,2),(4,3),(6,3),(7,4),(2,6),(3,6),(5,6);
/*!40000 ALTER TABLE `course_instructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_support`
--

DROP TABLE IF EXISTS `customer_support`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_support` (
  `emp_id` int NOT NULL,
  `firstname` varchar(20) DEFAULT NULL,
  `lastname` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  `aadhaar` varchar(13) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `phoneno` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_support`
--

LOCK TABLES `customer_support` WRITE;
/*!40000 ALTER TABLE `customer_support` DISABLE KEYS */;
INSERT INTO `customer_support` VALUES (1,'Ravi','Kumar','Male',30000.00,'123456789012','ravi@gmail.com','support123','Delhi','9876500001'),(2,'Pooja','Sharma','Female',32000.00,'123456789013','pooja@gmail.com','support123','Mumbai','9876500002'),(3,'Amit','Verma','Male',31000.00,'123456789014','amit@gmail.com','support123','Bangalore','9876500003');
/*!40000 ALTER TABLE `customer_support` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `dept_id` int NOT NULL,
  `university_id` int NOT NULL,
  `dept_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`dept_id`,`university_id`),
  KEY `fk_dept` (`university_id`),
  CONSTRAINT `fk_dept` FOREIGN KEY (`university_id`) REFERENCES `university` (`university_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,1,'Computer Science'),(2,1,'Mechanical Engineering'),(3,2,'Electrical Engineering'),(4,3,'Civil Engineering'),(5,4,'Mathematics'),(6,5,'Physics');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emp_ticket_his`
--

DROP TABLE IF EXISTS `emp_ticket_his`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emp_ticket_his` (
  `change_id` int NOT NULL,
  `emp_id` int DEFAULT NULL,
  PRIMARY KEY (`change_id`),
  KEY `fk4` (`emp_id`),
  CONSTRAINT `fk4` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emp_ticket_his`
--

LOCK TABLES `emp_ticket_his` WRITE;
/*!40000 ALTER TABLE `emp_ticket_his` DISABLE KEYS */;
/*!40000 ALTER TABLE `emp_ticket_his` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `emp_id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(20) DEFAULT NULL,
  `lastname` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  `aadhaar` varchar(15) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phoneno` varchar(11) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`emp_id`),
  CONSTRAINT `chk_role` CHECK ((`role` in (_utf8mb4'customer_support',_utf8mb4'administrator',_utf8mb4'super_admin')))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Ravi','Kumar','Male',30000.00,'123456789012','ravi@gmail.com','9876500001','customer_support','support123'),(2,'Pooja','Sharma','Female',32000.00,'123456789013','pooja@gmail.com','9876500002','customer_support','support123'),(3,'Amit','Verma','Male',31000.00,'123456789014','amit@gmail.com','9876500003','customer_support','support123'),(4,'Neha','Singh','Female',50000.00,'123456789015','neha@gmail.com','9876500004','administrator','admin123'),(5,'Karan','Patel','Male',52000.00,'123456789016','karan@gmail.com','9876500005','administrator','admin123'),(6,'Lokesh','Bellamkonda','Male',80000.00,'123456789017','lokesh@gmail.com','9876500006','super_admin','super123'),(9,'Pardhiv','naidu','Male',30000.00,'547259628429','pardhiv@gmail.com','9876543218','administrator','admin123'),(10,'Prabhas','Moravineni','Male',30000.00,'547259628430','prabhas@gmail.com','9876543219','administrator','admin123');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor` (
  `instr_id` int NOT NULL,
  `firstname` varchar(30) DEFAULT NULL,
  `lastname` varchar(30) DEFAULT NULL,
  `university_id` int DEFAULT NULL,
  `dept_id` int DEFAULT NULL,
  PRIMARY KEY (`instr_id`),
  KEY `university_id` (`university_id`),
  KEY `dept_id` (`dept_id`),
  CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`university_id`) REFERENCES `university` (`university_id`),
  CONSTRAINT `instructor_ibfk_2` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor`
--

LOCK TABLES `instructor` WRITE;
/*!40000 ALTER TABLE `instructor` DISABLE KEYS */;
INSERT INTO `instructor` VALUES (1,'Anil','Kumar',1,1),(2,'Sunita','Sharma',2,2),(3,'Rajesh','Verma',3,3),(4,'Meera','Iyer',4,4),(5,'Vikas','Patel',5,5),(6,'Neha','Rao',1,1);
/*!40000 ALTER TABLE `instructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keyword`
--

DROP TABLE IF EXISTS `keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keyword` (
  `keyword_id` int NOT NULL,
  `keyword` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keyword`
--

LOCK TABLES `keyword` WRITE;
/*!40000 ALTER TABLE `keyword` DISABLE KEYS */;
INSERT INTO `keyword` VALUES (1,'Algorithms'),(2,'C Programming'),(3,'C++'),(4,'Java'),(5,'Data Structures'),(6,'Operating Systems'),(7,'Computer Networks');
/*!40000 ALTER TABLE `keyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `orders_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `date_fulfilled` date DEFAULT NULL,
  `shipping_type` varchar(30) DEFAULT NULL,
  `credit_card_number` varchar(20) DEFAULT NULL,
  `credit_card_expiry_date` varchar(20) DEFAULT NULL,
  `credit_card_holder_name` varchar(40) DEFAULT NULL,
  `order_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`orders_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`),
  CONSTRAINT `orders_chk_1` CHECK ((`shipping_type` in (_utf8mb4'standard',_utf8mb4'2-day',_utf8mb4'1-day'))),
  CONSTRAINT `orders_chk_2` CHECK ((`order_status` in (_utf8mb4'new',_utf8mb4'processed',_utf8mb4'awaiting_shipping',_utf8mb4'shipped',_utf8mb4'cancelled',_utf8mb4'order_cancellation')))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,'2026-04-20',NULL,'standard','1234 5678 9101 2131','08/26','Lokesh Bellamkonda','cancelled'),(2,1,'2026-04-21',NULL,'standard','','','','cancelled'),(3,1,'2026-04-21',NULL,'standard','','','','cancelled');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_book`
--

DROP TABLE IF EXISTS `orders_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_book` (
  `orders_id` int NOT NULL,
  `isbn` varchar(15) NOT NULL,
  PRIMARY KEY (`orders_id`,`isbn`),
  KEY `fk_ord_book2` (`isbn`),
  CONSTRAINT `fk_ord_book1` FOREIGN KEY (`orders_id`) REFERENCES `orders` (`orders_id`),
  CONSTRAINT `fk_ord_book2` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_book`
--

LOCK TABLES `orders_book` WRITE;
/*!40000 ALTER TABLE `orders_book` DISABLE KEYS */;
INSERT INTO `orders_book` VALUES (1,'ISBN001'),(1,'ISBN002'),(2,'ISBN002'),(2,'ISBN003'),(3,'ISBN006'),(3,'ISBN008');
/*!40000 ALTER TABLE `orders_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `isbn` varchar(15) DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  KEY `fk_rev1` (`isbn`),
  KEY `fk_rev2` (`student_id`),
  CONSTRAINT `fk_rev1` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`),
  CONSTRAINT `fk_rev2` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`),
  CONSTRAINT `review_chk_1` CHECK (((`rating` >= 1) and (`rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,'ISBN001',1,4,'');
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `email` varchar(50) NOT NULL,
  `firstname` varchar(20) DEFAULT NULL,
  `lastname` varchar(20) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `phoneno` varchar(11) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `university_id` int DEFAULT NULL,
  `dept_id` int DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `curyear` int DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  `student_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `email` (`email`),
  KEY `st_univer` (`university_id`),
  KEY `st_dept` (`dept_id`),
  CONSTRAINT `st_dept` FOREIGN KEY (`dept_id`) REFERENCES `department` (`dept_id`),
  CONSTRAINT `st_univer` FOREIGN KEY (`university_id`) REFERENCES `university` (`university_id`),
  CONSTRAINT `st_status` CHECK ((`status` in (_utf8mb4'graduate',_utf8mb4'undergraduate')))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('rahul@gmail.com','Rahul','Sharma','Delhi','9876543201','2002-05-10',1,1,'graduate',1,'pass123',1),('sneha@gmail.com','Sneha','Reddy','Hyderabad','9876543202','2001-08-15',2,2,'undergraduate',2,'pass123',2),('arjun@gmail.com','Arjun','Verma','Mumbai','9876543203','2000-12-20',3,3,'graduate',3,'pass123',3),('priya@gmail.com','Priya','Nair','Chennai','9876543204','2002-03-18',4,4,'graduate',1,'pass123',4),('karan@gmail.com','Karan','Patel','Ahmedabad','9876543205','2001-07-25',5,5,'undergraduate',2,'pass123',5),('deepesh@gmail.com','Deepesh','varanasi','srikakulam','9876543220','2006-02-02',3,1,'undergraduate',3,'pass123',6),('hemanth@gmail.com','Hemanth','Molabanti','Ongole','9876543221','2006-10-19',3,4,'undergraduate',3,'pass123',7);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcategory`
--

DROP TABLE IF EXISTS `subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcategory` (
  `subcategory_id` int NOT NULL AUTO_INCREMENT,
  `subcategory_name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`subcategory_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategory`
--

LOCK TABLES `subcategory` WRITE;
/*!40000 ALTER TABLE `subcategory` DISABLE KEYS */;
INSERT INTO `subcategory` VALUES (1,'Algorithms'),(2,'Programming'),(3,'Data Structures'),(4,'Operating Systems'),(5,'Networking'),(6,'Databases'),(7,'Engineering Fundamentals'),(8,'General Knowledge');
/*!40000 ALTER TABLE `subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_history`
--

DROP TABLE IF EXISTS `ticket_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_history` (
  `change_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int DEFAULT NULL,
  `change_date` date DEFAULT NULL,
  PRIMARY KEY (`change_id`),
  KEY `ticket_history_ibfk_1` (`ticket_id`),
  CONSTRAINT `ticket_history_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `trouble_ticket` (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_history`
--

LOCK TABLES `ticket_history` WRITE;
/*!40000 ALTER TABLE `ticket_history` DISABLE KEYS */;
INSERT INTO `ticket_history` VALUES (1,1,'2026-04-16'),(2,2,'2026-04-16'),(3,3,'2026-04-17');
/*!40000 ALTER TABLE `ticket_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trouble_ticket`
--

DROP TABLE IF EXISTS `trouble_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trouble_ticket` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `date_logged` date DEFAULT NULL,
  `createdby` varchar(30) DEFAULT NULL,
  `title` varchar(20) DEFAULT NULL,
  `problem_description` varchar(100) DEFAULT NULL,
  `solution_description` varchar(100) DEFAULT NULL,
  `completion_date` date DEFAULT NULL,
  `emp_id` int DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  `support_id` int DEFAULT NULL,
  PRIMARY KEY (`ticket_id`),
  KEY `emp_id` (`emp_id`),
  KEY `fk_student` (`student_id`),
  KEY `fk_support` (`support_id`),
  CONSTRAINT `fk_student` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`),
  CONSTRAINT `fk_support` FOREIGN KEY (`support_id`) REFERENCES `customer_support` (`emp_id`),
  CONSTRAINT `trouble_ticket_ibfk_1` FOREIGN KEY (`emp_id`) REFERENCES `administrator` (`emp_id`),
  CONSTRAINT `trouble_ticket_chk_2` CHECK ((`createdby` in (_utf8mb4'customersupport',_utf8mb4'student'))),
  CONSTRAINT `trouble_ticket_chk_3` CHECK ((`status` in (_utf8mb4'New',_utf8mb4'Assigned',_utf8mb4'In-process',_utf8mb4'Completed')))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trouble_ticket`
--

LOCK TABLES `trouble_ticket` WRITE;
/*!40000 ALTER TABLE `trouble_ticket` DISABLE KEYS */;
INSERT INTO `trouble_ticket` VALUES (1,'2026-04-16','customersupport','ui fault','none',NULL,NULL,5,'In-process',NULL,1),(2,'2026-04-16','customersupport','ui fault','none','s','2026-04-16',5,'Completed',NULL,1),(3,'2026-04-17','student','testing','testing',NULL,NULL,NULL,'New',1,NULL),(4,'2026-04-21','student','Cancel Order #1','Student requested cancellation for Order ID 1',NULL,NULL,9,'Assigned',1,NULL),(5,'2026-04-21','student','Cancel Order #1','Student requested cancellation for Order ID 1','gvtv','2026-04-21',4,'Completed',1,NULL),(6,'2026-04-21','student','Cancel Order #1','Student requested cancellation for Order ID 1',NULL,NULL,4,'In-process',1,NULL),(7,'2026-04-21','student','Cancel Order #1','Student requested cancellation for Order ID 1',NULL,NULL,9,'Assigned',1,NULL),(8,'2026-04-21','student','Cancel Order #1','Student requested cancellation for Order ID 1',NULL,NULL,5,'Assigned',1,NULL),(9,'2026-04-21','student','Cancel Order #1','Student requested cancellation for Order ID 1',NULL,NULL,NULL,'New',1,NULL);
/*!40000 ALTER TABLE `trouble_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `university`
--

DROP TABLE IF EXISTS `university`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `university` (
  `university_id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `rep_first_name` varchar(20) DEFAULT NULL,
  `rep_last_name` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phoneno` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`university_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `university`
--

LOCK TABLES `university` WRITE;
/*!40000 ALTER TABLE `university` DISABLE KEYS */;
INSERT INTO `university` VALUES (1,'IIT Delhi','Delhi','Amit','Sharma','amit@iitd.ac.in','9876543210'),(2,'IIT Bombay','Mumbai','Ravi','Patel','ravi@iitb.ac.in','9876543211'),(3,'IIT Madras','Chennai','Suresh','Iyer','suresh@iitm.ac.in','9876543212'),(4,'IISc Bangalore','Bangalore','Meena','Rao','meena@iisc.ac.in','9876543213'),(5,'Delhi University','Delhi','Anjali','Verma','anjali@du.ac.in','9876543214'),(6,'IIT Bhubaneswar','Bhubaneswar','Sachin','Pandole','sachin@iitbbs.ac.in','9876543215');
/*!40000 ALTER TABLE `university` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-21 12:34:12
