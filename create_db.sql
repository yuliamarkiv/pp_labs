-- mysql -u root -p adservice < create_db.sql

CREATE TABLE IF NOT EXISTS `adservice`.`location` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`));


CREATE TABLE IF NOT EXISTS `adservice`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `locationId` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `user_location`
    FOREIGN KEY (`locationId`)
    REFERENCES `adservice`.`location` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


CREATE TABLE IF NOT EXISTS `adservice`.`ad` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `text` TEXT NULL,
  `price` FLOAT NOT NULL,
  `currency` VARCHAR(10) NOT NULL,
  `date` DATE NOT NULL,
  `locationId` INT NULL,
  `userId` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `ad_location`
    FOREIGN KEY (`locationId`)
    REFERENCES `adservice`.`location` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `ad_user`
    FOREIGN KEY (`userId`)
    REFERENCES `adservice`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
