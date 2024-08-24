CREATE TABLE `food` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `food_name` VARCHAR(255) NOT NULL,
          `food_type` VARCHAR(20) NOT NULL,
          `food_price` INT NOT NULL,
          `food_description` TEXT NOT NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
          `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);