-- Validation logic
local function IsPlayerAuthorized(source, teleportId)
    if not Config.EnableAcePermissions then return true end
    
    local permission = "teleport." .. teleportId
    return IsPlayerAceAllowed(source, permission) or IsPlayerAceAllowed(source, "teleport.all")
end

RegisterNetEvent('tp_system:requestTeleport')
AddEventHandler('tp_system:requestTeleport', function(teleportId, fromPoint)
    local src = source
    local ped = GetPlayerPed(src)
    local pCoords = GetEntityCoords(ped)
    local tpData = Config.TeleportPairs[teleportId]

    if not tpData then 
        print(string.format("^1[Security Check]^7 Player %s tried to access invalid teleport ID: %s", GetPlayerName(src), teleportId))
        return 
    end

    -- Authorization Check
    if not IsPlayerAuthorized(src, teleportId) then
        TriggerClientEvent('chat:addMessage', src, { args = { '^1SYSTEM', 'You do not have permission to use this teleport.' } })
        return
    end

    -- Distance Verification (Security against executors)
    local sourcePos = (fromPoint == 1) and tpData.pos1 or tpData.pos2
    local targetPos = (fromPoint == 1) and tpData.pos2 or tpData.pos1

    local distance = #(pCoords - vector3(sourcePos.x, sourcePos.y, sourcePos.z))
    if distance > (Config.InteractDistance + 5.0) then
        print(string.format("^1[Security Check]^7 Player %s failed distance check for teleport %s", GetPlayerName(src), teleportId))
        return
    end

    -- Log Admin actions if needed
    if Config.EnableAcePermissions then
        print(string.format("^2[Teleport]^7 Player %s used %s", GetPlayerName(src), tpData.name))
    end

    TriggerClientEvent('tp_system:performTeleport', src, targetPos)
end)