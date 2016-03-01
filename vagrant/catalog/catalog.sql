DROP DATABASE IF EXISTS catalog;

CREATE DATABASE catalog;

\c catalog;

CREATE TABLE users (
	id serial UNIQUE NOT NULL,
	social_id varchar(64) UNIQUE,
	name varchar(20) NOT NULL,
	username varchar(30) UNIQUE NOT NULL,
	salt varchar(50),
	pass varchar(192)
);

Create TABLE categories (
	id serial UNIQUE NOT NULL,
	name varchar(50) UNIQUE
);

INSERT INTO categories (name) VALUES ('hockey');
INSERT INTO categories (name) VALUES ('snowboarding');

CREATE TABLE items (
	id serial UNIQUE NOT NULL,
	creator_id int references users(id),
	category_id int references categories(id),
	name varchar(100) NOT NULL,
	description text NOT NULL
);

INSERT INTO items (category_id, name, description) 
	VALUES ((SELECT id from categories WHERE name = 'hockey'), 
	'puck', 'A disk played and used to score a point by hitting it in the goal');

INSERT INTO items (category_id, name, description) 
	VALUES ((SELECT id from categories WHERE name = 'snowboarding'), 
	'goggles', 'Used to protect eyes from snow, sun, and other events on the field');

INSERT INTO items (category_id, name, description) 
	VALUES ((SELECT id from categories WHERE name = 'snowboarding'), 
	'snowboard', 'Primary equipment used to slide down the snow hill');