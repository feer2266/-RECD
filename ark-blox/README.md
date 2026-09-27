# ARK:BLOX, The Island databases

Data untuk material/harvest node, item + Quality, dan struktur crafting. Semua di-generate dari satu sumber data.

| File | Isi |
|---|---|
| `tools/data.py` | Sumber data. Edit di sini. |
| `tools/gen.py` | Generator. Jalankan `python3 ark-blox/tools/gen.py`. |
| `modules/QualityTiers.lua` | 6 quality ASE (Primitive x1 sampai Ascendant x10), tanpa Transcendent. Ada juga urutan tier bangunan. |
| `modules/HarvestNodeDatabase.lua` | 42 node dunia (batu, pohon, semak, rawa, laut, beaver dam, bee hive, sap tap) dan 15 sumber bangkai. Drop memakai bobot. |
| `modules/StructureDatabase.lua` | 79 struktur (crafting, storage, farming, listrik, pertahanan, bed, dekor, Tek) dengan slot dan bahan bakar, plus 159 building piece Thatch sampai Tek. |
| `modules/ItemDatabase_Island.lua` | 214 item: resource, tools, senjata (beserta amunisinya), amunisi, armor, shield, saddle. |
| `model_manifest.csv` | Semua 494 aset model beserta path folder, status (`done` / `keep` / `todo`), dan kata kunci pencarian Sketchfab. |

## Cara pakai di Studio

Buat ModuleScript di `ReplicatedStorage.ARK_Data` dengan nama yang sama seperti file, lalu tempel isinya. `ItemDatabase_Island` me-`require` `QualityTiers` dari folder yang sama.

Quality disimpan per instance item, bukan sebagai model terpisah:

```lua
local item = ItemDatabase.NewInstance("MetalPick", "MASTERCRAFT") -- { Id, Quality, Multiplier }
local dmg = QualityTiers.ScaleStat(baseDamage, item.Quality)
```

Item yang bukan Tool/Weapon/Armor/Shield/Saddle (serta tool utilitas seperti GPS dan Spyglass) selalu `PRIMITIVE`.

## Status model (dari `model_manifest.csv`)

- `done` 61: 42 node dunia, 15 struktur crafting/storage tahap awal, 2 item (Silica Pearls, Oil), 2 saddle (Direbear, Megalosaurus).
- `keep` 159: building piece. Model yang ada sudah cukup, tidak diganti.
- `todo` 274: Saddle 61, Resource 45, Armor 44, Ammo 19, Weapon 19, Tool 18, Farming 17, Defense 14, Electrical 9, Crafting/Utility 8, Decor 5, Bed 4, Storage 4, Shield 4, Tek 3.

## Catatan

- Nilai slot dan bahan bakar struktur mengikuti wiki ASE. Bobot drop node adalah perkiraan untuk gameplay, bukan angka resmi.
- Resep crafting (bahan per item) belum dimasukkan. Tempelkan dari `ItemDatabase` yang sudah ada di place.
- Daftar saddle darat ditambah Rex, Spino, Equus, Kaprosuchus, Terror Bird, Beelzebufo, Diplodocus, dan Arthropleura karena creature-nya ada di CreatureLibrary.
- Reinforced Wooden Door, Double Door, Window, Dinosaur Gate, dan Giant Trapdoor tercatat tier Stone.
