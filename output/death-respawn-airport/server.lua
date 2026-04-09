local function getIdentifier(source)
    for _, v in pairs(GetPlayerIdentifiers(source)) do
        if string.find(v, 'license:') then
            return v
        end
    end
    return nil
end

-- Database Initialization
MySQL.ready(function()
    MySQL.query([[
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
    ]])
end)

-- Load player data on request
RegisterNetEvent('respawnSystem:requestPlayerData')
AddEventHandler('respawnSystem:requestPlayerData', function()
    local src = source
    local identifier = getIdentifier(src)

    if identifier then
        MySQL.single('SELECT * FROM player_spawns WHERE identifier = ?', {identifier}, function(result)
            if result then
                TriggerClientEvent('respawnSystem:receivePlayerData', src, result)
            else
                -- Create default entry for new user
                MySQL.insert('INSERT INTO player_spawns (identifier, is_new) VALUES (?, 1)', {identifier}, function(id)
                    TriggerClientEvent('respawnSystem:receivePlayerData', src, {is_new = 1})
                end)
            end
        end)
    end
end)

-- Save death location
RegisterNetEvent('respawnSystem:onPlayerKilled')
AddEventHandler('respawnSystem:onPlayerKilled', function(coords)
    local src = source
    local identifier = getIdentifier(src)

    if identifier then
        MySQL.update('UPDATE player_spawns SET death_x = ?, death_y = ?, death_z = ?, death_h = ?, is_dead = 1 WHERE identifier = ?', 
            {coords.x, coords.y, coords.z, coords.h, identifier})
        
        print(string.format("^2[Death Log]^7 Player %s died at: %s, %s, %s", GetPlayerName(src), coords.x, coords.y, coords.z))
    end
end)

-- Update new player status after first spawn
RegisterNetEvent('respawnSystem:setNewPlayerStatus')
AddEventHandler('respawnSystem:setNewPlayerStatus', function()
    local src = source
    local identifier = getIdentifier(src)

    if identifier then
        MySQL.update('UPDATE player_spawns SET is_new = 0 WHERE identifier = ?', {identifier})
    end
end)