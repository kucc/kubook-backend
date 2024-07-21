CREATE TABLE "user" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"auth_id" VARCHAR(50) UNIQUE NOT NULL,
	"user_name" VARCHAR(45) NOT NULL DEFAULT NULL,
	"is_active" BOOLEAN NOT NULL DEFAULT TRUE,
	"email" VARCHAR(100) UNIQUE NOT NULL,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "requested_book" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"user_id" INT NOT NULL,
	"book_title" VARCHAR(255) NOT NULL,
	"publication_year" YEAR NULL,
	"reject_reason" TEXT NULL,
	"request_link" VARCHAR(100) NOT NULL,
	"reason" TEXT NOT NULL,
	"processing_status" TINYINT NOT NULL DEFAULT 0,
	"request_date" DATE NOT NULL,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "admin" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"user_id" INT NOT NULL,
	"admin_status" BOOLEAN NOT NULL,
	"expiration_date" DATE NULL,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "notice" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"admin_id" INT NOT NULL,
	"user_id" INT NULL,
	"title" VARCHAR(255) NOT NULL,
	"notice_content" TEXT NOT NULL,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "book_category" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"code" VARCHAR(5) NOT NULL,
	"name" VARCHAR(50) NOT NULL,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "book_info" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"title" VARCHAR(255) NOT NULL,
	"subtitle" VARCHAR(255) NULL,
	"author" VARCHAR(100) NOT NULL,
	"publisher" VARCHAR(45) NOT NULL,
	"publication_year" YEAR NOT NULL,
	"image_url" VARCHAR(255) NULL,
	"category_id" INT NOT NULL,
	"version" VARCHAR(45) NULL,
	"major" BOOLEAN NULL DEFAULT FALSE,
	"language" BOOLEAN NOT NULL DEFAULT TRUE,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "book_review" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"user_id" INT NOT NULL,
	"book_info_id" INT NOT NULL,
	"review_content" TEXT NOT NULL,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "book" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"book_info_id" INT NOT NULL,
	"book_status" TINYINT NOT NULL DEFAULT 0,
	"note" VARCHAR(255) NULL DEFAULT NULL,
	"donor_name" VARCHAR(255) NULL DEFAULT NULL,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "reservation" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"book_id" INT NOT NULL,
	"user_id" INT NOT NULL,
	"reservation_date" DATE NOT NULL,
	"reservation_status" TINYINT NOT NULL DEFAULT 0,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "loan" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"book_id" INT NOT NULL,
	"user_id" INT NOT NULL,
	"loan_date" DATE NOT NULL,
	"due_date" DATE NOT NULL,
	"extend_status" BOOLEAN NOT NULL DEFAULT FALSE,
	"return_status" BOOLEAN NOT NULL DEFAULT FALSE,
	"return_date" DATE NULL,
	"overdue_days" INT NOT NULL DEFAULT 0,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE "library_setting" (
	"id" INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	"name" VARCHAR(50) NOT NULL,
	"value" VARCHAR(50) NOT NULL,
	"data_type" VARCHAR(50) NOT NULL,
	"description" TEXT NULL,
	"created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"updated_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	"is_valid" BOOLEAN NOT NULL DEFAULT TRUE
);