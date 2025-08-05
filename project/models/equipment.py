"""Equipment model for D&D 5e items and gear."""

from project import db


class Equipment(db.Model):
    """D&D 5e equipment and items model."""

    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Weapon, Armor, Tool, etc.

    # Basic properties
    cost_cp = db.Column(db.Integer, default=0)  # Cost in copper pieces
    weight = db.Column(db.Float, default=0.0)   # Weight in pounds
    description = db.Column(db.Text)

    # Weapon properties
    damage_dice = db.Column(db.String(20))      # e.g., "1d8"
    damage_type = db.Column(db.String(20))      # Piercing, Slashing, etc.
    weapon_properties = db.Column(db.JSON, default=list)  # Finesse, Light, etc.

    # Armor properties
    armor_class = db.Column(db.Integer)         # Base AC
    max_dex_bonus = db.Column(db.Integer)       # Max Dex modifier
    min_strength = db.Column(db.Integer, default=0)  # Strength requirement
    stealth_disadvantage = db.Column(db.Boolean, default=False)

    # Magic item properties
    rarity = db.Column(db.String(20), default='Common')  # Common, Uncommon, etc.
    requires_attunement = db.Column(db.Boolean, default=False)
    magic_bonus = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Equipment {self.name}>'

    @classmethod
    def get_starting_equipment_for_class(cls, character_class_name):
        """Get typical starting equipment for a character class."""
        equipment_sets = {
            'Fighter': [
                'Chain Mail', 'Shield', 'Longsword', 'Handaxe', 'Light Crossbow',
                'Explorer\'s Pack', 'Leather Armor'
            ],
            'Wizard': [
                'Dagger', 'Component Pouch', 'Scholar\'s Pack', 'Spellbook',
                'Quarterstaff', 'Light Crossbow'
            ],
            'Rogue': [
                'Rapier', 'Shortbow', 'Thieves\' Tools', 'Leather Armor',
                'Burglar\'s Pack', 'Dagger'
            ],
            'Cleric': [
                'Scale Mail', 'Shield', 'Mace', 'Light Crossbow',
                'Priest\'s Pack', 'Chain Mail'
            ]
        }

        equipment_names = equipment_sets.get(character_class_name, [])
        return cls.query.filter(cls.name.in_(equipment_names)).all()


class CharacterEquipment(db.Model):
    """Junction table for character equipment with quantities."""

    __tablename__ = 'character_equipment'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    equipped = db.Column(db.Boolean, default=False)
    attuned = db.Column(db.Boolean, default=False)

    # Relationships
    character = db.relationship('Character', backref='equipment_items')
    equipment = db.relationship('Equipment', backref='character_items')

    def __repr__(self):
        return f'<CharacterEquipment {self.character_id}:{self.equipment_id}>'
