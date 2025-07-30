"""Background model for D&D 5e character backgrounds."""

from project import db


class Background(db.Model):
    """D&D 5e character background model."""
    
    __tablename__ = 'backgrounds'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Background features
    skill_proficiencies = db.Column(db.JSON, default=list)  # List of skill names
    tool_proficiencies = db.Column(db.JSON, default=list)   # List of tool names
    languages = db.Column(db.JSON, default=list)            # List of language choices
    equipment = db.Column(db.JSON, default=list)            # Starting equipment
    
    # Background feature
    feature_name = db.Column(db.String(100))
    feature_description = db.Column(db.Text)
    
    # Suggested characteristics
    personality_traits = db.Column(db.JSON, default=list)   # List of trait options
    ideals = db.Column(db.JSON, default=list)               # List of ideal options
    bonds = db.Column(db.JSON, default=list)                # List of bond options
    flaws = db.Column(db.JSON, default=list)                # List of flaw options
    
    # Optional: Gold variant
    starting_gold = db.Column(db.Integer, default=0)        # In gold pieces
    
    def __repr__(self):
        return f'<Background {self.name}>'
    
    @classmethod
    def get_popular_backgrounds(cls):
        """Get the most commonly used backgrounds."""
        return cls.query.filter(
            cls.name.in_([
                'Acolyte', 'Criminal', 'Folk Hero', 'Noble', 
                'Sage', 'Soldier', 'Charlatan', 'Entertainer'
            ])
        ).all()
