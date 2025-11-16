-- Script: script-001.sql
-- Generado a partir de las clases en org.certManager.model
-- Crea la base de datos y las tablas necesarias en MariaDB / MySQL

CREATE DATABASE IF NOT EXISTS `cert_magnament` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `cert_magnament`;

-- Tabla de empresas (Company.nombre)
CREATE TABLE IF NOT EXISTS `companies` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `nombre` VARCHAR(255) NOT NULL,
  UNIQUE INDEX `ux_companies_nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de posiciones (Position.positionName)
CREATE TABLE IF NOT EXISTS `positions` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `position_name` VARCHAR(255) NOT NULL,
  UNIQUE INDEX `ux_positions_name` (`position_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de nombres de certificado (CertName.certName)
CREATE TABLE IF NOT EXISTS `cert_names` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `cert_name` VARCHAR(255) NOT NULL,
  UNIQUE INDEX `ux_cert_names_name` (`cert_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de empleados (Employee)
-- Mapeo recomendado:
--   employeeId -> employee_id (string, único)
--   employeeName -> employee_name
--   employeeSurname -> employee_surname
--   phoneNumber -> phone_number
--   isIncludedInMdp -> is_included_in_mdp (boolean)
--   company -> company_id (FK -> companies.id)
--   isActiveEmployee -> campos inline: is_active, checked_out_at
--   position -> position_id (FK -> positions.id)
CREATE TABLE IF NOT EXISTS `employees` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `employee_id` VARCHAR(100) NOT NULL,
  `employee_name` VARCHAR(255) NOT NULL,
  `employee_surname` VARCHAR(255),
  `phone_number` VARCHAR(50),
  `is_included_in_mdp` TINYINT(1) NOT NULL DEFAULT 0,
  `company_id` BIGINT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `checked_out_at` DATETIME NULL,
  `position_id` BIGINT  NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE INDEX `ux_employees_employee_id` (`employee_id`),
  INDEX `idx_employees_company_id` (`company_id`),
  INDEX `idx_employees_position_id` (`position_id`),
  CONSTRAINT `fk_employees_company` FOREIGN KEY (`company_id`) REFERENCES `companies`(`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_employees_position` FOREIGN KEY (`position_id`) REFERENCES `positions`(`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de vencimientos de certificados (CertExpiration)
-- Mapeo:
--   certExpirations es una lista en Employee -> tabla cert_expirations con FK a employees
--   certName -> cert_name_id (FK -> cert_names.id)
--   expirationDate -> expiration_date (DATE)
--   dateMade -> date_made (DATE)
CREATE TABLE IF NOT EXISTS `cert_expirations` (
  `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `employee_id` BIGINT NOT NULL,
  `cert_name_id` BIGINT NULL,
  `expiration_date` DATE NULL,
  `date_made` DATE NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_cert_expirations_employee_id` (`employee_id`),
  INDEX `idx_cert_expirations_cert_name_id` (`cert_name_id`),
  CONSTRAINT `fk_cert_expirations_employee` FOREIGN KEY (`employee_id`) REFERENCES `employees`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cert_expirations_cert_name` FOREIGN KEY (`cert_name_id`) REFERENCES `cert_names`(`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Ejemplos (opcional): insertar datos iniciales
-- INSERT INTO `companies` (`nombre`) VALUES ('ACME S.A.');
-- INSERT INTO `positions` (`position_name`) VALUES ('Developer');
-- INSERT INTO `cert_names` (`cert_name`) VALUES ('Certificación X');

-- Fin del script