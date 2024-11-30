CREATE TABLE `settings` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `start_date` DATETIME NOT NULL,
		      `end_date` DATETIME NOT NULL,
          `extend_days` TINYINT unsigned NOT NULL,
          `extend_max_count` TINYINT unsigned NOT NULL,
          `loan_days` TINYINT unsigned NOT NULL,
          `loan_max_book` TINYINT unsigned NOT NULL,
          `request_max_count` TINYINT unsigned NOT NULL,
          `request_max_price` TINYINT unsigned NOT NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);