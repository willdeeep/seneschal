"""
Spell and spell slot models.

This module contains models for D&D spells and spell slot tracking including
the Spell model for spell definitions and SpellSlot for character spell slot management.
"""

from project import db


class Spell(db.Model):
    """Model for D&D spells."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer, nullable=False)  # 0-9, where 0 is cantrips
    # "evocation", "illusion", etc.
    school = db.Column(db.String(30), nullable=False)

    # Casting details
    # "1 action", "1 bonus action", "10 minutes"
    casting_time = db.Column(db.String(50), nullable=True)
    # "60 feet", "Touch", "Self"
    spell_range = db.Column(db.String(50), nullable=True)
    # "V, S, M (a tiny bell)"
    components = db.Column(db.String(100), nullable=True)
    # "Instantaneous", "Concentration, up to 1 hour"
    duration = db.Column(db.String(50), nullable=True)

    # Spell description and mechanics
    description = db.Column(db.Text, nullable=False)
    # Description of casting at higher levels
    higher_level = db.Column(db.Text, nullable=True)

    # Spell lists (which classes can learn this spell)
    # Comma-separated: "wizard,sorcerer,bard"
    class_lists = db.Column(db.Text, nullable=True)

    # Source and references
    source = db.Column(db.String(50), nullable=True)  # "PHB", "XGE", etc.

    # Ritual and concentration
    is_ritual = db.Column(db.Boolean, default=False, nullable=False)
    requires_concentration = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Spell {self.name} (Level {self.level})>"


class SpellSlot(db.Model):
    """Model for tracking character spell slots."""

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    level = db.Column(db.Integer, nullable=False)  # Spell slot level (1-9)
    # Total slots available
    total_slots = db.Column(db.Integer, nullable=False)
    used_slots = db.Column(
        db.Integer, default=0, nullable=False
    )  # Slots currently used

    @property
    def remaining_slots(self):
        """Calculate remaining spell slots."""
        return max(0, self.total_slots - self.used_slots)

    def use_slot(self):
        """Use one spell slot if available."""
        if self.used_slots < self.total_slots:
            self.used_slots += 1
            return True
        return False

    def restore_slot(self):
        """Restore one spell slot if any are used."""
        if self.used_slots > 0:
            self.used_slots -= 1
            return True
        return False

    def long_rest(self):
        """Restore all spell slots after a long rest."""
        self.used_slots = 0

    def __repr__(self):
        return (
            f"<SpellSlot Level {self.level}: {self.remaining_slots}/{self.total_slots}>"
        )
