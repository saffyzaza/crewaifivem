local isDead = false
local firstSpawn = true
local lastCoords = nil

-- Handle the initial player spawn
AddEventHandler('playerSpawned', function()
    if firstSpawn then
        TriggerServerEvent('respawnSystem:requestPlayerData')
        firstSpawn = false
    end
end)

-- Receive data from server and determine spawn location
RegisterNetEvent('respawnSystem:receivePlayerData')
AddEventHandler('respawnSystem:receivePlayerData', function(data)
    DoScreenFadeOut(500)
    while not IsScreenFadedOut() do Wait(0) end

    local ped = PlayerPedId()
    
    if data.is_new == 1 then
        -- First time players go to airport
        SetEntityCoords(ped, Config.AirportCoords.x, Config.AirportCoords.y, Config.AirportCoords.z, false, false, false, true)
        SetEntityHeading(ped, Config.AirportCoords.w)
        TriggerServerEvent('respawnSystem:setNewPlayerStatus')
    elseif data.death_x and data.death_y and data.death_z then
        -- Returning dead players or regular spawn at death location
        SetEntityCoords(ped, data.death_x, data.death_y, data.death_z, false, false, false, true)
        if data.death_h then SetEntityHeading(ped, data.death_h) end
    end

    Wait(1000)
    DoScreenFadeIn(1000)
end)

-- Main loop to track health and handle death
CreateThread(function()
    while true do
        local ped = PlayerPedId()
        local sleep = 500

        if IsEntityDead(ped) and not isDead then
            isDead = true
            sleep = 0
            
            local coords = GetEntityCoords(ped)
            local heading = GetEntityHeading(ped)
            lastCoords = { x = coords.x, y = coords.y, z = coords.z, h = heading }

            -- Notify server of death location
            TriggerServerEvent('respawnSystem:onPlayerKilled', lastCoords)

            -- Start respawn timer
            Wait(Config.RespawnDelay)
            TriggerEvent('respawnSystem:performRespawn')
        elseif not IsEntityDead(ped) then
            isDead = false
        end
        
        Wait(sleep)
    end
end)

-- Respawn logic
RegisterNetEvent('respawnSystem:performRespawn')
AddEventHandler('respawnSystem:performRespawn', function()
    if Config.EnableCinematicFade then
        DoScreenFadeOut(800)
        while not IsScreenFadedOut() do Wait(0) end
    end

    local ped = PlayerPedId()
    
    -- Native function to resurrect player
    NetworkResurrectPlayer(lastCoords.x, lastCoords.y, lastCoords.z, lastCoords.h, true, false)
    
    -- Clear tasks and set state
    ClearPedTasksImmediately(ped)
    SetEntityHealth(ped, 200)
    isDead = false

    if Config.EnableCinematicFade then
        Wait(500)
        DoScreenFadeIn(800)
    end
end)