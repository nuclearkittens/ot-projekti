CREATE TABLE Items (id TEXT PRIMARY KEY, name TEXT, descr TEXT);
CREATE TABLE Skills (id TEXT PRIMARY KEY, category TEXT, subcategory TEXT, name TEXT, descr TEXT, element TEXT, hits INTEGER, mp_cost INTEGER, multiplier REAL, crit_rate REAL);
CREATE TABLE Effects (id TEXT PRIMARY KEY, target_attr TEXT, effect TEXT, amount NUMERIC);
CREATE TABLE ItemEffects (item_id TEXT, effect_id TEXT);
CREATE TABLE SkillEffects (skill_id TEXT, effect_id TEXT);
CREATE TABLE Monsters (id TEXT PRIMARY KEY, name TEXT, category TEXT, lvl INTEGER, descr TEXT);
CREATE TABLE Party (id TEXT PRIMARY KEY, name TEXT, lvl INTEGER);
CREATE TABLE Stats (char_id TEXT PRIMARY KEY, hp INTEGER, mp INTEGER, atk INTEGER, defs INTEGER, mag INTEGER, mdef INTEGER, agi INTEGER);
CREATE TABLE Resistance (char_id TEXT PRIMARY KEY, physical REAL, fire REAL, ice REAL, lightning REAL, wind REAL, light REAL, dark REAL);
CREATE TABLE CharSkills (char_id TEXT, skill_id TEXT);
CREATE TABLE Loot (monster_id TEXT PRIMARY KEY, money INTEGER, item_id TEXT, qty INTEGER);
CREATE TABLE Inventory (char_id TEXT, item_id TEXT, qty INTEGER);
INSERT INTO Items (id, name, descr) VALUES ('potion', 'Potion', 'Restores 20 HP to one character');
INSERT INTO Items (id, name, descr) VALUES ('coffee', 'Coffee', 'Restores 5 MP to one character');
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ('attack', 'skills', 'physical', 'Attack', 'Deals physical damage to a single target', 'physical', 1, 0, 1.0, 0.1);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ('kick', 'skills', 'physical', 'Kick', 'Kick a single target', 'physical', 1, 0, 1.0, 0.1);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ('dbl_claw', 'skills', 'physical', 'Double Claw', 'Deals two hits to a single target', 'physical', 2, 2, 0.7, 0.05);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ('fire', 'magic', 'blk', 'Fire', 'Deal weak fire-elemental damage to a single target', 'fire', 1, 4, 1.0, 0.1);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ('ice', 'magic', 'blk', 'Ice', 'Deal weak ice-elemental damage to a single target', 'ice', 1, 4, 1.0, 0.1);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ('thunder', 'magic', 'blk', 'Thunder', 'Deal weak lightning-elemental damage to a single target', 'lightning', 1, 4, 1.0, 0.1);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ('wind', 'magic', 'blk', 'Wind', 'Deal weak wind-elemental damage to a single target', 'wind', 1, 4, 1.0, 0.1);
INSERT INTO Effects (id, target_attr, effect, amount) VALUES ('hp20', 'hp', 'heal', 20);
INSERT INTO Effects (id, target_attr, effect, amount) VALUES ('mp5', 'mp', 'heal', 5);
INSERT INTO ItemEffects (item_id, effect_id) VALUES ('potion', 'hp20');
INSERT INTO ItemEffects (item_id, effect_id) VALUES ('coffee', 'mp5');
INSERT INTO Monsters (id, name, category, lvl, descr) VALUES ('ikorni', 'Ikorni', 'normal', 1, 'A squirrel with human feet, mostly found near parks and forests. Watch out for its claws.');
INSERT INTO Party (id, name, lvl) VALUES ('party', 'Party', 1);
INSERT INTO Party (id, name, lvl) VALUES ('ej', 'EJ', 1);
INSERT INTO Party (id, name, lvl) VALUES ('witch', 'The Witch', 1);
INSERT INTO Stats (char_id, hp, mp, atk, defs, mag, mdef, agi) VALUES ('ikorni', 40, 10, 12, 1, 1, 20, 8);
INSERT INTO Stats (char_id, hp, mp, atk, defs, mag, mdef, agi) VALUES ('ej', 60, 10, 14, 10, 5, 5, 7);
INSERT INTO Stats (char_id, hp, mp, atk, defs, mag, mdef, agi) VALUES ('witch', 36, 20, 7, 8, 15, 8, 10);
INSERT INTO Resistance (char_id, physical, fire, ice, lightning, wind, light, dark) VALUES ('ikorni', 1.0, 1.5, 1.0, 1.0, 0.5, 1.0, 0.5);
INSERT INTO Resistance (char_id, physical, fire, ice, lightning, wind, light, dark) VALUES ('ej', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0);
INSERT INTO Resistance (char_id, physical, fire, ice, lightning, wind, light, dark) VALUES ('witch', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0);
INSERT INTO CharSkills (char_id, skill_id) VALUES ('ikorni', 'kick');
INSERT INTO CharSkills (char_id, skill_id) VALUES ('ikorni', 'dbl_claw');
INSERT INTO CharSkills (char_id, skill_id) VALUES ('ej', 'attack');
INSERT INTO CharSkills (char_id, skill_id) VALUES ('witch', 'attack');
INSERT INTO CharSkills (char_id, skill_id) VALUES ('witch', 'fire');
INSERT INTO CharSkills (char_id, skill_id) VALUES ('witch', 'ice');
INSERT INTO CharSkills (char_id, skill_id) VALUES ('witch', 'thunder');
INSERT INTO CharSkills (char_id, skill_id) VALUES ('witch', 'wind');
INSERT INTO Loot (monster_id, money) VALUES ('ikorni', 15);
INSERT INTO Inventory (char_id, item_id, qty) VALUES ('ikorni', 'potion', 1);
INSERT INTO Inventory (char_id, item_id, qty) VALUES ('party', 'potion', 3);
INSERT INTO Inventory (char_id, item_id, qty) VALUES ('party', 'coffee', 1);






