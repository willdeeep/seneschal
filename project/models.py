from project import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Association tables for many-to-many relationships
character_proficiencies = db.Table('character_proficiencies',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True),
    db.Column('proficiency_id', db.Integer, db.ForeignKey('proficiency.id'), primary_key=True)
)

character_languages = db.Table('character_languages',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True)
)

character_features = db.Table('character_features',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True),
    db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'), primary_key=True)
)

character_spells = db.Table('character_spells',
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True),
    db.Column('spell_id', db.Integer, db.ForeignKey('spell.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    """User model for authentication and user management."""
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationship to characters
    characters = db.relationship('Character', backref='owner', lazy=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Character(db.Model):
    """Character model for D&D character sheets."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    player_name = db.Column(db.String(100), nullable=True)
    race = db.Column(db.String(50), nullable=False)
    subrace = db.Column(db.String(50), nullable=True)  # For variant races
    character_class = db.Column(db.String(50), nullable=False)
    subclass = db.Column(db.String(50), nullable=True)  # Archetype/subclass
    level = db.Column(db.Integer, default=1, nullable=False)
    background = db.Column(db.String(100), nullable=True)
    alignment = db.Column(db.String(30), nullable=True)  # e.g., "Chaotic Good"
    
    # Experience and advancement
    experience_points = db.Column(db.Integer, default=0, nullable=False)
    proficiency_bonus = db.Column(db.Integer, default=2, nullable=False)  # Calculated from level
    
    # Core stats
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    
    # Saving throws (track proficiencies)
    str_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    dex_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    con_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    int_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    wis_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    cha_save_proficient = db.Column(db.Boolean, default=False, nullable=False)
    
    # Combat stats
    current_hp = db.Column(db.Integer, nullable=True)
    max_hp = db.Column(db.Integer, nullable=True)
    temp_hp = db.Column(db.Integer, default=0, nullable=False)  # Temporary hit points
    hit_dice = db.Column(db.String(20), nullable=True)  # e.g., "3d8" for level 3 fighter
    armor_class = db.Column(db.Integer, nullable=True)
    initiative = db.Column(db.Integer, nullable=True)
    speed = db.Column(db.Integer, default=30, nullable=False)
    
    # Death saves
    death_save_successes = db.Column(db.Integer, default=0, nullable=False)
    death_save_failures = db.Column(db.Integer, default=0, nullable=False)
    
    # Resources and currencies
    gold_pieces = db.Column(db.Integer, default=0, nullable=False)
    silver_pieces = db.Column(db.Integer, default=0, nullable=False)
    copper_pieces = db.Column(db.Integer, default=0, nullable=False)
    platinum_pieces = db.Column(db.Integer, default=0, nullable=False)
    electrum_pieces = db.Column(db.Integer, default=0, nullable=False)
    
    # Character details and roleplay
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.String(20), nullable=True)  # e.g., "5'8\""
    weight = db.Column(db.String(20), nullable=True)  # e.g., "150 lbs"
    eyes = db.Column(db.String(30), nullable=True)
    skin = db.Column(db.String(30), nullable=True)
    hair = db.Column(db.String(30), nullable=True)
    personality_traits = db.Column(db.Text, nullable=True)
    ideals = db.Column(db.Text, nullable=True)
    bonds = db.Column(db.Text, nullable=True)
    flaws = db.Column(db.Text, nullable=True)
    backstory = db.Column(db.Text, nullable=True)
    
    # Extended backstory fields
    why_adventuring = db.Column(db.Text, nullable=True)  # Why is your character adventuring?
    motivation = db.Column(db.Text, nullable=True)  # What motivates your character? (comma-separated)
    origin = db.Column(db.Text, nullable=True)  # Where did your character grow up?
    class_origin = db.Column(db.Text, nullable=True)  # Why is your character their current class?
    attachments = db.Column(db.Text, nullable=True)  # Special attachments to people, places, things
    secret = db.Column(db.Text, nullable=True)  # Does your character have a secret?
    attitude_origin = db.Column(db.Text, nullable=True)  # What is your character like and why?
    
    # Additional notes and tracking
    other_proficiencies = db.Column(db.Text, nullable=True)  # Any special proficiencies
    attacks_spellcasting = db.Column(db.Text, nullable=True)  # Attack descriptions
    features_traits = db.Column(db.Text, nullable=True)  # Additional features not in features table
    
    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Many-to-many relationships
    proficiencies = db.relationship('Proficiency', secondary=character_proficiencies, lazy='subquery',
                                  backref=db.backref('characters', lazy=True))
    languages = db.relationship('Language', secondary=character_languages, lazy='subquery',
                              backref=db.backref('characters', lazy=True))
    features = db.relationship('Feature', secondary=character_features, lazy='subquery',
                             backref=db.backref('characters', lazy=True))
    spells = db.relationship('Spell', secondary=character_spells, lazy='subquery',
                           backref=db.backref('characters', lazy=True))
    
    # One-to-many relationship with inventory
    inventory = db.relationship('CharacterItem', backref='character', lazy=True, cascade='all, delete-orphan')
    
    # One-to-many relationship with spell slots
    spell_slots = db.relationship('SpellSlot', backref='character', lazy=True, cascade='all, delete-orphan')

    def get_ability_modifier(self, score):
        """Calculate ability modifier from ability score."""
        return (score - 10) // 2
    
    def get_saving_throw_bonus(self, ability):
        """Calculate saving throw bonus for a given ability."""
        base_modifier = self.get_ability_modifier(getattr(self, ability))
        proficiency_map = {
            'strength': self.str_save_proficient,
            'dexterity': self.dex_save_proficient,
            'constitution': self.con_save_proficient,
            'intelligence': self.int_save_proficient,
            'wisdom': self.wis_save_proficient,
            'charisma': self.cha_save_proficient
        }
        
        if proficiency_map.get(ability, False):
            return base_modifier + self.proficiency_bonus
        return base_modifier
    
    def update_proficiency_bonus(self):
        """Update proficiency bonus based on character level."""
        if self.level >= 17:
            self.proficiency_bonus = 6
        elif self.level >= 13:
            self.proficiency_bonus = 5
        elif self.level >= 9:
            self.proficiency_bonus = 4
        elif self.level >= 5:
            self.proficiency_bonus = 3
        else:
            self.proficiency_bonus = 2

    def __repr__(self):
        return f'<Character {self.name}>'


class Proficiency(db.Model):
    """Model for character proficiencies (skills, weapons, tools, etc.)."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    proficiency_type = db.Column(db.String(50), nullable=False)  # 'skill', 'weapon', 'tool', 'armor', etc.
    description = db.Column(db.Text, nullable=True)
    associated_ability = db.Column(db.String(20), nullable=True)  # For skills: 'strength', 'dexterity', etc.
    
    def __repr__(self):
        return f'<Proficiency {self.name}>'


class Language(db.Model):
    """Model for character languages."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    language_type = db.Column(db.String(50), nullable=True)  # 'Standard', 'Exotic', 'Dialect'
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Language {self.name}>'


class Item(db.Model):
    """Model for equipment and inventory items."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)  # 'weapon', 'armor', 'tool', 'consumable', etc.
    cost_gp = db.Column(db.Integer, default=0, nullable=False)
    weight_lbs = db.Column(db.Float, default=0.0, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Weapon-specific properties
    damage_dice = db.Column(db.String(20), nullable=True)  # e.g., "1d8", "2d6"
    damage_type = db.Column(db.String(30), nullable=True)  # "slashing", "piercing", "bludgeoning", etc.
    weapon_range = db.Column(db.String(50), nullable=True)  # "melee", "ranged", "5/10" for thrown
    weapon_properties = db.Column(db.Text, nullable=True)  # "finesse, light, versatile" etc.
    versatile_damage = db.Column(db.String(20), nullable=True)  # For versatile weapons like longsword
    
    # Armor-specific properties
    armor_class = db.Column(db.Integer, nullable=True)  # Base AC for armor
    max_dex_bonus = db.Column(db.Integer, nullable=True)  # Max Dex bonus for medium armor
    min_strength = db.Column(db.Integer, nullable=True)  # Minimum strength requirement
    stealth_disadvantage = db.Column(db.Boolean, default=False, nullable=False)
    
    # Magic item properties
    is_magical = db.Column(db.Boolean, default=False, nullable=False)
    rarity = db.Column(db.String(20), nullable=True)  # "common", "uncommon", "rare", "very rare", "legendary"
    requires_attunement = db.Column(db.Boolean, default=False, nullable=False)
    charges = db.Column(db.Integer, nullable=True)  # For items with limited uses
    
    # General properties
    stackable = db.Column(db.Boolean, default=True, nullable=False)  # Can multiple be in one inventory slot
    consumable = db.Column(db.Boolean, default=False, nullable=False)  # Gets used up when used
    
    def __repr__(self):
        return f'<Item {self.name}>'


class CharacterItem(db.Model):
    """Association model for character inventory with quantity and equipment details."""
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    equipped = db.Column(db.Boolean, default=False, nullable=False)
    
    # Equipment slot tracking for armor and accessories
    equipment_slot = db.Column(db.String(30), nullable=True)  # "main_hand", "off_hand", "armor", "helmet", etc.
    
    # Condition and customization
    condition = db.Column(db.String(20), default="good", nullable=False)  # "broken", "damaged", "good", "excellent"
    notes = db.Column(db.Text, nullable=True)  # Custom notes about this specific item
    
    # Attunement tracking for magic items
    attuned = db.Column(db.Boolean, default=False, nullable=False)
    
    # Charges tracking for items with limited uses
    current_charges = db.Column(db.Integer, nullable=True)
    
    # Relationships
    item = db.relationship('Item', backref='character_items')
    
    def __repr__(self):
        return f'<CharacterItem {self.quantity}x {self.item.name if self.item else "Unknown"}>'


class Feature(db.Model):
    """Model for character features from race, class, background, etc."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    feature_type = db.Column(db.String(50), nullable=False)  # 'racial', 'class', 'background', 'feat', etc.
    
    # Usage and limitations
    uses_per_rest = db.Column(db.Integer, nullable=True)  # How many times per short/long rest
    rest_type = db.Column(db.String(20), nullable=True)  # "short", "long", "none" (unlimited)
    level_required = db.Column(db.Integer, nullable=True)  # Minimum level to get this feature
    
    # Class/subclass specific
    source_class = db.Column(db.String(50), nullable=True)  # Which class grants this feature
    source_subclass = db.Column(db.String(50), nullable=True)  # Which subclass grants this feature
    
    # Prerequisites and conditions
    prerequisites = db.Column(db.Text, nullable=True)  # Any requirements to use this feature
    
    def __repr__(self):
        return f'<Feature {self.name}>'


class SpellSlot(db.Model):
    """Model for tracking character spell slots."""
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)  # Spell slot level (1-9)
    total_slots = db.Column(db.Integer, nullable=False)  # Total slots available
    used_slots = db.Column(db.Integer, default=0, nullable=False)  # Slots currently used
    
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
        return f'<SpellSlot Level {self.level}: {self.remaining_slots}/{self.total_slots}>'


class Spell(db.Model):
    """Model for D&D spells."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer, nullable=False)  # 0-9, where 0 is cantrips
    school = db.Column(db.String(30), nullable=False)  # "evocation", "illusion", etc.
    
    # Casting details
    casting_time = db.Column(db.String(50), nullable=True)  # "1 action", "1 bonus action", "10 minutes"
    spell_range = db.Column(db.String(50), nullable=True)  # "60 feet", "Touch", "Self"
    components = db.Column(db.String(100), nullable=True)  # "V, S, M (a tiny bell)"
    duration = db.Column(db.String(50), nullable=True)  # "Instantaneous", "Concentration, up to 1 hour"
    
    # Spell description and mechanics
    description = db.Column(db.Text, nullable=False)
    higher_level = db.Column(db.Text, nullable=True)  # Description of casting at higher levels
    
    # Spell lists (which classes can learn this spell)
    class_lists = db.Column(db.Text, nullable=True)  # Comma-separated: "wizard,sorcerer,bard"
    
    # Source and references
    source = db.Column(db.String(50), nullable=True)  # "PHB", "XGE", etc.
    
    # Ritual and concentration
    is_ritual = db.Column(db.Boolean, default=False, nullable=False)
    requires_concentration = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f'<Spell {self.name} (Level {self.level})>'


class Post(db.Model):
    """Post model for user-generated content."""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationship to User
    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.title}>'
