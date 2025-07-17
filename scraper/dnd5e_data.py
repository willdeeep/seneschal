"""Enhanced D&D 5e data for character creation."""

# Comprehensive list of D&D 5e proficiencies organized by type
DND5E_PROFICIENCIES = {
    'skills': [
        'Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception',
        'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine',
        'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion',
        'Sleight of Hand', 'Stealth', 'Survival'
    ],

    'armor': [
        'Light Armor', 'Medium Armor', 'Heavy Armor', 'Shields',
        'Padded Armor', 'Leather Armor', 'Studded Leather',
        'Hide Armor', 'Chain Shirt', 'Scale Mail', 'Breastplate', 'Half Plate',
        'Ring Mail', 'Chain Mail', 'Splint Armor', 'Plate Armor'
    ],

    'weapons': [
        'Simple Weapons', 'Martial Weapons',
        # Simple Melee Weapons
        'Club', 'Dagger', 'Dart', 'Handaxe', 'Javelin', 'Light Hammer',
        'Mace', 'Quarterstaff', 'Sickle', 'Spear',
        # Simple Ranged Weapons
        'Light Crossbow', 'Shortbow', 'Sling',
        # Martial Melee Weapons
        'Battleaxe', 'Flail', 'Glaive', 'Greataxe', 'Greatsword', 'Halberd',
        'Lance', 'Longsword', 'Maul', 'Morningstar', 'Pike', 'Rapier',
        'Scimitar', 'Shortsword', 'Trident', 'War Pick', 'Warhammer', 'Whip',
        # Martial Ranged Weapons
        'Blowgun', 'Hand Crossbow', 'Heavy Crossbow', 'Longbow', 'Net'
    ],

    'tools': [
        # Artisan's Tools
        "Alchemist's Supplies", "Brewer's Supplies", "Calligrapher's Supplies",
        "Carpenter's Tools", "Cartographer's Tools", "Cobbler's Tools",
        "Cook's Utensils", "Glassblower's Tools", "Jeweler's Tools",
        "Leatherworker's Tools", "Mason's Tools", "Painter's Supplies",
        "Potter's Tools", "Smith's Tools", "Tinker's Tools", "Weaver's Tools",
        "Woodcarver's Tools",
        
        # Gaming Sets
        'Dice Set', 'Dragonchess Set', 'Playing Card Set', 'Three-Dragon Ante Set',
        
        # Musical Instruments
        'Bagpipes', 'Drum', 'Dulcimer', 'Flute', 'Lute', 'Lyre',
        'Horn', 'Pan Flute', 'Shawm', 'Viol',
        
        # Other Tools
        "Disguise Kit", "Forgery Kit", "Herbalism Kit", "Navigator's Tools",
        "Poisoner's Kit", "Thieves' Tools", "Vehicles (Land)", "Vehicles (Water)"
    ],

    'languages': [
        # Standard Languages
        'Common', 'Dwarvish', 'Elvish', 'Giant', 'Gnomish', 'Goblin',
        'Halfling', 'Orc',
        
        # Exotic Languages
        'Abyssal', 'Celestial', 'Draconic', 'Deep Speech', 'Infernal',
        'Primordial', 'Sylvan', 'Undercommon',
        
        # Primordial Dialects
        'Aquan', 'Auran', 'Ignan', 'Terran'
    ]
}

# D&D 5e Features organized by source
DND5E_FEATURES = {
    'racial': [
        # Common Racial Features
        ('Darkvision', 'You can see in dim light within 60 feet as if it were bright light, and in darkness as if it were dim light.'),
        ('Fey Ancestry', 'You have advantage on saving throws against being charmed, and magic can\'t put you to sleep.'),
        ('Lucky', 'When you roll a 1 on an attack roll, ability check, or saving throw, you can reroll the die and must use the new roll.'),
        ('Brave', 'You have advantage on saving throws against being frightened.'),
        ('Halfling Nimbleness', 'You can move through the space of any creature that is of a size larger than yours.'),
        ('Stonecunning', 'You have proficiency with mason\'s tools and double your proficiency bonus on History checks related to stonework.'),
        ('Draconic Ancestry', 'You have draconic ancestry. Choose one type of dragon; this determines the damage and area of your breath weapon.'),
        ('Breath Weapon', 'You can use your action to exhale destructive energy determined by your draconic ancestry.'),
        ('Damage Resistance', 'You have resistance to the damage type associated with your draconic ancestry.'),
        ('Keen Senses', 'You have proficiency in the Perception skill.'),
        ('Trance', 'You don\'t need to sleep and can\'t be forced to sleep. Instead, you meditate deeply for 4 hours.'),
        ('Extra Language', 'You can speak, read, and write one extra language of your choice.'),
        ('Naturally Stealthy', 'You can attempt to hide even when you are obscured only by a creature that is at least one size larger than you.'),
        ('Gnome Cunning', 'You have advantage on Intelligence, Wisdom, and Charisma saving throws against magic.'),
        ('Tinker', 'You have proficiency with artisan\'s tools (tinker\'s tools) and can construct tiny clockwork devices.'),
        ('Relentless Endurance', 'When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead.'),
        ('Savage Attacks', 'When you score a critical hit with a melee weapon attack, you can roll one of the weapon\'s damage dice one additional time.'),
        ('Hellish Resistance', 'You have resistance to fire damage.'),
        ('Infernal Legacy', 'You know the thaumaturgy cantrip. Once you reach 3rd level, you can cast hellish rebuke once per day.'),
    ],

    'class': [
        # Barbarian
        ('Rage', 'In battle, you fight with primal ferocity. You have advantage on Strength checks and saving throws, bonus melee damage, and resistance to bludgeoning, piercing, and slashing damage.'),
        ('Unarmored Defense (Barbarian)', 'While not wearing armor, your AC equals 10 + Dex modifier + Con modifier.'),
        ('Reckless Attack', 'You can throw aside all concern for defense to attack with fierce desperation, gaining advantage on melee weapon attack rolls but giving attackers advantage against you.'),
        ('Danger Sense', 'You have advantage on Dexterity saving throws against effects you can see.'),
        
        # Bard
        ('Bardic Inspiration', 'You can inspire others through stirring words or music, giving them a d6 to add to one ability check, attack roll, or saving throw.'),
        ('Jack of All Trades', 'You can add half your proficiency bonus to any ability check that doesn\'t already include your proficiency bonus.'),
        ('Song of Rest', 'During a short rest, any creatures who hear your performance regain extra hit points.'),
        ('Magical Secrets', 'You learn additional spells from any class.'),
        
        # Cleric
        ('Channel Divinity', 'You gain the ability to channel divine energy directly from your deity.'),
        ('Destroy Undead', 'When an undead fails its saving throw against your Turn Undead feature, the creature is instantly destroyed.'),
        ('Divine Intervention', 'You can call on your deity to intervene on your behalf when your need is great.'),
        
        # Druid
        ('Wild Shape', 'You can use your action to magically assume the shape of a beast that you have seen before.'),
        ('Natural Recovery', 'During a short rest, you can recover some of your magical energy.'),
        ('Timeless Body', 'The primal magic that you wield causes you to age more slowly.'),
        
        # Fighter
        ('Fighting Style', 'You adopt a particular style of fighting as your specialty.'),
        ('Second Wind', 'You have a limited well of stamina that you can draw on to protect yourself from harm.'),
        ('Action Surge', 'You can push yourself beyond your normal limits for a moment.'),
        ('Extra Attack', 'You can attack twice, instead of once, whenever you take the Attack action on your turn.'),
        ('Indomitable', 'You can reroll a saving throw that you fail.'),
        
        # Monk
        ('Martial Arts', 'You gain benefits while unarmed or wielding only monk weapons and aren\'t wearing armor or wielding a shield.'),
        ('Ki', 'Your training allows you to harness the mystic energy of ki.'),
        ('Unarmored Defense (Monk)', 'While not wearing armor or wielding a shield, your AC equals 10 + Dex modifier + Wis modifier.'),
        ('Deflect Missiles', 'You can use your reaction to deflect or catch missiles when hit by a ranged weapon attack.'),
        ('Slow Fall', 'You can use your reaction when you fall to reduce any falling damage you take.'),
        ('Stunning Strike', 'You can interfere with the flow of ki in an opponent\'s body.'),
        
        # Paladin
        ('Divine Sense', 'The presence of strong evil registers on your senses like a noxious odor.'),
        ('Lay on Hands', 'Your blessed touch can heal wounds.'),
        ('Divine Smite', 'When you hit a creature with a melee weapon attack, you can expend one spell slot to deal radiant damage.'),
        ('Aura of Protection', 'You and friendly creatures within 10 feet gain a bonus to saving throws equal to your Charisma modifier.'),
        
        # Ranger
        ('Favored Enemy', 'You have studied, tracked, and learned to effectively fight a specific type of creature.'),
        ('Natural Explorer', 'You are particularly familiar with one type of natural environment.'),
        ('Hunter\'s Mark', 'You can mark a creature as your quarry.'),
        ('Primeval Awareness', 'You can use your action to focus your awareness on the region around you.'),
        
        # Rogue
        ('Expertise', 'Choose two of your skill proficiencies. Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies.'),
        ('Sneak Attack', 'You know how to strike subtly and exploit a foe\'s distraction.'),
        ('Thieves\' Cant', 'You know thieves\' cant, a secret mix of dialect, jargon, and code.'),
        ('Cunning Action', 'You can take a Dash, Disengage, or Hide action as a bonus action.'),
        ('Uncanny Dodge', 'When an attacker that you can see hits you with an attack, you can use your reaction to halve the attack\'s damage.'),
        ('Evasion', 'When you are subjected to an effect that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed.'),
        
        # Sorcerer
        ('Sorcerous Origin', 'Choose a sorcerous origin, which describes the source of your innate magical power.'),
        ('Font of Magic', 'You tap into a deep wellspring of magic within yourself.'),
        ('Metamagic', 'You gain the ability to twist your spells to suit your needs.'),
        
        # Warlock
        ('Otherworldly Patron', 'You have struck a pact with an otherworldly being.'),
        ('Pact Magic', 'Your arcane research and magic bestowed by your patron have given you facility with spells.'),
        ('Eldritch Invocations', 'You learn occult secrets called eldritch invocations.'),
        ('Pact Boon', 'Your otherworldly patron bestows a gift upon you for your loyal service.'),
        
        # Wizard
        ('Spellcasting', 'You have learned to untangle and reshape the fabric of reality in harmony with your wishes and music.'),
        ('Ritual Casting', 'You can cast a spell as a ritual if that spell has the ritual tag and you have the spell in your spellbook.'),
        ('Arcane Recovery', 'You have learned to regain some of your magical energy by studying your spellbook.'),
        ('Arcane Tradition', 'You choose an arcane tradition, shaping your practice of magic.'),
    ],

    'background': [
        ('Feature: Discovery', 'The quiet seclusion of your extended hermitage gave you access to a unique and powerful discovery.'),
        ('Feature: Shelter of the Faithful', 'You and your companions can expect to receive free healing and care at a temple, shrine, or other established presence of your faith.'),
        ('Feature: Guild Membership', 'As an established and respected member of a guild, you can rely on certain benefits.'),
        ('Feature: Position of Privilege', 'Thanks to your noble birth, people are inclined to think the best of you.'),
        ('Feature: Ship\'s Passage', 'When you need to, you can secure free passage on a sailing ship for yourself and your companions.'),
        ('Feature: Safe Haven', 'You have a reliable and trustworthy contact who acts as your liaison to a network of other criminals.'),
        ('Feature: Wanderer', 'You have an excellent memory for maps and geography, and you can always recall the general layout of terrain.'),
        ('Feature: Military Rank', 'You have a military rank from your career as a soldier.'),
    ]
}

# Enhanced equipment list with better categorization
DND5E_EQUIPMENT = {
    'weapons': [
        # Simple Melee Weapons
        ('Club', 'weapon', 1, 2.0, 'A simple wooden club.'),
        ('Dagger', 'weapon', 2, 1.0, 'A sharp knife, ideal for close combat or throwing.'),
        ('Dart', 'weapon', 5, 0.25, 'A small throwing weapon.'),
        ('Handaxe', 'weapon', 5, 2.0, 'A light axe designed for one-handed use.'),
        ('Javelin', 'weapon', 5, 2.0, 'A light spear designed for throwing.'),
        ('Light Hammer', 'weapon', 2, 2.0, 'A small hammer that can be thrown.'),
        ('Mace', 'weapon', 5, 4.0, 'A heavy club with a metal head.'),
        ('Quarterstaff', 'weapon', 2, 4.0, 'A simple staff weapon.'),
        ('Sickle', 'weapon', 1, 2.0, 'A farming tool adapted for combat.'),
        ('Spear', 'weapon', 1, 3.0, 'A long thrusting weapon.'),
        
        # Simple Ranged Weapons
        ('Light Crossbow', 'weapon', 25, 5.0, 'A light mechanical bow.'),
        ('Shortbow', 'weapon', 25, 2.0, 'A short bow for hunting and combat.'),
        ('Sling', 'weapon', 1, 0.0, 'A simple projectile weapon.'),
        
        # Martial Melee Weapons
        ('Battleaxe', 'weapon', 10, 4.0, 'A versatile axe for battle.'),
        ('Flail', 'weapon', 10, 2.0, 'A weapon with a hinged striking head.'),
        ('Glaive', 'weapon', 20, 6.0, 'A pole weapon with a blade.'),
        ('Greataxe', 'weapon', 30, 7.0, 'A large two-handed axe.'),
        ('Greatsword', 'weapon', 50, 6.0, 'A large two-handed sword.'),
        ('Halberd', 'weapon', 20, 6.0, 'A pole weapon with axe and spear points.'),
        ('Lance', 'weapon', 10, 6.0, 'A long cavalry weapon.'),
        ('Longsword', 'weapon', 15, 3.0, 'A versatile straight sword.'),
        ('Maul', 'weapon', 10, 10.0, 'A heavy two-handed hammer.'),
        ('Morningstar', 'weapon', 15, 4.0, 'A club with a spiked head.'),
        ('Pike', 'weapon', 5, 18.0, 'A very long spear.'),
        ('Rapier', 'weapon', 25, 2.0, 'A light thrusting sword.'),
        ('Scimitar', 'weapon', 25, 3.0, 'A curved light sword.'),
        ('Shortsword', 'weapon', 10, 2.0, 'A short straight sword.'),
        ('Trident', 'weapon', 5, 4.0, 'A three-pronged spear.'),
        ('War Pick', 'weapon', 5, 2.0, 'A pick designed for combat.'),
        ('Warhammer', 'weapon', 15, 2.0, 'A hammer designed for war.'),
        ('Whip', 'weapon', 2, 3.0, 'A flexible striking weapon.'),
        
        # Martial Ranged Weapons
        ('Blowgun', 'weapon', 10, 1.0, 'A tube for shooting darts.'),
        ('Hand Crossbow', 'weapon', 75, 3.0, 'A small one-handed crossbow.'),
        ('Heavy Crossbow', 'weapon', 50, 18.0, 'A large powerful crossbow.'),
        ('Longbow', 'weapon', 50, 2.0, 'A tall bow for long-range combat.'),
        ('Net', 'weapon', 5, 3.0, 'A weighted net for entangling foes.'),
    ],

    'armor': [
        # Light Armor
        ('Padded Armor', 'armor', 5, 8.0, 'Simple quilted cloth armor.'),
        ('Leather Armor', 'armor', 10, 10.0, 'Supple leather armor.'),
        ('Studded Leather', 'armor', 45, 13.0, 'Leather armor with metal studs.'),
        
        # Medium Armor
        ('Hide Armor', 'armor', 10, 12.0, 'Crude leather made from thick hides.'),
        ('Chain Shirt', 'armor', 50, 20.0, 'A shirt made of interlocking rings.'),
        ('Scale Mail', 'armor', 50, 45.0, 'A coat and leggings of leather covered with overlapping pieces of metal.'),
        ('Breastplate', 'armor', 400, 20.0, 'A fitted metal chest piece.'),
        ('Half Plate', 'armor', 750, 40.0, 'Partial plate armor.'),
        
        # Heavy Armor
        ('Ring Mail', 'armor', 30, 40.0, 'Leather armor with heavy rings sewn into it.'),
        ('Chain Mail', 'armor', 75, 55.0, 'Interlocking metal rings.'),
        ('Splint Armor', 'armor', 200, 60.0, 'Strips of metal riveted to leather.'),
        ('Plate Armor', 'armor', 1500, 65.0, 'Interlocking metal plates.'),
        
        # Shields
        ('Shield', 'armor', 10, 6.0, 'A shield grants +2 AC.'),
    ],

    'adventuring_gear': [
        ('Backpack', 'gear', 2, 5.0, 'A leather pack with straps for carrying gear.'),
        ('Bedroll', 'gear', 1, 7.0, 'A sleeping bag and blanket.'),
        ('Blanket', 'gear', 5, 3.0, 'A wool blanket.'),
        ('Rope (50 feet)', 'gear', 2, 10.0, 'Hempen rope.'),
        ('Torch', 'gear', 1, 1.0, 'A torch burns for 1 hour, providing bright light in a 20-foot radius.'),
        ('Rations (1 day)', 'consumable', 2, 2.0, 'Dry foods suitable for extended travel.'),
        ('Waterskin', 'gear', 2, 5.0, 'A waterskin holds 4 pints of liquid.'),
        ('Lantern', 'gear', 5, 2.0, 'A hooded lantern casts bright light in a 30-foot radius.'),
        ('Oil (flask)', 'consumable', 1, 1.0, 'Oil usually comes in a clay flask that holds 1 pint.'),
        ('Tinderbox', 'gear', 5, 1.0, 'A small container holding flint, fire steel, and tinder.'),
        ('Crowbar', 'gear', 2, 5.0, 'A flat metal bar for prying.'),
        ('Hammer', 'gear', 1, 3.0, 'A tool hammer.'),
        ('Piton', 'gear', 5, 0.25, 'A metal spike for climbing.'),
        ('Grappling Hook', 'gear', 2, 4.0, 'A hook attached to a rope for climbing.'),
        ('Chain (10 feet)', 'gear', 5, 10.0, 'A chain has 10 hit points.'),
        ('Manacles', 'gear', 2, 6.0, 'These metal restraints can bind a creature.'),
        ('Mirror, steel', 'gear', 5, 0.5, 'A polished steel mirror.'),
        ('Pole (10-foot)', 'gear', 5, 7.0, 'A simple wooden pole.'),
        ('Tent, two-person', 'gear', 2, 20.0, 'A simple and portable canvas shelter.'),
        
        # Tools
        ('Thieves\' Tools', 'tool', 25, 1.0, 'This set includes a small file, lock picks, a small mirror, and narrow-bladed scissors.'),
        ('Healer\'s Kit', 'tool', 5, 3.0, 'This kit has ten uses and can stabilize dying creatures.'),
        ('Disguise Kit', 'tool', 25, 3.0, 'This pouch contains cosmetics, hair dye, and small props.'),
        ('Forgery Kit', 'tool', 15, 5.0, 'This small box contains paper, inks, and other supplies.'),
        ('Herbalism Kit', 'tool', 5, 3.0, 'This kit contains pouches to store herbs and tools to harvest them.'),
        ('Poisoner\'s Kit', 'tool', 50, 2.0, 'This kit includes vials, chemicals, and other equipment.'),
        
        # Consumables
        ('Potion of Healing', 'consumable', 50, 0.5, 'A character who drinks this magical red fluid regains 2d4 + 2 hit points.'),
        ('Antitoxin', 'consumable', 50, 0.0, 'A creature that drinks this vial has advantage on saving throws against poison for 1 hour.'),
        ('Holy Water', 'consumable', 25, 1.0, 'As an action, you can splash this flask on a creature within 5 feet or throw it up to 20 feet.'),
        ('Acid (vial)', 'consumable', 25, 1.0, 'As an action, you can splash this acid on a creature within 5 feet.'),
        ('Alchemist\'s Fire', 'consumable', 50, 1.0, 'This sticky, adhesive fluid ignites when exposed to air.'),
    ]
}
