local isTeleporting = false

-- Utility function to show help notification
local function showHelpNotification(text)
    BeginTextCommandDisplayHelp("STRING")
    AddTextComponentShortString(text)
    EndTextCommandDisplayHelp(0, false, true, -1)
end

-- Utility function to draw 3D text (alternative to help notification)
local function draw3DText(coords, text)
    local onScreen, _x, _y = World3dToScreen2d(coords.x, coords.y, coords.z)
    if onScreen then
        SetTextScale(0.35, 0.35)
        SetTextFont(4)
        SetTextProportional(1)
        SetTextColour(255, 255, 255, 215)
        SetTextEntry("STRING")
        SetTextCentre(1)
        AddTextComponentString(text)
        DrawText(_x, _y)
        local factor = (string.len(text)) / 370
        DrawRect(_x, _y + 0.0125, 0.015 + factor, 0.03, 41, 11, 41, 68)
    end
end

-- Core teleport logic
local function performTeleport(targetCoords)
    if isTeleporting then return end
    isTeleporting = true

    local ped = PlayerPedId()
    local targetEntity = ped
    
    if Config.VehicleTeleportEnabled and IsPedInAnyVehicle(ped, false) then
        targetEntity = GetVehiclePedIsIn(ped, false)
        if GetPedInVehicleSeat(targetEntity, -1) ~= ped then
            isTeleporting = false
            return -- Only driver can teleport the vehicle
        end
    end

    if Config.UseCinematicTransition then
        DoScreenFadeOut(Config.FadeDuration)
        while not IsScreenFadedOut() do Wait(0) end
    end

    -- Perform physical teleport
    RequestCollisionAtCoord(targetCoords.x, targetCoords.y, targetCoords.z)
    SetEntityCoords(targetEntity, targetCoords.x, targetCoords.y, targetCoords.z, false, false, false, true)
    SetEntityHeading(targetEntity, targetCoords.w)
    
    -- Ensure entity stops moving
    SetEntityVelocity(targetEntity, 0.0, 0.0, 0.0)

    Wait(500) -- Allow map to load

    if Config.UseCinematicTransition then
        DoScreenFadeIn(Config.FadeDuration)
    end

    isTeleporting = false
end

-- Server Response Handler
RegisterNetEvent('tp_system:performTeleport')
AddEventHandler('tp_system:performTeleport', function(targetCoords)
    performTeleport(targetCoords)
end)

-- Main Loop
Citizen.CreateThread(function()
    while true {
        local sleep = 1000
        local ped = PlayerPedId()
        local pCoords = GetEntityCoords(ped)

        for id, data in pairs(Config.TeleportPairs) do
            -- Check Point 1
            local dist1 = #(pCoords - vector3(data.pos1.x, data.pos1.y, data.pos1.z))
            if dist1 < Config.DrawDistance then
                sleep = 0
                DrawMarker(Config.MarkerType, data.pos1.x, data.pos1.y, data.pos1.z - 0.95, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, Config.MarkerColor.r, Config.MarkerColor.g, Config.MarkerColor.b, Config.MarkerColor.a, Config.MarkerBob, Config.MarkerRotate, 2, false, nil, nil, false)
                
                if dist1 < Config.InteractDistance then
                    showHelpNotification("Press ~INPUT_CONTEXT~ to Enter/Teleport")
                    if IsControlJustReleased(0, Config.InteractKey) then
                        TriggerServerEvent('tp_system:requestTeleport', id, 1)
                    end
                end
            end

            -- Check Point 2 (Unless OneWay)
            if not data.isOneWay then
                local dist2 = #(pCoords - vector3(data.pos2.x, data.pos2.y, data.pos2.z))
                if dist2 < Config.DrawDistance then
                    sleep = 0
                    DrawMarker(Config.MarkerType, data.pos2.x, data.pos2.y, data.pos2.z - 0.95, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, Config.MarkerColor.r, Config.MarkerColor.g, Config.MarkerColor.b, Config.MarkerColor.a, Config.MarkerBob, Config.MarkerRotate, 2, false, nil, nil, false)

                    if dist2 < Config.InteractDistance then
                        showHelpNotification("Press ~INPUT_CONTEXT~ to Exit/Teleport")
                        if IsControlJustReleased(0, Config.InteractKey) then
                            TriggerServerEvent('tp_system:requestTeleport', id, 2)
                        end
                    end
                end
            end
        end
        Wait(sleep)
    end
end)