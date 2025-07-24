# Database Initialization Process

## Overview

The database initialization system provides a robust, automated approach to setting up the D&D 5e database with fallback strategies for data sourcing. The system handles schema creation, data population, and error recovery.

## Components

### DataSourceManager

The `DataSourceManager` class implements a cascading fallback strategy for obtaining D&D 5e reference data:

1. **Primary**: Check local `json_backups/` directory for existing data files
2. **Secondary**: Check `5e-database-repo/` directory, copy files to backups, cleanup repo
3. **Tertiary**: Download fresh data from GitHub (5e-bits/5e-database)

### DatabaseInitializer

The `DatabaseInitializer` class handles database schema creation and data population with user prompts and transaction safety.

## Usage

### Basic Initialization

```bash
python init_db.py
```

### Force Rebuild (Skip Prompts)

```bash
python init_db.py --force
```

### Docker Environment

```bash
docker-compose exec web python init_db.py
```

## Required Data Files

The system requires these D&D 5e SRD JSON files:

- `5e-SRD-Races.json`
- `5e-SRD-Classes.json`
- `5e-SRD-Spells.json`
- `5e-SRD-Equipment.json`
- `5e-SRD-Monsters.json`
- `5e-SRD-Skills.json`
- `5e-SRD-Backgrounds.json`
- `5e-SRD-Features.json`
- `5e-SRD-Proficiencies.json`
- `5e-SRD-Languages.json`

## Data Sourcing Strategy

### 1. Local Backup Check

```python
def check_json_backups(self):
    """Check if all required JSON files exist in json_backups."""
    if not self.json_backups_path.exists():
        return False

    missing_files = []
    for filename in self.required_files:
        if not (self.json_backups_path / filename).exists():
            missing_files.append(filename)

    return len(missing_files) == 0
```

### 2. Repository Copy

```python
def copy_from_repo(self):
    """Copy files from 5e-database-repo to json_backups and cleanup repo."""
    src_path = self.repo_path / "src" / "2014"

    # Copy required files
    for filename in self.required_files:
        src_file = src_path / filename
        dest_file = self.json_backups_path / filename
        if src_file.exists():
            shutil.copy2(src_file, dest_file)

    # Cleanup repo directory
    shutil.rmtree(self.repo_path)
```

### 3. GitHub Download

```python
def download_source_data(self):
    """Download fresh data from GitHub and extract required files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download repository zip
        urlretrieve(self.source_url, zip_file)

        # Extract and copy required files
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_path)

        # Copy files from src/2014/ directory
        for filename in self.required_files:
            shutil.copy2(src_file, dest_file)
```

## Database Population

### Species Data Loading

The system loads D&D races (referred to as "species" in the codebase) with:

- Ability score increases
- Racial traits
- Languages
- Starting proficiencies
- Physical characteristics (speed, size)

### Character Class Loading

Character classes are loaded with:

- Hit die information
- Primary ability scores
- Saving throw proficiencies
- Available skill proficiencies
- Armor and weapon proficiencies
- Spellcasting abilities

## Error Handling

### Data Sourcing Failures

If all data sourcing strategies fail, the system provides manual recovery instructions:

```
❌ All data sourcing strategies failed!
💡 Manual steps:
   1. Check internet connection
   2. Manually download: https://github.com/5e-bits/5e-database
   3. Extract and copy src/*.json files to json_backups/
```

### Database Transaction Safety

All database operations use transactions with rollback on failure:

```python
try:
    db.session.add(species)
    db.session.commit()
    logger.info(f"✅ Successfully loaded {loaded_count} species")
    return True
except Exception as e:
    db.session.rollback()
    logger.error(f"❌ Failed to commit species data: {e}")
    return False
```

### User Prompts

The system prompts users before overwriting existing data:

```
⚠️  Database already contains data. Rebuild? [y/N]:
```

## Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (optional, defaults to SQLite)
- `SECRET_KEY`: Flask secret key for application context

### File Paths

- `json_backups/`: Local data file storage
- `5e-database-repo/`: Temporary repository checkout location
- Source URL: `https://github.com/5e-bits/5e-database/archive/refs/heads/main.zip`

## Logging

The system provides structured logging with different levels:

- **INFO**: General progress information
- **DEBUG**: Detailed operation information
- **WARNING**: Non-fatal issues (missing optional files)
- **ERROR**: Fatal errors requiring intervention

## Troubleshooting

### Common Issues

**Missing JSON Files**
```bash
# Check if files exist
ls json_backups/

# Manual download if needed
wget https://github.com/5e-bits/5e-database/archive/refs/heads/main.zip
unzip main.zip
cp 5e-database-main/src/2014/*.json json_backups/
```

**Database Connection Issues**
```bash
# Check database connectivity
python -c "from project import create_app, db; app = create_app(); app.app_context().push(); print(db.engine.url)"
```

**Permission Issues**
```bash
# Ensure write permissions
chmod -R 755 json_backups/
chmod -R 755 instance/
```

### Debug Mode

For detailed debugging, modify the logging level:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Integration with Development Workflow

The initialization process integrates with:

- **Docker Compose**: Automatic database setup in containers
- **CI/CD Pipeline**: Automated testing with fresh database instances
- **Development Setup**: Quick local environment preparation
- **Testing**: Isolated test database creation

## Best Practices

1. **Always backup** existing data before running `--force`
2. **Verify data integrity** after initialization
3. **Use version control** for custom data modifications
4. **Monitor logs** during initialization for any warnings
5. **Test thoroughly** after any schema changes
