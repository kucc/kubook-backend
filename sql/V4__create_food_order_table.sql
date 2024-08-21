CREATE TABLE `food_order` (
          `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
          `food_id` BIGINT NOT NULL,
          `user_id` BIGINT NOT NULL,
          `quantity` INT NOT NULL,
          `created_at` TIMESTAMP NOT NULL DEFAULT NOW(),
          `updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
          `is_deleted` BOOLEAN NOT NULL DEFAULT FALSE
);