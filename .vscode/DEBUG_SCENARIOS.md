# Debug Configuration for D&D Character Sheet Application

## Debugging Scenarios Setup Complete! 🎯

Your VS Code debugging environment is now configured with specific scenarios for your D&D application:

### 🎲 Available Debug Configurations:

1. **🎯 Flask App (Local Development)**
   - Standard local development debugging
   - Includes database URL and debug environment
   - Pre-launch task checks PostgreSQL status

2. **🐳 Flask App (Docker Attach)**
   - Attach to running Docker container
   - For debugging containerized application
   - Path mapping included for container debugging

3. **🗃️ Database Schema Creation**
   - Debug database table creation
   - Test schema migrations
   - Validate model relationships

4. **🎲 Character Creation Debug**
   - Specifically for character creation workflows
   - Opens character creation page after launch
   - Enhanced environment variables for character debugging

5. **📊 D20 SRD Data Import**
   - Debug data scraping and import processes
   - Test reference data population
   - Validate scraped data integrity

6. **🔍 API Endpoints Testing**
   - Debug API routes and responses
   - Test character filtering endpoints
   - Validate JSON serialization

7. **🧪 Run Unit Tests**
   - Debug unit test execution
   - Focused on individual component testing
   - Enhanced error reporting

8. **🔧 Run Functional Tests**
   - Debug full application workflows
   - Test user interactions end-to-end
   - Integration testing support

9. **🎯 Debug Specific Test**
   - Interactive test file selection
   - Debug single test files or methods
   - Detailed error tracing

10. **🛡️ Character Model Validation**
    - Custom debug script for character models
    - Tests all backstory fields
    - Validates relationships and calculations
    - Breakpoint set at entry for step-through debugging

11. **📝 Flask Routes Debug**
    - Debug Flask routing and request handling
    - Enhanced route debugging environment
    - Request/response cycle analysis

### 🛠️ Key Features:

- **Emojis in config names** for easy identification
- **Environment-specific settings** for each scenario
- **Pre/post-launch tasks** for automation
- **Enhanced error reporting** with problem matchers
- **Path mapping** for Docker debugging
- **Input prompts** for interactive debugging

### 🚨 Common Debug Breakpoints to Set:

#### Character Creation:
- `project/characters.py` - Character creation route
- `project/models.py` - Character model validation
- `debug_character_validation.py` - Model testing functions

#### API Endpoints:
- Character filtering logic
- Race/class data retrieval
- JSON serialization methods

#### Database Operations:
- Model save operations
- Relationship handling
- Query execution

### 🎯 Debug Workflow Recommendations:

1. **Start with Database Schema Creation** to ensure clean state
2. **Use Character Model Validation** to test model logic
3. **Run Character Creation Debug** for UI workflow testing
4. **Use API Endpoints Testing** for backend validation
5. **Run tests** to validate overall functionality

### 🔧 Tasks Available:

- `check-postgres`: Verify database is running
- `start-postgres`: Start PostgreSQL container
- `run-all-tests`: Execute full test suite
- `lint-python`: Code quality checks
- `format-python`: Auto-format code
- `create-test-db`: Set up test database
- `populate-test-data`: Load reference data

### 💡 Pro Tips:

- Use `justMyCode: false` to debug into libraries
- Set `stopOnEntry: true` for immediate debugging
- Use the "Current File Debug" for quick script testing
- Environment variables are pre-configured for each scenario
- Problem matchers will highlight errors in VS Code

Ready to debug your D&D application! 🚀
