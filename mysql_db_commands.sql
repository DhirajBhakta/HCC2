
CREATE TABLE `StudentUser` (
  `rollno` char(7) NOT NULL,
  `name` varchar(64) NOT NULL,
  `email` varchar(64) DEFAULT NULL,
  `passwordhash` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`rollno`)
);




CREATE TABLE `Student` (
  `rollno` varchar(8) NOT NULL,
  `name` varchar(64) NOT NULL,
  `DOB` date DEFAULT NULL,
  `phno` char(10) DEFAULT NULL,
  `loc_addr` varchar(255) DEFAULT NULL,
  `perm_addr` varchar(255) DEFAULT NULL,
  `course_id` int(11) NOT NULL,
  `allergic_to` varchar(255) DEFAULT NULL,
  `guardian_phno` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`rollno`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `Student_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `Course` (`course_id`)
) ;




CREATE TABLE `Course` (
  `course_id` int(11) NOT NULL,
  `course_name` varchar(16) NOT NULL,
  PRIMARY KEY (`course_id`)
) ;