"""Source of truth for the ARK:BLOX The Island databases.

Edit this file, then run `python3 ark-blox/tools/gen.py` to regenerate the
Luau ModuleScripts in ark-blox/modules/ and ark-blox/model_manifest.csv.

Model status values:
  done     - model already imported in the Studio place (see notes)
  keep     - existing model is good enough, do not replace
  todo     - no model yet; realistic Sketchfab candidates in model_candidates.csv
"""

QUALITY_TIERS = [
    # id, name, stat multiplier threshold (ASE wiki), UI color
    ("PRIMITIVE", "Primitive", 1.0, "#E6E6E6"),
    ("RAMSHACKLE", "Ramshackle", 1.25, "#4CAF50"),
    ("APPRENTICE", "Apprentice", 2.5, "#2196F3"),
    ("JOURNEYMAN", "Journeyman", 4.5, "#9C27B0"),
    ("MASTERCRAFT", "Mastercraft", 7.0, "#FFC107"),
    ("ASCENDANT", "Ascendant", 10.0, "#00E5FF"),
]

# Item categories that roll quality in vanilla ASE.
QUALITY_CATEGORIES = {"Tool", "Weapon", "Armor", "Shield", "Saddle"}

BUILDING_TIERS = ["Thatch", "Wood", "Stone", "Greenhouse", "Metal", "Tek"]

# ---------------------------------------------------------------------------
# Resources (inventory items). (id, name, subcategory)
# ---------------------------------------------------------------------------
RESOURCES = [
    ("Stone", "Stone", "Basic"), ("Flint", "Flint", "Basic"), ("Wood", "Wood", "Basic"),
    ("Thatch", "Thatch", "Basic"), ("Fiber", "Fiber", "Basic"), ("Metal", "Metal", "Mineral"),
    ("Obsidian", "Obsidian", "Mineral"), ("Crystal", "Crystal", "Mineral"), ("Oil", "Oil", "Mineral"),
    ("Sap", "Sap", "Basic"),
    ("Amarberry", "Amarberry", "Berry"), ("Azulberry", "Azulberry", "Berry"),
    ("Mejoberry", "Mejoberry", "Berry"), ("Narcoberry", "Narcoberry", "Berry"),
    ("Stimberry", "Stimberry", "Berry"), ("Tintoberry", "Tintoberry", "Berry"),
    ("RareFlower", "Rare Flower", "Plant"), ("RareMushroom", "Rare Mushroom", "Plant"),
    ("PlantSpeciesXSeed", "Plant Species X Seed", "Seed"),
    ("AmarberrySeed", "Amarberry Seed", "Seed"), ("AzulberrySeed", "Azulberry Seed", "Seed"),
    ("MejoberrySeed", "Mejoberry Seed", "Seed"), ("NarcoberrySeed", "Narcoberry Seed", "Seed"),
    ("StimberrySeed", "Stimberry Seed", "Seed"), ("TintoberrySeed", "Tintoberry Seed", "Seed"),
    ("CitronalSeed", "Citronal Seed", "Seed"), ("LongrassSeed", "Longrass Seed", "Seed"),
    ("RockarrotSeed", "Rockarrot Seed", "Seed"), ("SavorootSeed", "Savoroot Seed", "Seed"),
    ("CementingPaste", "Cementing Paste", "Special"), ("SilicaPearls", "Silica Pearls", "Special"),
    ("BlackPearl", "Black Pearl", "Special"), ("GiantBeeHoney", "Giant Bee Honey", "Special"),
    ("Hide", "Hide", "Creature"), ("Pelt", "Pelt", "Creature"), ("Keratin", "Keratin", "Creature"),
    ("Chitin", "Chitin", "Creature"),
    ("RawMeat", "Raw Meat", "Meat"), ("RawPrimeMeat", "Raw Prime Meat", "Meat"),
    ("RawFishMeat", "Raw Fish Meat", "Meat"), ("RawPrimeFishMeat", "Raw Prime Fish Meat", "Meat"),
    ("OrganicPolymer", "Organic Polymer", "Creature"), ("AchatinaPaste", "Achatina Paste", "Creature"),
    ("LeechBlood", "Leech Blood", "Creature"), ("AnglerGel", "AnglerGel", "Creature"),
    ("AmmoniteBile", "Ammonite Bile", "Creature"), ("TusoteuthisTentacle", "Tusoteuthis Tentacle", "Creature"),
]
# Inventory models already made in the previous session.
RESOURCE_MODELS_DONE = {"SilicaPearls", "Oil"}

# ---------------------------------------------------------------------------
# Harvest nodes. (id, display name, biome/where, tool, [(item, weight)], model status)
# weight = relative share of the node's yield; tool: Hand/Pick/Hatchet/Any/Sickle
# All 42 world nodes were modelled in the previous session -> "done".
# ---------------------------------------------------------------------------
HARVEST_NODES = [
    # Rocks
    ("SMALL_ROCK", "Small Rock", "All", "Any", [("Stone", 70), ("Flint", 30)]),
    ("STONE_ROCK", "Stone Rock", "All", "Any", [("Stone", 70), ("Flint", 30)]),
    ("LARGE_STONE_ROCK", "Large Stone Rock", "All", "Any", [("Stone", 70), ("Flint", 30)]),
    ("RIVER_ROCK", "River Rock", "River", "Any", [("Stone", 60), ("Flint", 35), ("Metal", 5)]),
    ("METAL_ROCK", "Metal Rock", "Mountain,Snow,Cave", "Pick", [("Metal", 45), ("Stone", 35), ("Flint", 20)]),
    ("RICH_METAL_ROCK", "Rich Metal Rock", "Mountain,Volcano,Cave", "Pick", [("Metal", 65), ("Stone", 25), ("Flint", 10)]),
    ("OBSIDIAN_ROCK", "Obsidian Rock", "Volcano,Mountain,Cave", "Pick", [("Obsidian", 75), ("Stone", 25)]),
    ("CRYSTAL_NODE", "Crystal Node", "Mountain,Snow,Cave", "Pick", [("Crystal", 80), ("Stone", 18), ("RareMushroom", 2)]),
    ("OIL_ROCK", "Oil Rock", "Snow,Beach,Volcano", "Pick", [("Oil", 70), ("Stone", 30)]),
    ("OIL_ROCK_SNOW", "Oil Rock (Snow Coast)", "Snow", "Pick", [("Oil", 70), ("Stone", 30)]),
    ("UNDERWATER_OIL_NODE", "Underwater Oil Node", "Ocean,UnderwaterCave", "Pick", [("Oil", 90), ("Stone", 10)]),
    ("CAVE_ROCK", "Cave Rock", "Cave", "Any", [("Stone", 65), ("Flint", 35)]),
    ("CAVE_METAL_NODE", "Cave Metal Node", "Cave", "Pick", [("Metal", 60), ("Stone", 40)]),
    ("CAVE_CRYSTAL", "Cave Crystal", "Cave", "Pick", [("Crystal", 100)]),
    ("CAVE_OBSIDIAN", "Cave Obsidian", "Cave", "Pick", [("Obsidian", 100)]),
    ("CAVE_OIL_NODE", "Cave Oil Node", "Cave", "Pick", [("Oil", 100)]),
    # Trees
    ("TREE_SMALL", "Small Tree", "Grassland,Jungle,Beach", "Hatchet", [("Wood", 60), ("Thatch", 40)]),
    ("TREE_MEDIUM", "Medium Tree", "Grassland,Jungle", "Hatchet", [("Wood", 60), ("Thatch", 40)]),
    ("TREE_LARGE", "Large Tree", "Jungle,Grassland", "Hatchet", [("Wood", 65), ("Thatch", 35)]),
    ("JUNGLE_TREE", "Jungle Tree", "Jungle", "Hatchet", [("Wood", 60), ("Thatch", 40)]),
    ("REDWOOD_TREE", "Redwood Tree", "Redwoods", "Hatchet", [("Wood", 70), ("Thatch", 30)]),
    ("DEAD_TREE", "Dead Tree", "Snow,Volcano", "Hatchet", [("Wood", 90), ("Thatch", 10)]),
    ("TREE_STUMP", "Tree Stump", "All", "Hatchet", [("Wood", 60), ("Thatch", 40)]),
    ("SWAMP_TREE", "Swamp Tree", "Swamp", "Hatchet", [("Wood", 60), ("Thatch", 40)]),
    ("SWAMP_ROOT_TREE", "Swamp Root Tree", "Swamp", "Hatchet", [("Wood", 55), ("Thatch", 35), ("RareMushroom", 10)]),
    ("SAP_TREE", "Redwood Tree (Sap Tap spot)", "Redwoods", "Hatchet", [("Wood", 70), ("Thatch", 30)]),
    # Bushes
    ("BUSH", "Bush", "All", "Hand", [("Fiber", 40), ("Amarberry", 10), ("Azulberry", 10), ("Mejoberry", 8), ("Narcoberry", 8), ("Stimberry", 8), ("Tintoberry", 10), ("AmarberrySeed", 1), ("CitronalSeed", 1), ("LongrassSeed", 1), ("RockarrotSeed", 1), ("SavorootSeed", 1)]),
    ("BERRY_BUSH", "Berry Bush", "All", "Hand", [("Fiber", 30), ("Amarberry", 12), ("Azulberry", 12), ("Mejoberry", 12), ("Narcoberry", 10), ("Stimberry", 10), ("Tintoberry", 12), ("MejoberrySeed", 1), ("NarcoberrySeed", 1)]),
    ("SNOW_BUSH", "Snow Bush", "Snow", "Hand", [("Fiber", 45), ("Amarberry", 10), ("Mejoberry", 10), ("Narcoberry", 10), ("Stimberry", 10), ("Tintoberry", 10), ("RareFlower", 5)]),
    ("RED_MOUNTAIN_BUSH", "Red Mountain Bush", "Mountain", "Hand", [("Fiber", 40), ("Azulberry", 10), ("Mejoberry", 10), ("Narcoberry", 10), ("Tintoberry", 10), ("RareFlower", 15), ("PlantSpeciesXSeed", 5)]),
    ("REDWOOD_BUSH", "Redwood Bush", "Redwoods", "Hand", [("Fiber", 45), ("Amarberry", 10), ("Azulberry", 10), ("Mejoberry", 10), ("Stimberry", 10), ("Tintoberry", 15)]),
    ("SWAMP_BUSH", "Swamp Bush", "Swamp", "Hand", [("Fiber", 50), ("Azulberry", 12), ("Mejoberry", 12), ("Narcoberry", 13), ("Stimberry", 13)]),
    ("SWAMP_CATTAIL", "Swamp Cattail", "Swamp", "Hand", [("Fiber", 40), ("Amarberry", 10), ("Narcoberry", 10), ("Stimberry", 10), ("RareFlower", 25), ("PlantSpeciesXSeed", 5)]),
    ("SWAMP_BRAMBLE", "Swamp Bramble", "Swamp", "Hand", [("Fiber", 40), ("Azulberry", 10), ("Mejoberry", 10), ("Tintoberry", 10), ("RareFlower", 25), ("PlantSpeciesXSeed", 5)]),
    ("RARE_MUSHROOM_SOURCE", "Rare Mushroom Source", "Swamp,Cave", "Hand", [("RareMushroom", 100)]),
    # Harvest structures
    ("SAP_TAP", "Tree Sap Tap", "Redwoods", "Hand", [("Sap", 100)]),
    ("GIANT_BEE_HIVE", "Giant Bee Hive", "Redwoods", "Hand", [("GiantBeeHoney", 100)]),
    ("BEAVER_DAM", "Giant Beaver Dam", "River,Swamp,Redwoods", "Hand", [("Wood", 40), ("CementingPaste", 25), ("RareFlower", 12), ("RareMushroom", 12), ("SilicaPearls", 11)]),
    ("PEARL_CLAM", "Pearl Clam", "Ocean,Snow", "Hand", [("SilicaPearls", 100)]),
    ("UNDERWATER_PEARL_NODE", "Underwater Pearl Node", "UnderwaterCave", "Hand", [("SilicaPearls", 100)]),
    ("UNDERWATER_CAVE_PEARL_CLAM", "Underwater Cave Pearl Clam", "UnderwaterCave", "Hand", [("SilicaPearls", 100)]),
    ("SWAMP_CAVE_VEGETATION", "Swamp Cave Vegetation", "Cave", "Hand", [("Fiber", 50), ("Azulberry", 15), ("Mejoberry", 15), ("RareMushroom", 20)]),
]

# Corpse / creature sources. These use the creature's own model (CreatureLibrary),
# so no extra model is needed. (id, creature, tool, [(item, weight)])
CORPSE_SOURCES = [
    ("TRILOBITE_CORPSE", "Trilobite", "Pick", [("Chitin", 40), ("RawMeat", 15), ("Oil", 20), ("SilicaPearls", 20), ("BlackPearl", 5)]),
    ("EURYPTERID_CORPSE", "Eurypterid", "Pick", [("Chitin", 45), ("Oil", 25), ("SilicaPearls", 25), ("BlackPearl", 5)]),
    ("LEECH_CORPSE", "Leech", "Any", [("LeechBlood", 40), ("Chitin", 30), ("SilicaPearls", 30)]),
    ("AMMONITE_CORPSE", "Ammonite", "Any", [("Chitin", 35), ("AmmoniteBile", 25), ("BlackPearl", 10), ("SilicaPearls", 15), ("RawMeat", 15)]),
    ("TUSOTEUTHIS_CORPSE", "Tusoteuthis", "Any", [("BlackPearl", 15), ("Oil", 25), ("RawFishMeat", 25), ("RawPrimeFishMeat", 15), ("TusoteuthisTentacle", 20)]),
    ("KAIRUKU_CORPSE", "Kairuku", "Pick", [("OrganicPolymer", 50), ("Hide", 25), ("RawMeat", 25)]),
    ("ANGLERFISH_CORPSE", "Angler", "Any", [("AnglerGel", 40), ("RawFishMeat", 40), ("RawPrimeFishMeat", 20)]),
    ("ACHATINA", "Achatina", "Hand", [("AchatinaPaste", 100)]),
    ("DINO_CORPSE", "*", "Hatchet", [("RawMeat", 60), ("Hide", 40)]),
    ("LARGE_DINO_CORPSE", "*Large", "Hatchet", [("RawMeat", 50), ("RawPrimeMeat", 10), ("Hide", 40)]),
    ("HORNED_CORPSE", "*Horned", "Pick", [("Keratin", 40), ("Hide", 30), ("RawMeat", 30)]),
    ("FURRY_CORPSE", "*Furry", "Hatchet", [("Pelt", 35), ("Hide", 30), ("RawMeat", 35)]),
    ("INSECT_CORPSE", "*Insect", "Pick", [("Chitin", 70), ("RawMeat", 30)]),
    ("FISH_CORPSE", "*Fish", "Any", [("RawFishMeat", 100)]),
    ("LARGE_FISH_CORPSE", "*LargeFish", "Any", [("RawFishMeat", 80), ("RawPrimeFishMeat", 20)]),
]

# ---------------------------------------------------------------------------
# Structures (placeables). (id, name, category, tier, station/fn, slots, fuel, status)
# Building pieces (Thatch..Tek) are listed separately as "keep".
# slots / fuel follow the ASE wiki; values marked None are not containers.
# ---------------------------------------------------------------------------
STRUCTURES = [
    # Crafting (first 15 were made in the previous session)
    ("MortarAndPestle", "Mortar And Pestle", "Crafting", "Early crafting", 50, None, "done"),
    ("Campfire", "Campfire", "Crafting", "Cooking / light", 8, "Wood,Thatch,Sparkpowder,AnglerGel", "done"),
    ("StoneFireplace", "Stone Fireplace", "Crafting", "Warmth / light", 8, "Wood,Thatch,Sparkpowder,AnglerGel", "done"),
    ("RefiningForge", "Refining Forge", "Crafting", "Smelting", 8, "Wood,Thatch,Sparkpowder,AnglerGel", "done"),
    ("Smithy", "Smithy", "Crafting", "Metal equipment / saddles", 50, None, "done"),
    ("CookingPot", "Cooking Pot", "Crafting", "Cooking / dyes", 12, "Wood,Thatch,Sparkpowder,AnglerGel", "done"),
    ("PreservingBin", "Preserving Bin", "Storage", "Slows spoil", 20, "Sparkpowder", "done"),
    ("BeerBarrel", "Beer Barrel", "Crafting", "Brewing", 12, None, "done"),
    ("CompostBin", "Compost Bin", "Farming", "Fertilizer", 25, None, "done"),
    ("StorageBox", "Storage Box", "Storage", "Storage", 20, None, "done"),
    ("LargeStorageBox", "Large Storage Box", "Storage", "Storage", 45, None, "done"),
    ("Bookshelf", "Bookshelf", "Storage", "Notes / blueprints", 50, None, "done"),
    ("FeedingTrough", "Feeding Trough", "Storage", "Tame food", 60, None, "done"),
    ("WaterReservoir", "Water Reservoir", "Storage", "Water", None, None, "done"),
    ("TreeSapTap", "Tree Sap Tap", "Farming", "Sap on Redwood", None, None, "done"),
    ("Fabricator", "Fabricator", "Crafting", "Advanced industrial crafting", 70, "Gasoline", "todo"),
    ("ChemistryBench", "Chemistry Bench", "Crafting", "Advanced chemistry", 50, "Electricity", "todo"),
    ("IndustrialForge", "Industrial Forge", "Crafting", "High-volume smelting", 150, "Gasoline", "todo"),
    ("IndustrialGrill", "Industrial Grill", "Crafting", "Mass grilling", 100, "Gasoline", "todo"),
    ("IndustrialCooker", "Industrial Cooker", "Crafting", "Mass cooking", 60, "Gasoline", "todo"),
    ("IndustrialGrinder", "Industrial Grinder", "Crafting", "Grinding / refund", 50, "Electricity", "todo"),
    ("Refrigerator", "Refrigerator", "Storage", "Slows spoil (x100)", 80, "Electricity", "todo"),
    ("AirConditioner", "Air Conditioner", "Utility", "Insulation", None, "Electricity", "todo"),
    ("TekReplicator", "Tek Replicator", "Crafting", "Tek crafting", 600, None, "todo"),
    # Storage
    ("Vault", "Vault", "Storage", "Storage", 350, None, "todo"),
    ("MetalWaterReservoir", "Metal Water Reservoir", "Storage", "Water", None, None, "todo"),
    ("TekTrough", "Tek Trough", "Storage", "Tame food (spoil x100)", 600, None, "todo"),
    # Farming
    ("SmallCropPlot", "Small Crop Plot", "Farming", "Crop", 10, None, "todo"),
    ("MediumCropPlot", "Medium Crop Plot", "Farming", "Crop", 20, None, "todo"),
    ("LargeCropPlot", "Large Crop Plot", "Farming", "Crop", 30, None, "todo"),
] + [
    (f"{mat}IrrigationPipe{kind.replace(' ', '')}", f"{mat} Irrigation Pipe - {kind}", "Farming", "Water pipe", None, None, "todo")
    for mat in ("Stone", "Metal")
    for kind in ("Intake", "Straight", "Inclined", "Vertical", "Intersection", "Tap", "Flexible")
] + [
    # Electrical
    ("ElectricalGenerator", "Electrical Generator", "Electrical", "Power source", 1, "Gasoline", "todo"),
    ("ElectricalCableStraight", "Straight Electrical Cable", "Electrical", "Cable", None, None, "todo"),
    ("ElectricalCableVertical", "Vertical Electrical Cable", "Electrical", "Cable", None, None, "todo"),
    ("ElectricalCableInclined", "Inclined Electrical Cable", "Electrical", "Cable", None, None, "todo"),
    ("ElectricalCableFlexible", "Flexible Electrical Cable", "Electrical", "Cable", None, None, "todo"),
    ("ElectricalCableIntersection", "Electrical Cable Intersection", "Electrical", "Cable", None, None, "todo"),
    ("ElectricalOutlet", "Electrical Outlet", "Electrical", "Power outlet", None, None, "todo"),
    ("Lamppost", "Lamppost", "Electrical", "Light", None, "Electricity", "todo"),
    ("OmnidirectionalLamppost", "Omnidirectional Lamppost", "Electrical", "Light", None, "Electricity", "todo"),
    # Defense
    ("WoodenSpikeWall", "Wooden Spike Wall", "Defense", "Damage wall", None, None, "todo"),
    ("MetalSpikeWall", "Metal Spike Wall", "Defense", "Damage wall", None, None, "todo"),
    ("BearTrap", "Bear Trap", "Defense", "Trap", None, None, "todo"),
    ("LargeBearTrap", "Large Bear Trap", "Defense", "Trap", None, None, "todo"),
    ("TripwireAlarmTrap", "Tripwire Alarm Trap", "Defense", "Trap", None, None, "todo"),
    ("TripwireNarcoticTrap", "Tripwire Narcotic Trap", "Defense", "Trap", None, None, "todo"),
    ("PlantSpeciesX", "Plant Species X", "Defense", "Turret plant", None, None, "todo"),
    ("CatapultTurret", "Catapult Turret", "Defense", "Turret", 20, None, "todo"),
    ("BallistaTurret", "Ballista Turret", "Defense", "Turret", 20, None, "todo"),
    ("AutoTurret", "Auto Turret", "Defense", "Turret", 20, "Electricity", "todo"),
    ("HeavyAutoTurret", "Heavy Auto Turret", "Defense", "Turret", 20, "Electricity", "todo"),
    ("MinigunTurret", "Minigun Turret", "Defense", "Turret", 20, None, "todo"),
    ("RocketTurret", "Rocket Turret", "Defense", "Turret", 20, None, "todo"),
    ("TekTurret", "Tek Turret", "Defense", "Turret", 20, "Element", "todo"),
    # Beds & player
    ("HideSleepingBag", "Hide Sleeping Bag", "Bed", "Respawn (single use)", None, None, "todo"),
    ("SimpleBed", "Simple Bed", "Bed", "Respawn", None, None, "todo"),
    ("BunkBed", "Bunk Bed", "Bed", "Respawn", None, None, "todo"),
    ("SleepingPod", "Sleeping Pod", "Bed", "Respawn / sleep", None, None, "todo"),
    ("TrophyWallMount", "Trophy Wall-Mount", "Decor", "Trophy", None, None, "todo"),
    ("ArtifactPedestal", "Artifact Pedestal", "Decor", "Artifact display", None, None, "todo"),
    ("DisplayCase", "Display Case", "Decor", "Item display", None, None, "todo"),
    ("TrainingDummy", "Training Dummy", "Decor", "DPS test", None, None, "todo"),
    ("LoadoutMannequin", "Loadout Mannequin", "Decor", "Gear loadout", None, None, "todo"),
]

# ---------------------------------------------------------------------------
# Building pieces per tier (models exist - keep). Names follow the list the
# owner provided; the database still needs every entry.
# ---------------------------------------------------------------------------
BUILDING_PIECES = {
    "Thatch": ["Foundation", "Triangle Foundation", "Ceiling", "Triangle Ceiling", "Wall", "Doorframe", "Door",
               "Sloped Wall Left", "Sloped Wall Right", "Sloped Roof", "Hatchframe", "Trapdoor", "Pillar",
               "Railing", "Ramp", "Staircase", "Ladder", "Fence Foundation", "Fence Support"],
    "Wood": ["Foundation", "Triangle Foundation", "Ceiling", "Triangle Ceiling", "Wall", "Sloped Wall Left",
             "Sloped Wall Right", "Sloped Roof", "Triangle Roof", "Doorframe", "Door", "Double Doorframe",
             "Double Door", "Windowframe", "Window", "Hatchframe", "Trapdoor", "Pillar", "Railing", "Ramp",
             "Staircase", "Ladder", "Fence Foundation", "Fence Support", "Catwalk", "Tree Platform", "Sign",
             "Wall Sign", "Billboard", "Dinosaur Gateway", "Dinosaur Gate"],
    "Stone": ["Foundation", "Triangle Foundation", "Ceiling", "Triangle Ceiling", "Wall", "Large Wall",
              "Sloped Wall Left", "Sloped Wall Right", "Sloped Roof", "Triangle Roof", "Doorframe",
              "Reinforced Wooden Door", "Double Doorframe", "Reinforced Double Door", "Windowframe",
              "Reinforced Window", "Hatchframe", "Giant Hatchframe", "Trapdoor", "Giant Reinforced Trapdoor",
              "Pillar", "Railing", "Ramp", "Staircase", "Fence Foundation", "Fence Support", "Catwalk",
              "Dinosaur Gateway", "Reinforced Dinosaur Gate"],
    "Greenhouse": ["Foundation", "Ceiling", "Triangle Ceiling", "Wall", "Sloped Wall Left", "Sloped Wall Right",
                   "Doorframe", "Door", "Double Doorframe", "Double Door", "Window", "Sloped Roof", "Triangle Roof"],
    "Metal": ["Foundation", "Triangle Foundation", "Ceiling", "Triangle Ceiling", "Wall", "Sloped Wall Left",
              "Sloped Wall Right", "Sloped Roof", "Triangle Roof", "Doorframe", "Door", "Double Doorframe",
              "Double Door", "Windowframe", "Window", "Hatchframe", "Giant Hatchframe", "Trapdoor",
              "Giant Trapdoor", "Pillar", "Railing", "Ramp", "Staircase", "Ladder", "Fence Foundation",
              "Fence Support", "Catwalk", "Tree Platform", "Ocean Platform", "Sign", "Wall Sign", "Billboard",
              "Dinosaur Gateway", "Dinosaur Gate", "Behemoth Gateway", "Behemoth Gate"],
    "Tek": ["Foundation", "Triangle Foundation", "Fence Foundation", "Fence Support", "Ceiling", "Triangle Ceiling",
            "Wall", "Large Wall", "Sloped Wall Left", "Sloped Wall Right", "Sloped Roof", "Triangle Roof",
            "Doorframe", "Door", "Double Doorframe", "Double Door", "Windowframe", "Window", "Hatchframe",
            "Trapdoor", "Pillar", "Railing", "Ramp", "Staircase", "Ladder", "Catwalk", "Dinosaur Gateway",
            "Dinosaur Gate", "Behemoth Gateway", "Behemoth Gate", "Ocean Platform"],
}
# Stone-tier pieces that look wooden (mechanically stone tier).
STONE_TIER_WOOD_LOOK = {"Reinforced Wooden Door", "Reinforced Double Door", "Reinforced Window",
                        "Reinforced Dinosaur Gate", "Giant Reinforced Trapdoor"}
# Tek functional structures (not building pieces, need models).
TEK_FUNCTIONAL = [("TekTransmitter", "Tek Transmitter"), ("TekTeleporter", "Tek Teleporter"),
                  ("TekShieldGenerator", "Tek Forcefield")]

# ---------------------------------------------------------------------------
# Equipment. (id, name, subcategory, station, sources)
# ---------------------------------------------------------------------------
LOOT = "Engram,SupplyCrate,CaveLoot"
TOOLS = [
    ("StonePick", "Stone Pick", "Harvest", "Inventory", LOOT),
    ("StoneHatchet", "Stone Hatchet", "Harvest", "Inventory", LOOT),
    ("Torch", "Torch", "Light", "Inventory", "Engram"),
    ("MetalPick", "Metal Pick", "Harvest", "Smithy", LOOT),
    ("MetalHatchet", "Metal Hatchet", "Harvest", "Smithy", LOOT),
    ("MetalSickle", "Metal Sickle", "Harvest", "Smithy", LOOT),
    ("Spyglass", "Spyglass", "Utility", "Inventory", "Engram"),
    ("Compass", "Compass", "Utility", "Inventory", "Engram"),
    ("GPS", "GPS", "Utility", "Fabricator", "Engram"),
    ("MagnifyingGlass", "Magnifying Glass", "Utility", "Inventory", "Engram"),
    ("FishingRod", "Fishing Rod", "Utility", "Smithy", LOOT),
    ("Paintbrush", "Paintbrush", "Utility", "Inventory", "Engram"),
    ("SprayPainter", "Spray Painter", "Utility", "Fabricator", "Engram"),
    ("Scissors", "Scissors", "Utility", "Smithy", "Engram"),
    ("Camera", "Camera", "Utility", "Fabricator", "Engram"),
    ("Radio", "Radio", "Utility", "Fabricator", "Engram"),
    ("RemoteKeypad", "Remote Keypad", "Utility", "Fabricator", "Engram"),
    ("Electronics", "Electronics", "Component", "Fabricator", "Engram"),
]
# Tools without quality in vanilla (utility items).
NO_QUALITY_TOOLS = {"Torch", "Spyglass", "Compass", "GPS", "MagnifyingGlass", "Paintbrush", "SprayPainter",
                    "Camera", "Radio", "RemoteKeypad", "Electronics", "Scissors"}

# (id, name, subcategory, station, sources, ammo ids)
WEAPONS = [
    ("WoodenClub", "Wooden Club", "Melee", "Inventory", LOOT, []),
    ("Spear", "Spear", "Melee", "Inventory", LOOT, []),
    ("Pike", "Pike", "Melee", "Smithy", LOOT, []),
    ("Sword", "Sword", "Melee", "Smithy", LOOT, []),
    ("ElectricProd", "Electric Prod", "Melee", "Fabricator", LOOT, []),
    ("Slingshot", "Slingshot", "Ranged", "Inventory", LOOT, ["Stone"]),
    ("Bola", "Bola", "Thrown", "Inventory", "Engram", []),
    ("Bow", "Bow", "Ranged", "Inventory", LOOT, ["StoneArrow", "TranqArrow"]),
    ("Crossbow", "Crossbow", "Ranged", "Smithy", LOOT, ["StoneArrow", "TranqArrow", "GrapplingHook"]),
    ("CompoundBow", "Compound Bow", "Ranged", "Fabricator", LOOT, ["StoneArrow", "TranqArrow"]),
    ("SimplePistol", "Simple Pistol", "Firearm", "Smithy", LOOT, ["SimpleBullet"]),
    ("LongneckRifle", "Longneck Rifle", "Firearm", "Smithy", LOOT, ["SimpleRifleAmmo", "TranquilizerDart", "ShockingTranquilizerDart"]),
    ("Shotgun", "Shotgun", "Firearm", "Smithy", LOOT, ["SimpleShotgunAmmo"]),
    ("FabricatedPistol", "Fabricated Pistol", "Firearm", "Fabricator", LOOT, ["AdvancedBullet"]),
    ("PumpActionShotgun", "Pump-Action Shotgun", "Firearm", "Fabricator", LOOT, ["SimpleShotgunAmmo"]),
    ("FabricatedSniperRifle", "Fabricated Sniper Rifle", "Firearm", "Fabricator", LOOT, ["AdvancedRifleAmmo"]),
    ("RocketLauncher", "Rocket Launcher", "Heavy", "Fabricator", LOOT, ["RocketPropelledGrenade"]),
    ("HarpoonLauncher", "Harpoon Launcher", "Ranged", "Fabricator", LOOT, ["SpearBolt", "TranqSpearBolt"]),
    ("Cannon", "Cannon", "Structure", "Smithy", "Engram", ["CannonBall"]),
]

AMMO = [
    ("StoneArrow", "Stone Arrow", "Inventory"), ("TranqArrow", "Tranq Arrow", "Inventory"),
    ("SimpleBullet", "Simple Bullet", "Smithy"), ("AdvancedBullet", "Advanced Bullet", "Fabricator"),
    ("SimpleRifleAmmo", "Simple Rifle Ammo", "Smithy"), ("AdvancedRifleAmmo", "Advanced Rifle Ammo", "Fabricator"),
    ("TranquilizerDart", "Tranquilizer Dart", "Smithy"), ("ShockingTranquilizerDart", "Shocking Tranquilizer Dart", "Fabricator"),
    ("SimpleShotgunAmmo", "Simple Shotgun Ammo", "Smithy"), ("RocketPropelledGrenade", "Rocket Propelled Grenade", "Fabricator"),
    ("Grenade", "Grenade", "Inventory"), ("CannonBall", "Cannon Ball", "Smithy"),
    ("SpearBolt", "Spear Bolt", "Smithy"), ("TranqSpearBolt", "Tranq Spear Bolt", "Smithy"),
    ("GrapplingHook", "Grappling Hook", "Smithy"), ("RocketHomingMissile", "Rocket Homing Missile", "Fabricator"),
    ("C4Charge", "C4 Charge", "Fabricator"), ("C4RemoteDetonator", "C4 Remote Detonator", "Fabricator"),
    ("HomingUnderwaterMine", "Homing Underwater Mine", "Fabricator"),
]

ARMOR_SETS = {
    "Cloth": (["Cloth Hat", "Cloth Shirt", "Cloth Pants", "Cloth Gloves", "Cloth Boots"], "Inventory"),
    "Hide": (["Hide Hat", "Hide Shirt", "Hide Pants", "Hide Gloves", "Hide Boots"], "Inventory"),
    "Fur": (["Fur Cap", "Fur Chestpiece", "Fur Leggings", "Fur Gauntlets", "Fur Boots"], "Smithy"),
    "Chitin": (["Chitin Helmet", "Chitin Chestpiece", "Chitin Leggings", "Chitin Gauntlets", "Chitin Boots"], "Smithy"),
    "Ghillie": (["Ghillie Mask", "Ghillie Chestpiece", "Ghillie Leggings", "Ghillie Gauntlets", "Ghillie Boots"], "Inventory"),
    "Flak": (["Flak Helmet", "Flak Chestpiece", "Flak Leggings", "Flak Gauntlets", "Flak Boots"], "Smithy"),
    "SCUBA": (["SCUBA Mask", "SCUBA Tank", "SCUBA Leggings", "SCUBA Flippers"], "Fabricator"),
    "Riot": (["Riot Helmet", "Riot Chestpiece", "Riot Leggings", "Riot Gauntlets", "Riot Boots"], "Fabricator"),
    "Tek": (["Tek Helmet", "Tek Chestpiece", "Tek Leggings", "Tek Gauntlets", "Tek Boots"], "TekReplicator"),
}
ARMOR_SLOTS = ["Head", "Chest", "Legs", "Hands", "Feet"]
SCUBA_SLOTS = ["Head", "Chest", "Legs", "Feet"]

SHIELDS = [("WoodenShield", "Wooden Shield", "Inventory"), ("MetalShield", "Metal Shield", "Smithy"),
           ("RiotShield", "Riot Shield", "Fabricator"), ("TekShield", "Tek Shield", "TekReplicator")]

# Saddles: (creature, type). type = Ground/Flying/Aquatic/Platform/Tek
SADDLES = [(c, "Ground") for c in [
    "Parasaur", "Carbonemys", "Pachy", "Trike", "Raptor", "Iguanodon", "Stego", "Megaloceros", "Mammoth",
    "Pachyrhinosaurus", "Gallimimus", "Doedicurus", "Sarco", "Ankylo", "Sabertooth", "Direbear", "Baryonyx",
    "Megatherium", "Daeodon", "Thylacoleo", "Chalicotherium", "Procoptodon", "Castoroides", "WoollyRhino",
    "Megalosaurus", "Megalania", "Allosaurus", "Yutyrannus", "Therizinosaurus", "Giganotosaurus", "Carcharo",
    "Rhyniognatha", "Rex", "Spino", "Equus", "Kaprosuchus", "Terrorbird", "Beelzebufo",
    "Diplodocus", "Arthropleura"]] + \
    [(c, "Flying") for c in ["Pteranodon", "Argentavis", "Tapejara", "Pelagornis", "Quetz"]] + \
    [(c, "Aquatic") for c in ["Ichthyosaurus", "Megalodon", "Manta", "Basilosaurus", "Dunkleosteus",
                              "Mosasaur", "Plesiosaur", "Tusoteuthis"]] + \
    [(c, "Platform") for c in ["Paracer", "Bronto", "Plesiosaur", "Quetz", "Mosasaur", "Titanosaur"]] + \
    [(c, "Tek") for c in ["Megalodon", "Mosasaur", "Rex", "Tapejara"]]
# Saddle models that already exist in the place (from the creature session).
SADDLE_MODELS_DONE = {("Direbear", "Ground"), ("Megalosaurus", "Ground")}

# Crafting station per saddle type.
SADDLE_STATION = {"Ground": "Smithy", "Flying": "Smithy", "Aquatic": "Smithy", "Platform": "Smithy",
                  "Tek": "TekReplicator"}

# ---------------------------------------------------------------------------
# Realistic model search (Sketchfab). Queries are tried in order, separated by
# "|", until one returns a usable candidate (see tools/sketchfab_pick.py).
# Anything not listed falls back to "<name> realistic".
# ---------------------------------------------------------------------------
MODEL_QUERIES = {
    # Resources
    "Stone": "stone rock photogrammetry|stone rock", "Flint": "flint stone|flint rock",
    "Wood": "firewood logs|wood log", "Thatch": "straw bundle|hay bundle", "Fiber": "dried grass bundle|hay bundle",
    "Metal": "iron ore|metal ore rock", "Obsidian": "obsidian rock|obsidian", "Crystal": "quartz crystal cluster|crystal",
    "Oil": "oil canister", "Sap": "tree resin amber|amber", "Amarberry": "yellow berries|berries",
    "Azulberry": "blueberries|berries", "Mejoberry": "blackberries|berries", "Narcoberry": "elderberries|black berries",
    "Stimberry": "white berries|snowberry", "Tintoberry": "raspberries|berries", "RareFlower": "wild flower scan|flower",
    "RareMushroom": "mushroom photogrammetry|mushroom", "PlantSpeciesXSeed": "seed pod|seed",
    "AmarberrySeed": "seeds pile|seeds", "AzulberrySeed": "seeds pile|seeds", "MejoberrySeed": "seeds pile|seeds",
    "NarcoberrySeed": "seeds pile|seeds", "StimberrySeed": "seeds pile|seeds", "TintoberrySeed": "seeds pile|seeds",
    "CitronalSeed": "seeds pile|seeds", "LongrassSeed": "grass seeds|seeds", "RockarrotSeed": "carrot seeds|seeds",
    "SavorootSeed": "root seeds|seeds", "CementingPaste": "clay lump|wet clay", "SilicaPearls": "pearls",
    "BlackPearl": "black pearl|pearl", "GiantBeeHoney": "honeycomb", "Hide": "animal hide leather|leather hide",
    "Pelt": "fur pelt|animal fur", "Keratin": "animal horn|horn", "Chitin": "insect carapace|beetle shell",
    "RawMeat": "raw meat steak|raw meat", "RawPrimeMeat": "raw beef marbled steak|raw steak",
    "RawFishMeat": "raw fish fillet|fish fillet", "RawPrimeFishMeat": "salmon fillet|fish fillet",
    "OrganicPolymer": "wax lump|resin", "AchatinaPaste": "paste jar|clay jar", "LeechBlood": "blood vial|vial",
    "AnglerGel": "bioluminescent jelly|glowing jar", "AmmoniteBile": "green potion vial|potion vial",
    "TusoteuthisTentacle": "octopus tentacle|tentacle",
    # Tools
    "StonePick": "primitive stone pickaxe|stone pickaxe", "StoneHatchet": "stone axe primitive|stone axe",
    "Torch": "medieval torch|torch", "MetalPick": "pickaxe", "MetalHatchet": "hatchet axe|hatchet",
    "MetalSickle": "sickle", "Spyglass": "brass spyglass telescope|spyglass", "Compass": "old compass|compass",
    "GPS": "handheld gps|gps device", "MagnifyingGlass": "magnifying glass", "FishingRod": "fishing rod",
    "Paintbrush": "paint brush", "SprayPainter": "spray paint gun|paint sprayer", "Scissors": "scissors",
    "Camera": "vintage camera|camera", "Radio": "walkie talkie|radio", "RemoteKeypad": "keypad remote|keypad",
    "Electronics": "circuit board|pcb",
    # Weapons
    "WoodenClub": "wooden club", "Spear": "primitive spear|spear", "Pike": "pike polearm|halberd",
    "Sword": "medieval sword|sword", "ElectricProd": "stun baton|cattle prod", "Slingshot": "slingshot",
    "Bola": "bolas weapon|bola", "Bow": "wooden bow|longbow", "Crossbow": "crossbow", "CompoundBow": "compound bow",
    "SimplePistol": "flintlock pistol", "LongneckRifle": "bolt action rifle|hunting rifle",
    "Shotgun": "double barrel shotgun", "FabricatedPistol": "pistol handgun|pistol",
    "PumpActionShotgun": "pump action shotgun", "FabricatedSniperRifle": "sniper rifle",
    "RocketLauncher": "rocket launcher|rpg launcher", "HarpoonLauncher": "speargun|harpoon gun", "Cannon": "cannon",
    # Ammo
    "StoneArrow": "stone arrow|arrow", "TranqArrow": "arrow", "SimpleBullet": "musket ball|lead bullet",
    "AdvancedBullet": "9mm bullet|pistol bullet", "SimpleRifleAmmo": "rifle cartridge|bullet",
    "AdvancedRifleAmmo": "rifle ammo|ammo box", "TranquilizerDart": "tranquilizer dart|dart",
    "ShockingTranquilizerDart": "tranquilizer dart|dart", "SimpleShotgunAmmo": "shotgun shell",
    "RocketPropelledGrenade": "rpg rocket|rpg", "Grenade": "hand grenade|grenade", "CannonBall": "cannonball",
    "SpearBolt": "speargun spear|harpoon", "TranqSpearBolt": "harpoon", "GrapplingHook": "grappling hook",
    "RocketHomingMissile": "missile", "C4Charge": "c4 explosive", "C4RemoteDetonator": "detonator",
    "HomingUnderwaterMine": "naval mine|sea mine",
    # Shields
    "WoodenShield": "wooden round shield|wooden shield", "MetalShield": "metal shield",
    "RiotShield": "riot shield", "TekShield": "sci-fi shield",
    # Structures
    "Fabricator": "industrial machine workbench|industrial machine", "ChemistryBench": "chemistry lab table|laboratory table",
    "IndustrialForge": "industrial furnace|furnace", "IndustrialGrill": "industrial grill|commercial grill",
    "IndustrialCooker": "industrial kettle|cooking kettle", "IndustrialGrinder": "industrial grinder machine|grinder machine",
    "Refrigerator": "refrigerator|fridge", "AirConditioner": "air conditioner unit|air conditioner",
    "TekReplicator": "sci-fi machine|sci-fi fabricator", "Vault": "safe vault|safe", "MetalWaterReservoir": "water tank metal|water tank",
    "TekTrough": "sci-fi container|sci-fi crate", "SmallCropPlot": "raised garden bed|garden bed",
    "MediumCropPlot": "raised garden bed|garden bed", "LargeCropPlot": "raised garden bed|garden bed",
    "ElectricalGenerator": "diesel generator|generator", "ElectricalCableStraight": "electrical cable",
    "ElectricalCableVertical": "electrical cable", "ElectricalCableInclined": "electrical cable",
    "ElectricalCableFlexible": "electrical cable", "ElectricalCableIntersection": "junction box|electrical box",
    "ElectricalOutlet": "power outlet|wall socket", "Lamppost": "street lamp|lamp post",
    "OmnidirectionalLamppost": "floodlight tower|floodlight", "WoodenSpikeWall": "wooden spike barricade|wooden spikes",
    "MetalSpikeWall": "metal spike barricade|czech hedgehog", "BearTrap": "bear trap", "LargeBearTrap": "bear trap",
    "TripwireAlarmTrap": "tripwire trap|tripwire", "TripwireNarcoticTrap": "tripwire trap|tripwire",
    "PlantSpeciesX": "carnivorous plant|venus flytrap", "CatapultTurret": "catapult", "BallistaTurret": "ballista",
    "AutoTurret": "sentry turret|turret", "HeavyAutoTurret": "heavy turret|turret", "MinigunTurret": "minigun turret|minigun",
    "RocketTurret": "missile launcher turret|missile turret", "TekTurret": "sci-fi turret",
    "HideSleepingBag": "sleeping bag", "SimpleBed": "rustic wooden bed|wooden bed", "BunkBed": "bunk bed",
    "SleepingPod": "sci-fi sleeping pod|cryo pod", "TrophyWallMount": "trophy wall mount|hunting trophy",
    "ArtifactPedestal": "stone pedestal|pedestal", "DisplayCase": "glass display case|display case",
    "TrainingDummy": "training dummy", "LoadoutMannequin": "mannequin",
    "TekTransmitter": "sci-fi antenna|sci-fi transmitter", "TekTeleporter": "sci-fi teleporter pad|teleporter",
    "TekShieldGenerator": "sci-fi force field generator|shield generator",
}
# Irrigation pipes: query by material + piece.
PIPE_QUERIES = {"Intake": "water intake pipe", "Straight": "pipe", "Inclined": "pipe", "Vertical": "pipe",
                "Intersection": "pipe junction", "Tap": "water tap faucet", "Flexible": "flexible pipe"}
# Armor: per-set wording + per-slot noun.
ARMOR_QUERY_SET = {"Cloth": "linen cloth", "Hide": "leather", "Fur": "fur", "Chitin": "bone insect armor",
                   "Ghillie": "ghillie suit", "Flak": "military combat", "SCUBA": "scuba", "Riot": "riot police",
                   "Tek": "sci-fi armor"}
ARMOR_QUERY_SLOT = {"Head": "helmet", "Chest": "vest", "Legs": "pants", "Hands": "gloves", "Feet": "boots"}
SCUBA_QUERY = {"SCUBA Mask": "diving mask", "SCUBA Tank": "scuba tank", "SCUBA Leggings": "wetsuit",
               "SCUBA Flippers": "diving fins"}
SADDLE_QUERY = {"Ground": "{c} saddle|dinosaur saddle|leather saddle",
                "Flying": "{c} saddle|dragon saddle|leather saddle",
                "Aquatic": "{c} saddle|sea creature saddle|leather saddle harness",
                "Platform": "{c} platform saddle|howdah|wooden platform",
                "Tek": "{c} tek saddle|sci-fi saddle"}
