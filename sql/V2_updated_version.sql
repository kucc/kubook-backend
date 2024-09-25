CREATE TABLE `admin` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `user_id` BIGINT NOT NULL,
          `admin_status` TINYINT NOT NULL,
          `expiration_date` DATE NOT NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE `requested_book` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `user_id` BIGINT NOT NULL,
          `book_title` VARCHAR(255) NOT NULL,
          `publication_year` YEAR NULL,
          `reject_reason` VARCHAR(20) NULL,
          `request_link` VARCHAR(255) NOT NULL,
          `reason` TEXT NOT NULL,
          `requested_at` TIMESTAMP NOT NULL,
          `processing_status` TINYINT NOT NULL DEFAULT 0,
          `processed_at` TIMESTAMP NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE `loan` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `book_id` BIGINT NOT NULL,
          `user_id` BIGINT NOT NULL,
          `loan_date` DATE NOT NULL,
          `due_date` DATE NOT NULL,
          `extend_status` TINYINT NOT NULL DEFAULT 0,
          `return_status` TINYINT NOT NULL DEFAULT 0,
          `return_date` DATE NULL,
          `overdue_days` INT NOT NULL DEFAULT 0,
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE `book_review` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `user_id` BIGINT NOT NULL,
          `book_info_id` BIGINT NOT NULL,
          `review_content` TEXT NOT NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE `book_info` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `book_title` VARCHAR(255) NOT NULL,
          `code` VARCHAR(20) NOT NULL,
          `category_name` VARCHAR(50) NOT NULL,
          `subtitle` VARCHAR(255) NULL,
          `author` VARCHAR(100) NOT NULL,
          `publisher` VARCHAR(45) NOT NULL,
          `publication_year` YEAR NOT NULL,
          `image_url` VARCHAR(255) NULL,
          `version` VARCHAR(45) NULL,
          `major` BOOLEAN NULL DEFAULT FALSE,
          `language` VARCHAR(20) NOT NULL DEFAULT 'KOREAN',
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE `user` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `auth_id` VARCHAR(255) NOT NULL,
          `auth_type` VARCHAR(20) NOT NULL DEFAULT 'FIREBASE',
          `email` VARCHAR(100) NOT NULL,
          `user_name` VARCHAR(45) NOT NULL,
          `github_id` varchar(100) DEFAULT NULL,
          `instagram_id` varchar(100) DEFAULT NULL,
          `is_active` VARCHAR(20) NOT NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE `book` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `book_info_id` BIGINT NOT NULL,
          `book_status` TINYINT NOT NULL DEFAULT 1,
          `note` VARCHAR(255) NULL DEFAULT NULL,
          `donor_name` VARCHAR(20) NULL DEFAULT NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE `notice` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `admin_id` BIGINT NOT NULL,
          `user_id` INT NOT NULL,
          `title` VARCHAR(255) NOT NULL,
          `content` TEXT NOT NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);