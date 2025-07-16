"""Character management blueprint for D&D character sheets."""

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from project import db
from project.models import (
    Character, Proficiency, Language, Item, CharacterItem, Feature, Spell
)

bp = Blueprint('characters', __name__, url_prefix='/characters')


@bp.route('/')
@login_required
def index():
    """Display all characters for the current user."""
    characters = Character.query.filter_by(user_id=current_user.id).all()
    return render_template('characters/index.html', characters=characters)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new character."""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        player_name = request.form.get('player_name')
        race = request.form.get('race')
        character_class = request.form.get('character_class')
        level = int(request.form.get('level', 1))
        background = request.form.get('background')
        
        # Ability scores
        strength = int(request.form.get('strength', 10))
        dexterity = int(request.form.get('dexterity', 10))
        constitution = int(request.form.get('constitution', 10))
        intelligence = int(request.form.get('intelligence', 10))
        wisdom = int(request.form.get('wisdom', 10))
        charisma = int(request.form.get('charisma', 10))
        
        # Combat stats
        max_hp = int(request.form.get('max_hp', 1))
        current_hp = int(request.form.get('current_hp', max_hp))
        armor_class = int(request.form.get('armor_class', 10))
        initiative = int(request.form.get('initiative', 0))
        speed = int(request.form.get('speed', 30))
        gold_pieces = int(request.form.get('gold_pieces', 0))
        
        # Character details
        personality_traits = request.form.get('personality_traits')
        ideals = request.form.get('ideals')
        bonds = request.form.get('bonds')
        flaws = request.form.get('flaws')
        
        # Extended backstory fields
        why_adventuring = request.form.get('why_adventuring')
        motivation_list = request.form.getlist('motivation')  # Get list from checkboxes
        motivation = ','.join(motivation_list) if motivation_list else ''  # Convert to comma-separated string
        origin = request.form.get('origin')
        class_origin = request.form.get('class_origin')
        attachments = request.form.get('attachments')
        secret = request.form.get('secret')
        attitude_origin = request.form.get('attitude_origin')
        
        # Validation
        if not all([name, race, character_class]):
            flash('Name, race, and class are required.', 'error')
            return render_template('characters/create.html')
        
        # Create character
        character = Character(
            name=name,
            player_name=player_name,
            race=race,
            character_class=character_class,
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
            user_id=current_user.id
        )
        
        # Handle proficiencies
        proficiency_ids = request.form.getlist('proficiencies')
        for prof_id in proficiency_ids:
            proficiency = Proficiency.query.get(int(prof_id))
            if proficiency:
                character.proficiencies.append(proficiency)
        
        # Handle languages
        language_ids = request.form.getlist('languages')
        for lang_id in language_ids:
            language = Language.query.get(int(lang_id))
            if language:
                character.languages.append(language)
        
        # Handle features
        feature_ids = request.form.getlist('features')
        for feat_id in feature_ids:
            feature = Feature.query.get(int(feat_id))
            if feature:
                character.features.append(feature)
        
        # Handle spells
        spell_ids = request.form.getlist('spells')
        for spell_id in spell_ids:
            spell = Spell.query.get(int(spell_id))
            if spell:
                character.spells.append(spell)
        
        try:
            db.session.add(character)
            db.session.commit()
            flash(f'Character {name} created successfully!', 'success')
            return redirect(url_for('characters.view', character_id=character.id))
        except SQLAlchemyError:
            db.session.rollback()
            flash('An error occurred while creating the character.', 'error')
            return render_template('characters/create.html')
    
    # GET request - show form with dynamic loading enabled
    return render_template('characters/create.html')


@bp.route('/<int:character_id>')
@login_required
def view(character_id):
    """View a specific character."""
    character = Character.query.filter_by(id=character_id, user_id=current_user.id).first_or_404()
    return render_template('characters/view.html', character=character)


@bp.route('/<int:character_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(character_id):
    """Edit a character."""
    character = Character.query.filter_by(id=character_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        # Update character with form data
        character.name = request.form.get('name')
        character.player_name = request.form.get('player_name')
        character.race = request.form.get('race')
        character.character_class = request.form.get('character_class')
        character.level = int(request.form.get('level', 1))
        character.background = request.form.get('background')
        
        # Ability scores
        character.strength = int(request.form.get('strength', 10))
        character.dexterity = int(request.form.get('dexterity', 10))
        character.constitution = int(request.form.get('constitution', 10))
        character.intelligence = int(request.form.get('intelligence', 10))
        character.wisdom = int(request.form.get('wisdom', 10))
        character.charisma = int(request.form.get('charisma', 10))
        
        # Combat stats
        character.max_hp = int(request.form.get('max_hp', 1))
        character.current_hp = int(request.form.get('current_hp', character.max_hp))
        character.armor_class = int(request.form.get('armor_class', 10))
        character.initiative = int(request.form.get('initiative', 0))
        character.speed = int(request.form.get('speed', 30))
        character.gold_pieces = int(request.form.get('gold_pieces', 0))
        
        # Character details
        character.personality_traits = request.form.get('personality_traits')
        character.ideals = request.form.get('ideals')
        character.bonds = request.form.get('bonds')
        character.flaws = request.form.get('flaws')
        
        # Backstory fields
        character.why_adventuring = request.form.get('why_adventuring')
        motivation_list = request.form.getlist('motivation')
        character.motivation = ','.join(motivation_list) if motivation_list else ''
        character.origin = request.form.get('origin')
        character.class_origin = request.form.get('class_origin')
        character.attachments = request.form.get('attachments')
        character.secret = request.form.get('secret')
        character.attitude_origin = request.form.get('attitude_origin')
        
        # Update relationships
        character.proficiencies = []
        proficiency_ids = request.form.getlist('proficiencies')
        for prof_id in proficiency_ids:
            proficiency = Proficiency.query.get(int(prof_id))
            if proficiency:
                character.proficiencies.append(proficiency)
        
        character.languages = []
        language_ids = request.form.getlist('languages')
        for lang_id in language_ids:
            language = Language.query.get(int(lang_id))
            if language:
                character.languages.append(language)
        
        character.features = []
        feature_ids = request.form.getlist('features')
        for feat_id in feature_ids:
            feature = Feature.query.get(int(feat_id))
            if feature:
                character.features.append(feature)
        
        try:
            db.session.commit()
            flash(f'Character {character.name} updated successfully!', 'success')
            return redirect(url_for('characters.view', character_id=character.id))
        except SQLAlchemyError:
            db.session.rollback()
            flash('An error occurred while updating the character.', 'error')
    
    # GET request or error - show form
    proficiencies = Proficiency.query.all()
    languages = Language.query.all()
    features = Feature.query.all()
    
    return render_template('characters/edit.html', 
                         character=character,
                         proficiencies=proficiencies,
                         languages=languages,
                         features=features)


@bp.route('/<int:character_id>/delete', methods=['POST'])
@login_required
def delete(character_id):
    """Delete a character."""
    character = Character.query.filter_by(id=character_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(character)
        db.session.commit()
        flash(f'Character {character.name} deleted successfully!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while deleting the character.', 'error')
    
    return redirect(url_for('characters.index'))


@bp.route('/<int:character_id>/inventory')
@login_required
def inventory(character_id):
    """Manage character inventory."""
    character = Character.query.filter_by(id=character_id, user_id=current_user.id).first_or_404()
    items = Item.query.all()
    return render_template('characters/inventory.html', character=character, items=items)


@bp.route('/<int:character_id>/inventory/add', methods=['POST'])
@login_required
def add_item(character_id):
    """Add item to character inventory."""
    character = Character.query.filter_by(id=character_id, user_id=current_user.id).first_or_404()
    
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 1))
    equipped = bool(request.form.get('equipped'))
    
    if not item_id:
        flash('Please select an item.', 'error')
        return redirect(url_for('characters.inventory', character_id=character_id))
    
    # Check if item already exists in inventory
    existing_item = CharacterItem.query.filter_by(
        character_id=character.id, 
        item_id=item_id
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
    else:
        character_item = CharacterItem(
            character_id=character.id,
            item_id=item_id,
            quantity=quantity,
            equipped=equipped
        )
        db.session.add(character_item)
    
    try:
        db.session.commit()
        flash('Item added to inventory!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while adding the item.', 'error')
    
    return redirect(url_for('characters.inventory', character_id=character_id))


@bp.route('/inventory/<int:item_id>/remove', methods=['POST'])
@login_required
def remove_item(item_id):
    """Remove item from character inventory."""
    character_item = CharacterItem.query.get_or_404(item_id)
    character = character_item.character
    
    # Verify ownership
    if character.user_id != current_user.id:
        flash('You can only modify your own characters.', 'error')
        return redirect(url_for('characters.index'))
    
    try:
        db.session.delete(character_item)
        db.session.commit()
        flash('Item removed from inventory!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while removing the item.', 'error')
    
    return redirect(url_for('characters.inventory', character_id=character.id))


# API endpoints for dynamic character creation
@bp.route('/api/proficiencies')
@login_required
def get_available_proficiencies():
    """Get proficiencies available for a race/class combination."""
    race = request.args.get('race', '')
    character_class = request.args.get('class', '')
    proficiencies = []
    
    # Race-specific proficiencies
    race_proficiencies = {
        'Elf': ['Longsword', 'Shortbow', 'Longbow', 'Perception'],
        'Dwarf': ['Battleaxe', 'Handaxe', 'Light Hammer', 'Warhammer'],
        'Human': [],  # Humans get flexible proficiencies
        'Halfling': ['Sling'],
        'Dragonborn': [],
        'Gnome': [],
        'Half-Elf': [],
        'Half-Orc': [],
        'Tiefling': []
    }
    
    # Class-specific proficiencies
    class_proficiencies = {
        'Fighter': ['Simple Weapons', 'Martial Weapons', 'Light Armor', 'Medium Armor', 'Heavy Armor', 'Shields'],
        'Wizard': ['Dagger', 'Dart', 'Sling', 'Quarterstaff', 'Light Crossbow'],
        'Rogue': ['Simple Weapons', 'Hand Crossbow', 'Longsword', 'Rapier', 'Shortsword', 'Light Armor', "Thieves' Tools"],
        'Cleric': ['Simple Weapons', 'Light Armor', 'Medium Armor', 'Shields'],
        'Ranger': ['Simple Weapons', 'Martial Weapons', 'Light Armor', 'Medium Armor', 'Shields'],
        'Paladin': ['Simple Weapons', 'Martial Weapons', 'Light Armor', 'Medium Armor', 'Heavy Armor', 'Shields'],
        'Barbarian': ['Simple Weapons', 'Martial Weapons', 'Light Armor', 'Medium Armor', 'Shields'],
        'Bard': ['Simple Weapons', 'Hand Crossbow', 'Longsword', 'Rapier', 'Shortsword', 'Light Armor'],
        'Druid': ['Light Armor', 'Medium Armor', 'Shields', 'Scimitar', 'Shortsword', 'Simple Weapons'],
        'Monk': ['Simple Weapons', 'Shortsword'],
        'Sorcerer': ['Dagger', 'Dart', 'Sling', 'Quarterstaff', 'Light Crossbow'],
        'Warlock': ['Simple Weapons', 'Light Armor']
    }
    
    # Combine race and class proficiencies
    available_names = set()
    available_names.update(race_proficiencies.get(race, []))
    available_names.update(class_proficiencies.get(character_class, []))
    
    # Get proficiencies from database that match available names
    if available_names:
        proficiencies = Proficiency.query.filter(Proficiency.name.in_(available_names)).all()
    else:
        # If no specific restrictions, return all proficiencies
        proficiencies = Proficiency.query.all()
    
    return jsonify({
        'proficiencies': [{
            'id': prof.id,
            'name': prof.name,
            'type': prof.proficiency_type,
            'description': prof.description
        } for prof in proficiencies]
    })


@bp.route('/api/languages')
@login_required
def get_available_languages():
    """Get languages available for a race/class combination."""
    race = request.args.get('race', '')
    character_class = request.args.get('class', '')
    # Race-specific languages
    race_languages = {
        'Elf': ['Common', 'Elvish'],
        'Dwarf': ['Common', 'Dwarvish'],
        'Human': ['Common'],  # Humans get one additional language of choice
        'Halfling': ['Common', 'Halfling'],
        'Dragonborn': ['Common', 'Draconic'],
        'Gnome': ['Common', 'Gnomish'],
        'Half-Elf': ['Common', 'Elvish'],  # Plus one additional
        'Half-Orc': ['Common', 'Orc'],
        'Tiefling': ['Common', 'Infernal']
    }
    
    # Some classes might provide additional languages
    class_languages = {
        'Druid': ['Druidic'],
        'Cleric': [],  # Depends on domain
        'Wizard': [],  # Can learn through study
    }
    
    base_languages = race_languages.get(race, ['Common'])
    class_bonus = class_languages.get(character_class, [])
    base_languages.extend(class_bonus)
    
    # Get all languages for selection (players can choose additional ones)
    all_languages = Language.query.all()
    
    return jsonify({
        'base_languages': base_languages,
        'languages': [{
            'id': lang.id,
            'name': lang.name,
            'description': lang.description
        } for lang in all_languages]
    })


@bp.route('/api/features')
@login_required
def get_available_features():
    """Get features available for a race/class combination."""
    race = request.args.get('race', '')
    character_class = request.args.get('class', '')
    
    # Get racial features (for now, return all racial features)
    racial_features = Feature.query.filter(
        Feature.feature_type == 'racial'
    ).all()
    
    # Get class features specific to the class
    class_features = Feature.query.filter(
        Feature.feature_type == 'class',
        Feature.source_class.ilike(f'%{character_class}%') if character_class else True
    ).all()
    
    # Get general features available to all
    general_features = Feature.query.filter(
        Feature.feature_type.in_(['general', 'feat'])
    ).all()
    
    # Combine all available features
    features = racial_features + class_features + general_features
    
    return jsonify({
        'features': [{
            'id': feat.id,
            'name': feat.name,
            'source': feat.source_class or feat.feature_type.title(),
            'description': feat.description
        } for feat in features]
    })


@bp.route('/api/spells')
@login_required
def get_available_spells():
    """Get spells available for a class."""
    character_class = request.args.get('class', '')
    # Class spell lists
    class_spell_lists = {
        'Wizard': ['wizard'],
        'Sorcerer': ['sorcerer'],
        'Warlock': ['warlock'],
        'Bard': ['bard'],
        'Cleric': ['cleric'],
        'Druid': ['druid'],
        'Paladin': ['paladin'],
        'Ranger': ['ranger']
    }
    
    # Non-spellcasting classes
    if character_class not in class_spell_lists:
        return jsonify({'spells': []})
    
    # Get spells available to this class (level 0-2 for character creation)
    spells = Spell.query.filter(Spell.level <= 2).all()
    
    return jsonify({
        'spells': [{
            'id': spell.id,
            'name': spell.name,
            'level': spell.level,
            'school': spell.school,
            'description': spell.description[:100] + '...' if len(spell.description) > 100 else spell.description
        } for spell in spells]
    })


@bp.route('/api/races')
@login_required
def get_races():
    """Get all available races."""
    races = [
        'Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn', 
        'Gnome', 'Half-Elf', 'Half-Orc', 'Tiefling'
    ]
    return jsonify(races)


@bp.route('/api/classes')
@login_required
def get_classes():
    """Get all available classes."""
    classes = [
        'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 
        'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 
        'Warlock', 'Wizard'
    ]
    return jsonify(classes)
