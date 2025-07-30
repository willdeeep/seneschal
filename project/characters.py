"""Character management blueprint for D&D character sheets."""

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from project import db
from project.models import (
    Character,
    Species,
    CharacterClass,
    SubSpecies,
    Proficiency,
    Language,
    Item,
    CharacterItem,
    Feature,
    Spell,
    Background,
    Equipment,
)

bp = Blueprint("characters", __name__, url_prefix="/characters")


@bp.route("/")
@login_required
def index():
    """Display all characters for the current user."""
    characters = Character.query.filter_by(user_id=current_user.id).all()
    return render_template("characters/index.html", characters=characters)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new character."""
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        player_name = request.form.get("player_name")
        species_id = request.form.get("species_id")
        subspecies_id = request.form.get("subspecies_id") if request.form.get("subspecies_id") else None
        class_id = request.form.get("class_id")
        background_id = request.form.get("background_id") if request.form.get("background_id") else None
        level = int(request.form.get("level", 1))
        background = request.form.get("background")  # Keep for backward compatibility

        # Ability scores
        strength = int(request.form.get("strength", 10))
        dexterity = int(request.form.get("dexterity", 10))
        constitution = int(request.form.get("constitution", 10))
        intelligence = int(request.form.get("intelligence", 10))
        wisdom = int(request.form.get("wisdom", 10))
        charisma = int(request.form.get("charisma", 10))

        # Combat stats
        max_hp = int(request.form.get("max_hp", 1))
        current_hp = int(request.form.get("current_hp", max_hp))
        armor_class = int(request.form.get("armor_class", 10))
        initiative = int(request.form.get("initiative", 0))
        speed = int(request.form.get("speed", 30))
        gold_pieces = int(request.form.get("gold_pieces", 0))

        # Character details
        personality_traits = request.form.get("personality_traits")
        ideals = request.form.get("ideals")
        bonds = request.form.get("bonds")
        flaws = request.form.get("flaws")

        # Extended backstory fields
        why_adventuring = request.form.get("why_adventuring")
        motivation_list = request.form.getlist("motivation")  # Get list from checkboxes
        # Convert to comma-separated string
        motivation = ",".join(motivation_list) if motivation_list else ""
        origin = request.form.get("origin")
        class_origin = request.form.get("class_origin")
        attachments = request.form.get("attachments")
        secret = request.form.get("secret")
        attitude_origin = request.form.get("attitude_origin")

        # Enhanced validation
        errors = []

        # Required field validation
        if not name or not name.strip():
            errors.append("Character name is required.")
        elif len(name.strip()) < 2:
            errors.append("Character name must be at least 2 characters long.")
        elif len(name.strip()) > 50:
            errors.append("Character name cannot exceed 50 characters.")

        if not species_id:
            errors.append("Species selection is required.")
        else:
            # Validate species exists
            species = db.session.get(Species, int(species_id))
            if not species:
                errors.append("Selected species is invalid.")

        if not class_id:
            errors.append("Class selection is required.")
        else:
            # Validate class exists
            char_class = db.session.get(CharacterClass, int(class_id))
            if not char_class:
                errors.append("Selected class is invalid.")

        # Validate subspecies if provided
        if subspecies_id:
            subspecies = db.session.get(SubSpecies, int(subspecies_id))
            if not subspecies:
                errors.append("Selected subspecies is invalid.")
            elif subspecies.species_id != int(species_id):
                errors.append("Selected subspecies does not belong to the chosen species.")

        # Validate ability scores
        ability_scores = [strength, dexterity, constitution, intelligence, wisdom, charisma]
        for i, score in enumerate(ability_scores):
            ability_names = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
            if score < 3 or score > 20:
                errors.append(f"{ability_names[i]} must be between 3 and 20.")

        # Validate level
        if level < 1 or level > 20:
            errors.append("Level must be between 1 and 20.")

        # Validate HP values
        if max_hp < 1:
            errors.append("Maximum HP must be at least 1.")
        if current_hp < 0:
            errors.append("Current HP cannot be negative.")
        if current_hp > max_hp:
            errors.append("Current HP cannot exceed Maximum HP.")

        # Validate AC and other combat stats
        if armor_class < 1 or armor_class > 30:
            errors.append("Armor Class must be between 1 and 30.")
        if initiative < -10 or initiative > 20:
            errors.append("Initiative modifier must be between -10 and +20.")
        if speed < 0 or speed > 120:
            errors.append("Speed must be between 0 and 120 feet.")

        # Validate gold pieces
        if gold_pieces < 0:
            errors.append("Gold pieces cannot be negative.")

        if errors:
            for error in errors:
                flash(error, "error")
            species = Species.query.order_by(Species.name).all()
            classes = CharacterClass.query.order_by(CharacterClass.name).all()
            subspecies = SubSpecies.query.order_by(SubSpecies.name).all()
            return render_template("characters/create.html",
                                 species=species,
                                 classes=classes,
                                 subspecies=subspecies,
                                 form_data=request.form)

        # Create character
        character = Character(
            name=name,
            player_name=player_name,
            species_id=int(species_id) if species_id else None,
            subspecies_id=int(subspecies_id) if subspecies_id else None,
            class_id=int(class_id) if class_id else None,
            background_id=int(background_id) if background_id else None,
            level=level,
            background=background,
            strength=strength,
            dexterity=dexterity,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            max_hp=max_hp,
            current_hp=current_hp,
            armor_class=armor_class,
            initiative=initiative,
            speed=speed,
            gold_pieces=gold_pieces,
            personality_traits=personality_traits,
            ideals=ideals,
            bonds=bonds,
            flaws=flaws,
            why_adventuring=why_adventuring,
            motivation=motivation,
            origin=origin,
            class_origin=class_origin,
            attachments=attachments,
            secret=secret,
            attitude_origin=attitude_origin,
            user_id=current_user.id,
        )

        # Handle proficiencies
        proficiency_ids = request.form.getlist("proficiencies")
        for prof_id in proficiency_ids:
            proficiency = db.session.get(Proficiency, int(prof_id))
            if proficiency:
                character.proficiencies.append(proficiency)

        # Handle languages
        language_ids = request.form.getlist("languages")
        for lang_id in language_ids:
            language = db.session.get(Language, int(lang_id))
            if language:
                character.languages.append(language)

        # Handle features
        feature_ids = request.form.getlist("features")
        for feat_id in feature_ids:
            feature = db.session.get(Feature, int(feat_id))
            if feature:
                character.features.append(feature)

        # Handle spells
        spell_ids = request.form.getlist("spells")
        for spell_id in spell_ids:
            spell = db.session.get(Spell, int(spell_id))
            if spell:
                character.spells.append(spell)

        try:
            db.session.add(character)
            db.session.commit()
            flash(f"Character {name} created successfully!", "success")
            return redirect(url_for("characters.view", character_id=character.id))
        except SQLAlchemyError:
            db.session.rollback()
            flash("An error occurred while creating the character.", "error")
            species = Species.query.order_by(Species.name).all()
            classes = CharacterClass.query.order_by(CharacterClass.name).all()
            subspecies = SubSpecies.query.order_by(SubSpecies.name).all()
            return render_template("characters/create.html",
                                 species=species,
                                 classes=classes,
                                 subspecies=subspecies)

    # GET request - show form with dynamic loading enabled
    species = Species.query.order_by(Species.name).all()
    classes = CharacterClass.query.order_by(CharacterClass.name).all()
    subspecies = SubSpecies.query.order_by(SubSpecies.name).all()
    backgrounds = Background.query.order_by(Background.name).all()
    return render_template("characters/create.html",
                         species=species,
                         classes=classes,
                         subspecies=subspecies,
                         backgrounds=backgrounds)


@bp.route("/<int:character_id>")
@login_required
def view(character_id):
    """View a specific character."""
    character = Character.query.filter_by(
        id=character_id, user_id=current_user.id
    ).first_or_404()
    return render_template("characters/view.html", character=character)


@bp.route("/<int:character_id>/edit", methods=["GET", "POST"])
@login_required
def edit(character_id):
    """Edit a character."""
    character = Character.query.filter_by(
        id=character_id, user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":
        # Update character with form data
        character.name = request.form.get("name")
        character.player_name = request.form.get("player_name")
        character.race = request.form.get("race")
        character.character_class = request.form.get("character_class")
        character.level = int(request.form.get("level", 1))
        character.background = request.form.get("background")

        # Ability scores
        character.strength = int(request.form.get("strength", 10))
        character.dexterity = int(request.form.get("dexterity", 10))
        character.constitution = int(request.form.get("constitution", 10))
        character.intelligence = int(request.form.get("intelligence", 10))
        character.wisdom = int(request.form.get("wisdom", 10))
        character.charisma = int(request.form.get("charisma", 10))

        # Combat stats
        character.max_hp = int(request.form.get("max_hp", 1))
        character.current_hp = int(request.form.get("current_hp", character.max_hp))
        character.armor_class = int(request.form.get("armor_class", 10))
        character.initiative = int(request.form.get("initiative", 0))
        character.speed = int(request.form.get("speed", 30))
        character.gold_pieces = int(request.form.get("gold_pieces", 0))

        # Character details
        character.personality_traits = request.form.get("personality_traits")
        character.ideals = request.form.get("ideals")
        character.bonds = request.form.get("bonds")
        character.flaws = request.form.get("flaws")

        # Backstory fields
        character.why_adventuring = request.form.get("why_adventuring")
        motivation_list = request.form.getlist("motivation")
        character.motivation = ",".join(motivation_list) if motivation_list else ""
        character.origin = request.form.get("origin")
        character.class_origin = request.form.get("class_origin")
        character.attachments = request.form.get("attachments")
        character.secret = request.form.get("secret")
        character.attitude_origin = request.form.get("attitude_origin")

        # Update relationships
        character.proficiencies = []
        proficiency_ids = request.form.getlist("proficiencies")
        for prof_id in proficiency_ids:
            proficiency = db.session.get(Proficiency, int(prof_id))
            if proficiency:
                character.proficiencies.append(proficiency)

        character.languages = []
        language_ids = request.form.getlist("languages")
        for lang_id in language_ids:
            language = db.session.get(Language, int(lang_id))
            if language:
                character.languages.append(language)

        character.features = []
        feature_ids = request.form.getlist("features")
        for feat_id in feature_ids:
            feature = db.session.get(Feature, int(feat_id))
            if feature:
                character.features.append(feature)

        try:
            db.session.commit()
            flash(f"Character {character.name} updated successfully!", "success")
            return redirect(url_for("characters.view", character_id=character.id))
        except SQLAlchemyError:
            db.session.rollback()
            flash("An error occurred while updating the character.", "error")

    # GET request or error - show form
    proficiencies = Proficiency.query.all()
    languages = Language.query.all()
    features = Feature.query.all()

    return render_template(
        "characters/edit.html",
        character=character,
        proficiencies=proficiencies,
        languages=languages,
        features=features,
    )


@bp.route("/<int:character_id>/delete", methods=["POST"])
@login_required
def delete(character_id):
    """Delete a character."""
    character = Character.query.filter_by(
        id=character_id, user_id=current_user.id
    ).first_or_404()

    try:
        db.session.delete(character)
        db.session.commit()
        flash(f"Character {character.name} deleted successfully!", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("An error occurred while deleting the character.", "error")

    return redirect(url_for("characters.index"))


@bp.route("/<int:character_id>/inventory")
@login_required
def inventory(character_id):
    """Manage character inventory."""
    character = Character.query.filter_by(
        id=character_id, user_id=current_user.id
    ).first_or_404()
    items = Item.query.all()
    return render_template(
        "characters/inventory.html", character=character, items=items
    )


@bp.route("/<int:character_id>/inventory/add", methods=["POST"])
@login_required
def add_item(character_id):
    """Add item to character inventory."""
    character = Character.query.filter_by(
        id=character_id, user_id=current_user.id
    ).first_or_404()

    item_id = request.form.get("item_id")
    quantity = int(request.form.get("quantity", 1))
    equipped = bool(request.form.get("equipped"))

    if not item_id:
        flash("Please select an item.", "error")
        return redirect(url_for("characters.inventory", character_id=character_id))

    # Check if item already exists in inventory
    existing_item = CharacterItem.query.filter_by(
        character_id=character.id, item_id=item_id
    ).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        character_item = CharacterItem(
            character_id=character.id,
            item_id=item_id,
            quantity=quantity,
            equipped=equipped,
        )
        db.session.add(character_item)

    try:
        db.session.commit()
        flash("Item added to inventory!", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("An error occurred while adding the item.", "error")

    return redirect(url_for("characters.inventory", character_id=character_id))


@bp.route("/inventory/<int:item_id>/remove", methods=["POST"])
@login_required
def remove_item(item_id):
    """Remove item from character inventory."""
    character_item = CharacterItem.query.get_or_404(item_id)
    character = character_item.character

    # Verify ownership
    if character.user_id != current_user.id:
        flash("You can only modify your own characters.", "error")
        return redirect(url_for("characters.index"))

    try:
        db.session.delete(character_item)
        db.session.commit()
        flash("Item removed from inventory!", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("An error occurred while removing the item.", "error")

    return redirect(url_for("characters.inventory", character_id=character.id))


def get_max_skill_proficiencies(class_id):
    """Get the maximum number of skill proficiencies a class can choose."""
    if not class_id:
        return 2

    char_class = db.session.get(CharacterClass, class_id)
    if not char_class:
        return 2

    # D&D 5e skill proficiency limits by class
    skill_limits = {
        "Fighter": 2,
        "Rogue": 4,  # Rogues get more skills
        "Wizard": 2,
        "Cleric": 2,
        "Barbarian": 2,
        "Bard": 3,   # Bards are versatile
        "Druid": 2,
        "Monk": 2,
        "Paladin": 2,
        "Ranger": 3, # Rangers get more skills
        "Sorcerer": 2,
        "Warlock": 2
    }

    return skill_limits.get(char_class.name, 2)


# API endpoints for dynamic character creation
@bp.route("/api/proficiencies")
@login_required
def get_available_proficiencies():
    """Get proficiencies available for a species/class combination."""
    species_id = request.args.get("species_id")
    class_id = request.args.get("class_id")

    available_proficiencies = []
    base_proficiencies = set()
    optional_proficiencies = set()

    # Get base proficiencies from species
    if species_id:
        species = db.session.get(Species, species_id)
        if species and hasattr(species, 'proficiencies') and species.proficiencies:
            base_proficiencies.update(species.proficiencies)

    # Get base proficiencies from class
    if class_id:
        char_class = db.session.get(CharacterClass, class_id)
        if char_class:
            # Add required class proficiencies
            if char_class.skill_proficiencies:
                base_proficiencies.update(char_class.skill_proficiencies)
            if char_class.armor_proficiencies:
                base_proficiencies.update(char_class.armor_proficiencies)
            if char_class.weapon_proficiencies:
                base_proficiencies.update(char_class.weapon_proficiencies)

            # Add class-specific optional skill proficiencies based on D&D 5e rules
            if char_class.name == "Fighter":
                optional_proficiencies.update(["Acrobatics", "Animal Handling", "Athletics",
                                              "History", "Insight", "Intimidation", "Perception", "Survival"])
            elif char_class.name == "Rogue":
                optional_proficiencies.update(["Acrobatics", "Athletics", "Deception", "Insight",
                                              "Intimidation", "Investigation", "Perception", "Performance",
                                              "Persuasion", "Sleight of Hand", "Stealth"])
            elif char_class.name == "Wizard":
                optional_proficiencies.update(["Arcana", "History", "Insight", "Investigation",
                                              "Medicine", "Religion"])
            elif char_class.name == "Cleric":
                optional_proficiencies.update(["History", "Insight", "Medicine", "Persuasion", "Religion"])
            elif char_class.name == "Barbarian":
                optional_proficiencies.update(["Animal Handling", "Athletics", "Intimidation",
                                              "Nature", "Perception", "Survival"])
            elif char_class.name == "Bard":
                optional_proficiencies.update(["Deception", "History", "Investigation", "Persuasion",
                                              "Sleight of Hand", "Stealth"])
            elif char_class.name == "Druid":
                optional_proficiencies.update(["Arcana", "Animal Handling", "Insight", "Medicine",
                                              "Nature", "Perception", "Religion", "Survival"])
            elif char_class.name == "Monk":
                optional_proficiencies.update(["Acrobatics", "Athletics", "History", "Insight",
                                              "Religion", "Stealth"])
            elif char_class.name == "Paladin":
                optional_proficiencies.update(["Athletics", "Insight", "Intimidation", "Medicine",
                                              "Persuasion", "Religion"])
            elif char_class.name == "Ranger":
                optional_proficiencies.update(["Animal Handling", "Athletics", "Insight", "Investigation",
                                              "Nature", "Perception", "Stealth", "Survival"])
            elif char_class.name == "Sorcerer":
                optional_proficiencies.update(["Arcana", "Deception", "Insight", "Intimidation",
                                              "Persuasion", "Religion"])
            elif char_class.name == "Warlock":
                optional_proficiencies.update(["Arcana", "Deception", "History", "Intimidation",
                                              "Investigation", "Nature", "Religion"])

    # If no specific proficiencies found, add some general ones
    if not optional_proficiencies:
        optional_proficiencies.update(["Athletics", "Insight", "Perception", "Persuasion"])

    # Create required and optional proficiency objects for the frontend
    required_proficiencies = []
    optional_proficiencies_list = []

    # Process base (required) proficiencies
    for prof_name in base_proficiencies:
        # Determine proficiency category based on name
        category = "Skill"
        if any(armor in prof_name for armor in ["Armor", "Shield", "Light", "Medium", "Heavy"]):
            category = "Armor"
        elif any(weapon in prof_name for weapon in ["Weapon", "Sword", "Bow", "Axe", "Hammer", "Simple", "Martial"]):
            category = "Weapon"
        elif "Tools" in prof_name or "Kit" in prof_name:
            category = "Tool"

        required_proficiencies.append({
            "id": f"req_{len(required_proficiencies) + 1}",
            "name": prof_name,
            "category": category
        })

    # Process optional proficiencies (those that are not required)
    for prof_name in optional_proficiencies:
        if prof_name not in base_proficiencies:
            # Determine proficiency category based on name
            category = "Skill"
            if any(armor in prof_name for armor in ["Armor", "Shield", "Light", "Medium", "Heavy"]):
                category = "Armor"
            elif any(weapon in prof_name for weapon in ["Weapon", "Sword", "Bow", "Axe", "Hammer", "Simple", "Martial"]):
                category = "Weapon"
            elif "Tools" in prof_name or "Kit" in prof_name:
                category = "Tool"

            optional_proficiencies_list.append({
                "id": f"opt_{len(optional_proficiencies_list) + 1}",
                "name": prof_name,
                "category": category
            })

    max_skill_selections = get_max_skill_proficiencies(class_id)

    return jsonify({
        "required": required_proficiencies,
        "optional": optional_proficiencies_list,
        "max_selections": max_skill_selections,
        "skill_count": max_skill_selections
    })


@bp.route("/api/languages")
@login_required
def get_available_languages():
    """Get languages available for a species/class combination."""
    species_id = request.args.get("species_id")
    class_id = request.args.get("class_id")

    base_languages = set()
    optional_languages = set()

    # Get base languages from species
    if species_id:
        species = db.session.get(Species, species_id)
        if species and species.languages:
            base_languages.update(species.languages)

    # Get additional languages from class (if any)
    if class_id:
        char_class = db.session.get(CharacterClass, class_id)
        if char_class and char_class.name == "Druid":
            base_languages.add("Druidic")

    # Standard optional languages for selection
    standard_languages = [
        "Common", "Dwarvish", "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Orc"
    ]
    exotic_languages = [
        "Abyssal", "Celestial", "Draconic", "Deep Speech", "Infernal", "Primordial", "Sylvan", "Undercommon"
    ]

    # Add optional languages (excluding already known ones)
    optional_languages.update(lang for lang in standard_languages if lang not in base_languages)
    optional_languages.update(lang for lang in exotic_languages if lang not in base_languages)

    # Format for frontend as base and optional languages
    base_language_list = []
    optional_language_list = []

    # Process base languages
    for lang in base_languages:
        base_language_list.append({
            "id": f"base_{len(base_language_list) + 1}",
            "name": lang
        })

    # Process optional languages
    for lang in optional_languages:
        optional_language_list.append({
            "id": f"opt_{len(optional_language_list) + 1}",
            "name": lang
        })

    return jsonify({
        "base": base_language_list,
        "optional": optional_language_list
    })


@bp.route("/api/features")
@login_required
def get_available_features():
    """Get features available for a race/class combination."""
    character_class = request.args.get("class", "")

    # Get racial features (for now, return all racial features)
    racial_features = Feature.query.filter(Feature.feature_type == "racial").all()

    # Get class features specific to the class
    class_features = Feature.query.filter(
        Feature.feature_type == "class",
        Feature.source_class.ilike(f"%{character_class}%") if character_class else True,
    ).all()

    # Get general features available to all
    general_features = Feature.query.filter(
        Feature.feature_type.in_(["general", "feat"])
    ).all()

    # Combine all available features
    features = racial_features + class_features + general_features

    return jsonify(
        {
            "features": [
                {
                    "id": feat.id,
                    "name": feat.name,
                    "source": feat.source_class or feat.feature_type.title(),
                    "description": feat.description,
                }
                for feat in features
            ]
        }
    )


@bp.route("/api/spells")
@login_required
def get_available_spells():
    """Get spells available for a class."""
    character_class = request.args.get("class", "")
    # Class spell lists
    class_spell_lists = {
        "Wizard": ["wizard"],
        "Sorcerer": ["sorcerer"],
        "Warlock": ["warlock"],
        "Bard": ["bard"],
        "Cleric": ["cleric"],
        "Druid": ["druid"],
        "Paladin": ["paladin"],
        "Ranger": ["ranger"],
    }

    # Non-spellcasting classes
    if character_class not in class_spell_lists:
        return jsonify({"spells": []})

    # Get spells available to this class (level 0-2 for character creation)
    spells = Spell.query.filter(Spell.level <= 2).all()

    return jsonify(
        {
            "spells": [
                {
                    "id": spell.id,
                    "name": spell.name,
                    "level": spell.level,
                    "school": spell.school,
                    "description": (
                        spell.description[:100] + "..."
                        if len(spell.description) > 100
                        else spell.description
                    ),
                }
                for spell in spells
            ]
        }
    )


@bp.route("/api/races")
@login_required
def get_races():
    """Get all available races."""
    races = [
        "Human",
        "Elf",
        "Dwarf",
        "Halfling",
        "Dragonborn",
        "Gnome",
        "Half-Elf",
        "Half-Orc",
        "Tiefling",
    ]
    return jsonify(races)


@bp.route("/api/classes")
@login_required
def get_classes():
    """Get all available classes."""
    classes = [
        "Barbarian",
        "Bard",
        "Cleric",
        "Druid",
        "Fighter",
        "Monk",
        "Paladin",
        "Ranger",
        "Rogue",
        "Sorcerer",
        "Warlock",
        "Wizard",
    ]
    return jsonify(classes)


@bp.route("/ability-bonuses")
@login_required
def get_ability_bonuses():
    """Get ability score bonuses for species and subspecies combination."""
    species_id = request.args.get("species_id")
    subspecies_id = request.args.get("subspecies_id")
    bonuses = {
        "str": 0, "dex": 0, "con": 0,
        "int": 0, "wis": 0, "cha": 0
    }
    species_info = {}
    subspecies_info = {}
    if species_id:
        species = db.session.get(Species, species_id)
        if species:
            species_info = {
                "name": species.name,
                "size": species.size,
                "speed": species.speed,
                "traits": species.traits or [],
                "languages": species.languages or []
            }
            if species.ability_score_increases:
                for ability, bonus in species.ability_score_increases.items():
                    if ability in bonuses:
                        bonuses[ability] += bonus
    if subspecies_id:
        subspecies = db.session.get(SubSpecies, subspecies_id)
        if subspecies and subspecies.additional_traits:
            subspecies_info = {
                "name": subspecies.name,
                "additional_traits": subspecies.additional_traits
            }
    return jsonify({
        "bonuses": bonuses,
        "species_info": species_info,
        "subspecies_info": subspecies_info
    })


# Advanced Character Customization API Endpoints

@bp.route("/api/backgrounds")
def api_backgrounds():
    """Get available character backgrounds."""
    from project.models import Background
    
    backgrounds = Background.query.all()
    return jsonify([{
        "id": bg.id,
        "name": bg.name,
        "description": bg.description,
        "skill_proficiencies": bg.skill_proficiencies,
        "tool_proficiencies": bg.tool_proficiencies,
        "languages": bg.languages,
        "equipment": bg.equipment,
        "feature_name": bg.feature_name,
        "feature_description": bg.feature_description,
        "starting_gold": bg.starting_gold
    } for bg in backgrounds])


@bp.route("/api/equipment")
def api_equipment():
    """Get equipment based on class and background."""
    from project.models import Equipment, CharacterClass, Background
    
    class_id = request.args.get("class_id", type=int)
    background_id = request.args.get("background_id", type=int)
    category = request.args.get("category")  # Optional filter
    
    equipment = []
    
    if class_id:
        char_class = db.session.get(CharacterClass, class_id)
        if char_class:
            # Get class-appropriate equipment
            class_equipment = Equipment.get_starting_equipment_for_class(char_class.name)
            equipment.extend(class_equipment)
    
    if background_id:
        background = db.session.get(Background, background_id)
        if background and background.equipment:
            # Get background equipment
            bg_equipment = Equipment.query.filter(
                Equipment.name.in_(background.equipment)
            ).all()
            equipment.extend(bg_equipment)
    
    if category:
        equipment = [item for item in equipment if item.category.lower() == category.lower()]
    
    # Remove duplicates
    equipment = list({item.id: item for item in equipment}.values())
    
    return jsonify([{
        "id": item.id,
        "name": item.name,
        "category": item.category,
        "cost_cp": item.cost_cp,
        "weight": item.weight,
        "description": item.description,
        "damage_dice": item.damage_dice,
        "damage_type": item.damage_type,
        "armor_class": item.armor_class
    } for item in equipment])


@bp.route("/api/cantrips")
def api_cantrips():
    """Get available cantrips for a character class."""
    class_id = request.args.get("class_id", type=int)
    
    if not class_id:
        return jsonify({"error": "class_id parameter is required"}), 400
    
    char_class = db.session.get(CharacterClass, class_id)
    if not char_class:
        return jsonify({"error": "Invalid class_id"}), 400
    
    # Get cantrips available to this class
    cantrips = Spell.query.filter(
        Spell.level == 0,
        Spell.class_lists.contains(char_class.name.lower())
    ).all()
    
    return jsonify([{
        "id": spell.id,
        "name": spell.name,
        "school": spell.school,
        "casting_time": spell.casting_time,
        "range": spell.spell_range,
        "components": spell.components,
        "duration": spell.duration,
        "description": spell.description
    } for spell in cantrips])


@bp.route("/api/starting-spells")
def api_starting_spells():
    """Get starting spells for a character class at level 1."""
    class_id = request.args.get("class_id", type=int)
    
    if not class_id:
        return jsonify({"error": "class_id parameter is required"}), 400
    
    char_class = db.session.get(CharacterClass, class_id)
    if not char_class:
        return jsonify({"error": "Invalid class_id"}), 400
    
    # Get 1st level spells available to this class
    spells = Spell.query.filter(
        Spell.level == 1,
        Spell.class_lists.contains(char_class.name.lower())
    ).all()
    
    # Determine spell limits based on class
    spell_limits = {
        "Wizard": {"known": 6, "can_choose": True},
        "Sorcerer": {"known": 2, "can_choose": True},
        "Bard": {"known": 4, "can_choose": True},
        "Warlock": {"known": 2, "can_choose": True},
        "Cleric": {"known": -1, "can_choose": False},  # Prepares from full list
        "Druid": {"known": -1, "can_choose": False},   # Prepares from full list
    }
    
    limits = spell_limits.get(char_class.name, {"known": 0, "can_choose": False})
    
    return jsonify({
        "spells": [{
            "id": spell.id,
            "name": spell.name,
            "school": spell.school,
            "casting_time": spell.casting_time,
            "range": spell.spell_range,
            "components": spell.components,
            "duration": spell.duration,
            "description": spell.description,
            "is_ritual": spell.is_ritual
        } for spell in spells],
        "limits": limits
    })


@bp.route("/api/ability-score-methods")
def api_ability_score_methods():
    """Get available ability score generation methods."""
    methods = {
        "standard_array": {
            "name": "Standard Array",
            "description": "Use the standard array: 15, 14, 13, 12, 10, 8",
            "values": [15, 14, 13, 12, 10, 8],
            "point_buy": False
        },
        "point_buy": {
            "name": "Point Buy",
            "description": "Purchase ability scores using a point system (27 points)",
            "base_cost": 27,
            "min_score": 8,
            "max_score": 15,
            "point_buy": True
        },
        "rolling": {
            "name": "Rolling",
            "description": "Roll 4d6, drop lowest, six times",
            "point_buy": False,
            "requires_rolling": True
        },
        "custom": {
            "name": "Custom",
            "description": "Enter custom ability scores (DM approval may be required)",
            "point_buy": False,
            "custom": True
        }
    }
    
    return jsonify(methods)


@bp.route("/api/character-optimization")
def api_character_optimization():
    """Get character build optimization suggestions."""
    species_id = request.args.get("species_id", type=int)
    class_id = request.args.get("class_id", type=int)
    background_id = request.args.get("background_id", type=int)
    
    if not species_id or not class_id:
        return jsonify({"error": "species_id and class_id are required"}), 400
    
    species = db.session.get(Species, species_id)
    char_class = db.session.get(CharacterClass, class_id)
    background = db.session.get(Background, background_id) if background_id else None
    
    if not species or not char_class:
        return jsonify({"error": "Invalid species_id or class_id"}), 400
    
    # Basic optimization suggestions
    suggestions = {
        "recommended_abilities": _get_recommended_abilities(char_class, species),
        "recommended_proficiencies": _get_recommended_proficiencies(char_class, background),
        "synergies": _get_species_class_synergies(species, char_class),
        "warnings": _get_build_warnings(species, char_class)
    }
    
    return jsonify(suggestions)


def _get_recommended_abilities(char_class, species):
    """Get recommended ability score priorities."""
    class_priorities = {
        "Fighter": ["Strength", "Constitution", "Dexterity"],
        "Wizard": ["Intelligence", "Constitution", "Dexterity"],
        "Rogue": ["Dexterity", "Constitution", "Intelligence"],
        "Cleric": ["Wisdom", "Constitution", "Strength"],
        "Ranger": ["Dexterity", "Wisdom", "Constitution"],
        "Bard": ["Charisma", "Dexterity", "Constitution"],
        "Sorcerer": ["Charisma", "Constitution", "Dexterity"],
        "Warlock": ["Charisma", "Constitution", "Dexterity"],
        "Barbarian": ["Strength", "Constitution", "Dexterity"],
        "Druid": ["Wisdom", "Constitution", "Dexterity"],
        "Monk": ["Dexterity", "Wisdom", "Constitution"],
        "Paladin": ["Strength", "Charisma", "Constitution"]
    }
    
    priorities = class_priorities.get(char_class.name, ["Constitution"])
    
    # Factor in species bonuses
    if species.ability_score_increases:
        species_bonuses = list(species.ability_score_increases.keys())
        # Move species-boosted abilities higher in priority
        for ability in species_bonuses:
            ability_full = {
                "str": "Strength", "dex": "Dexterity", "con": "Constitution",
                "int": "Intelligence", "wis": "Wisdom", "cha": "Charisma"
            }.get(ability, ability)
            
            if ability_full in priorities:
                priorities.remove(ability_full)
                priorities.insert(0, ability_full)
    
    return priorities


def _get_recommended_proficiencies(char_class, background):
    """Get recommended skill proficiencies."""
    recommendations = []
    
    if char_class.skill_proficiencies:
        # Recommend skills that match class primary ability
        primary_skills = {
            "Strength": ["Athletics"],
            "Dexterity": ["Acrobatics", "Sleight of Hand", "Stealth"],
            "Intelligence": ["Arcana", "History", "Investigation", "Nature", "Religion"],
            "Wisdom": ["Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
            "Charisma": ["Deception", "Intimidation", "Performance", "Persuasion"]
        }

        if char_class.primary_ability in primary_skills:
            class_skills = set(char_class.skill_proficiencies)
            recommended_skills = set(primary_skills[char_class.primary_ability])
            recommendations.extend(list(class_skills.intersection(recommended_skills)))
    
    return recommendations


def _get_species_class_synergies(species, char_class):
    """Identify positive synergies between species and class."""
    synergies = []
    
    if species.ability_score_increases and char_class.primary_ability:
        primary_short = {
            "Strength": "str", "Dexterity": "dex", "Constitution": "con",
            "Intelligence": "int", "Wisdom": "wis", "Charisma": "cha"
        }.get(char_class.primary_ability, "")

        if primary_short in species.ability_score_increases:
            synergies.append({
                "type": "ability_synergy",
                "description": f"{species.name} gets a bonus to {char_class.primary_ability}, which is {char_class.name}'s primary ability"
            })
    
    # Check for matching proficiencies
    if species.proficiencies and char_class.skill_proficiencies:
        matching_profs = set(species.proficiencies).intersection(set(char_class.skill_proficiencies))
        if matching_profs:
            synergies.append({
                "type": "proficiency_synergy",
                "description": f"Both {species.name} and {char_class.name} provide {', '.join(matching_profs)} proficiency"
            })
    
    return synergies


def _get_build_warnings(species, char_class):
    """Identify potential issues with the species/class combination."""
    warnings = []
    
    # Check for ability score conflicts
    if species.ability_score_increases and char_class.primary_ability:
        primary_short = {
            "Strength": "str", "Dexterity": "dex", "Constitution": "con",
            "Intelligence": "int", "Wisdom": "wis", "Charisma": "cha"
        }.get(char_class.primary_ability, "")

        if primary_short not in species.ability_score_increases:
            warnings.append({
                "type": "ability_mismatch",
                "description": f"{species.name} doesn't boost {char_class.primary_ability}, which may make this build less optimal"
            })
    
    return warnings
