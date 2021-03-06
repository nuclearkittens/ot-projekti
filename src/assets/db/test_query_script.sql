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
INSERT INTO Items (id, name, descr) VALUES ("test_item1", "Test Item 1", "test item 1: set amount hp/mp heal");
INSERT INTO Items (id, name, descr) VALUES ("test_item2", "Test Item 2", "test item 2: percentage hp/mp heal");
INSERT INTO Items (id, name, descr) VALUES ("test_item3", "Test Item 3", "test item 3: no healing");
INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("hp20", "hp", "heal", 20);
INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("mp5", "mp", "heal", 5);
INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("hp25pc", "hp", "heal", 0.25);
INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("mp10pc", "mp", "heal", 0.1);
INSERT INTO Effects (id, target_attr, effect, amount) VALUES ("other", "other", "other", 0);
INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item1", "hp20");
INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item2", "hp25pc");
INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item1", "mp5");
INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item2", "mp10pc");
INSERT INTO ItemEffects (item_id, effect_id) VALUES ("test_item3", "other");
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ("test_skill", "skills", "physical", "Test Skill", "A skill for testing", "physical", 2, 0, 1.0, 1.0);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ("test_magic", "magic", "blk", "Test Spell", "A skill for testing", "fire", 1, 5, 1.2, 0.5);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ("test_other", "other", "other", "Unspecified Skill", "A skill for testing", "dark", 0, 0, 0.0, 0.0);
INSERT INTO Skills (id, category, subcategory, name, descr, element, hits, mp_cost, multiplier, crit_rate) VALUES ('attack', 'skills', 'physical', 'Attack', 'Physical damage to a single target', 'physical', 1, 0, 1.0, 0.1);
INSERT INTO Stats (char_id, hp, mp, atk, defs, mag, mdef, agi) VALUES ("bob", 100, 10, 10, 10, 5, 5, 20);
INSERT INTO Resistance (char_id, physical, fire, ice, lightning, wind, light, dark) VALUES ("bob", 1.0, 0.0, 1.5, 1.0, 1.0, 0.5, -1.0);
INSERT INTO CharSkills (char_id, skill_id) VALUES ("bob", "test_skill");
INSERT INTO CharSkills (char_id, skill_id) VALUES ("bob", "test_magic");
INSERT INTO CharSkills (char_id, skill_id) VALUES ("bob", "attack");
INSERT INTO Monsters (id, name, category, lvl, descr) VALUES ("bob", "Bob", "undead", 1, "Bob the test monster");
INSERT INTO Party (id, name, lvl) VALUES ("bob", "Bob", 1);
INSERT INTO Inventory (char_id, item_id, qty) VALUES ("bob", "test_item1", 1)

