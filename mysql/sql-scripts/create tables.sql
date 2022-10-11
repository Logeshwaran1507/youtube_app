use youtube;

CREATE TABLE user (
  user INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(300) NOT NULL,
  password VARCHAR(300) NOT NULL,
  PRIMARY KEY (user),
  UNIQUE INDEX username_UNIQUE (username ASC) VISIBLE);

CREATE TABLE groups_keywords (
  user_id INT NOT NULL,
  group_name VARCHAR(300) NOT NULL,
  keyword VARCHAR(300) NOT NULL,
  PRIMARY KEY (user_id, group_name, keyword));

CREATE TABLE default_values (
  userId INT NOT NULL,
  group_name VARCHAR(300) NOT NULL,
  keyword VARCHAR(300) NOT NULL,
  PRIMARY KEY (userId));

CREATE TABLE bookmark (
  user_id INT NOT NULL,
  title VARCHAR(300) NOT NULL,
  url VARCHAR(300) NOT NULL,
  PRIMARY KEY (user_id, title, url));