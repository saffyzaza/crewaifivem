Config = {}

-- Interaction settings
Config.InteractKey = 38 -- E (https://docs.fivem.net/docs/game-references/controls/)
Config.DrawDistance = 15.0 -- Distance to start rendering the marker
Config.InteractDistance = 1.5 -- Distance to allow the E prompt

-- Visual settings
Config.MarkerType = 1 -- Vertical Cylinder
Config.MarkerColor = { r = 0, g = 150, b = 255, a = 150 }
Config.MarkerBob = true
Config.MarkerRotate = false

-- Feature Toggles
Config.UseCinematicTransition = true
Config.FadeDuration = 500 -- Milliseconds
Config.EnableAcePermissions = false -- If true, requires ace permission 'teleport.[id]'
Config.VehicleTeleportEnabled = true

-- Teleport Pairs
-- pos: vector4(x, y, z, heading)
Config.TeleportPairs = {
    ["fib_elevator"] = {
        name = "FIB Elevator",
        pos1 = vector4(136.66, -761.85, 45.75, 160.0),
        pos2 = vector4(135.32, -766.7, 242.15, 0.0),
        isOneWay = false
    },
    ["police_roof"] = {
        name = "MRPD Roof Access",
        pos1 = vector4(464.3, -998.05, 24.91, 85.0),
        pos2 = vector4(461.5, -986.0, 40.8, 175.0),
        isOneWay = false
    }
}