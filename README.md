IMDB Toplist Scrapy Project
===========================

A Python spider built on [Scrapy](http://scrapy.org). It scrapes and stores a list of top movies.

## Installation

Install Python, Python headers and static libs (required to install PIL), Scrapy, PIL and PyMySQL.

Create a database:

    CREATE DATABASE `imdb_toplist` CHARSET utf8 COLLATE utf8_general_ci;

    USE `imdb_toplist`;

    CREATE TABLE `movie` (
      `id` int(11) unsigned NOT NULL,
      `url` varchar(255) DEFAULT NULL,
      `title` varchar(255) NOT NULL DEFAULT '',
      `original_title` varchar(255) DEFAULT NULL,
      `description` varchar(511) DEFAULT NULL,
      `year` smallint(4) NOT NULL,
      `length` smallint(5) unsigned NOT NULL DEFAULT '0',
      `director` varchar(128) DEFAULT NULL,
      `image_small` varchar(255) DEFAULT NULL,
      `image_large` varchar(255) DEFAULT NULL,
      `rating` decimal(2,2) unsigned NOT NULL DEFAULT '0.00',
      `votes` int(11) unsigned NOT NULL DEFAULT '0',
      PRIMARY KEY (`id`),
      UNIQUE KEY `title_idx` (`title`),
      KEY `year_idx` (`year`),
      KEY `rating_idx` (`rating`),
      KEY `votes_idx` (`votes`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

    CREATE USER 'imdb'@'localhost' IDENTIFIED BY 'imdb123';
    GRANT ALL PRIVILEGES ON `imdb_toplist`.* TO 'imdb'@'localhost';
    FLUSH PRIVILEGES

Clone the project:

    git clone git://github.com/bkuberek/imdb_toplist.git

Run it:

    cd imdb_toplist
    scrapy crawl imdb_toplist

