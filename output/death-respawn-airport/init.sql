CREATE TABLE IF NOT EXISTS `player_spawns` (
    `identifier` VARCHAR(60) NOT NULL,
    `is_new` TINYINT(1) DEFAULT 1,
    `death_x` FLOAT DEFAULT NULL,
    `death_y` FLOAT DEFAULT NULL,
    `death_z` FLOAT DEFAULT NULL,
    `death_h` FLOAT DEFAULT NULL,
    `is_dead` TINYINT(1) DEFAULT 0,
    PRIMARY KEY (`identifier`)
);