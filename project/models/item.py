"""
Item and inventory-related models.

This module contains models for equipment, inventory items, and character-item
associations including Item, CharacterItem for inventory management.
"""

from project import db


class Item(db.Model):
    """Model for equipment and inventory items."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # 'weapon', 'armor', 'tool', 'consumable', etc.
    item_type = db.Column(db.String(50), nullable=False)
    cost_gp = db.Column(db.Integer, default=0, nullable=False)
    weight_lbs = db.Column(db.Float, default=0.0, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Weapon-specific properties
    damage_dice = db.Column(db.String(20), nullable=True)  # e.g., "1d8", "2d6"
    # "slashing", "piercing", "bludgeoning", etc.
    damage_type = db.Column(db.String(30), nullable=True)
    # "melee", "ranged", "5/10" for thrown
    weapon_range = db.Column(db.String(50), nullable=True)
    # "finesse, light, versatile" etc.
    weapon_properties = db.Column(db.Text, nullable=True)
    # For versatile weapons like longsword
    versatile_damage = db.Column(db.String(20), nullable=True)

    # Armor-specific properties
    armor_class = db.Column(db.Integer, nullable=True)  # Base AC for armor
    # Max Dex bonus for medium armor
    max_dex_bonus = db.Column(db.Integer, nullable=True)
    # Minimum strength requirement
    min_strength = db.Column(db.Integer, nullable=True)
    stealth_disadvantage = db.Column(db.Boolean, default=False, nullable=False)

    # Magic item properties
    is_magical = db.Column(db.Boolean, default=False, nullable=False)
    # "common", "uncommon", "rare", "very rare", "legendary"
    rarity = db.Column(db.String(20), nullable=True)
    requires_attunement = db.Column(db.Boolean, default=False, nullable=False)
    # For items with limited uses
    charges = db.Column(db.Integer, nullable=True)

    # General properties
    # Can multiple be in one inventory slot
    stackable = db.Column(db.Boolean, default=True, nullable=False)
    consumable = db.Column(
        db.Boolean, default=False, nullable=False
    )  # Gets used up when used

    def __repr__(self):
        return f"<Item {self.name}>"


class CharacterItem(db.Model):
    """Association model for character inventory with quantity and equipment details."""

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    equipped = db.Column(db.Boolean, default=False, nullable=False)

    # Equipment slot tracking for armor and accessories
    # "main_hand", "off_hand", "armor", "helmet", etc.
    equipment_slot = db.Column(db.String(30), nullable=True)

    # Condition and customization
    # "broken", "damaged", "good", "excellent"
    condition = db.Column(db.String(20), default="good", nullable=False)
    # Custom notes about this specific item
    notes = db.Column(db.Text, nullable=True)

    # Attunement tracking for magic items
    attuned = db.Column(db.Boolean, default=False, nullable=False)

    # Charges tracking for items with limited uses
    current_charges = db.Column(db.Integer, nullable=True)

    # Relationships
    item = db.relationship("Item", backref="character_items")

    def __repr__(self):
        return f'<CharacterItem {self.quantity}x {self.item.name if self.item else "Unknown"}>'
