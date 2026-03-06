# Multi-Workspace Setup Guide

## Overview

This guide walks through adding new ClickUp workspaces to the multi-workspace Notion migration system. Each workspace can route tasks to different Notion data sources based on configurable classification rules.

## Prerequisites

- Access to Notion workspace with integration permissions
- ClickUp workspace ID to be migrated
- Understanding of task types in the ClickUp workspace
- Notion databases/collections ready for migration target

## Quick Setup Checklist

- [ ] Identify ClickUp workspace ID and task types
- [ ] Create or identify target Notion databases
- [ ] Obtain Notion data source IDs
- [ ] Configure workspace mapping in `production/config/conf.py`
- [ ] Define classification rules for task types
- [ ] Test configuration with validation utilities
- [ ] Update DAG parameters to include new workspace
- [ ] Run test migration with limited batches

## Setup Process Overview

### 1. Workspace Analysis
Analyze the ClickUp workspace to understand task patterns and types.

### 2. Notion Database Preparation
Set up target Notion databases and obtain their data source IDs.

### 3. Configuration Implementation
Add workspace mapping configuration with classification rules.

### 4. Validation and Testing
Validate configuration and run test migrations.

### 5. Production Deployment
Deploy to production with monitoring.

## Configuration Steps

### Step 1: Identify Workspace Requirements

1. **Get ClickUp Workspace ID**
   ```bash
   # Found in ClickUp URL: https://app.clickup.com/WORKSPACE_ID/
   # Example: 20391307
   ```

2. **Analyze Task Patterns**
   - Review existing tasks in the workspace
   - Identify common task naming patterns
   - Determine logical task type categories
   - Note any special classification requirements

3. **Define Task Types**
   ```
   Example for Product Planning workspace:
   - problem: User issues, requirements, challenges
   - solution: Proposed solutions, approaches
   - bug: Defects, fixes, errors

   Example for Engineering workspace:
   - dev_task: Implementation tasks, features
   - tech_design: Architecture, specifications
   ```

### Step 2: Configure Workspace Mapping

1. **Edit Configuration File**
   Open `/airflow/dags/production/config/conf.py`

2. **Add Workspace Configuration**
   ```python
   # Add to WORKSPACE_DATA_SOURCE_MAPPINGS dictionary
   "YOUR_WORKSPACE_ID": {
       "workspace_name": "Your Workspace Name",
       "data_sources": {
           "task_type_1": "12345678-90ab-cdef-1234-567890abcdef",
           "task_type_2": "87654321-ba09-fedc-4321-0987654321ba"
       },
       "classification_rules": {
           "task_type_1": [
               r"keyword1",
               r"pattern.*with.*regex",
               r"\b(word1|word2)\b"
           ],
           "task_type_2": [
               r"different.*pattern",
               r"specific\s+words"
           ]
       },
       "default_data_source": "task_type_1"
   }
   ```

3. **Update Target Spaces**
   ```python
   # Add workspace ID to TARGET_SPACES dictionary
   TARGET_SPACES = {
       'existing_id_1': 'Existing Workspace',
       'existing_id_2': 'Another Workspace',
       'YOUR_WORKSPACE_ID': 'Your Workspace Name'  # Add this line
   }
   ```

### Step 3: Create Classification Rules

1. **Pattern Design Principles**
   - Use case-insensitive regex patterns
   - Include word boundaries for precise matching
   - Test patterns against sample task names
   - Order patterns from specific to general

2. **Common Pattern Examples**
   ```python
   # Simple word matching
   r"problem"              # Matches "problem" anywhere
   r"\bproblem\b"          # Matches whole word "problem" only

   # Multiple alternatives
   r"(bug|defect|error)"   # Matches any of these words

   # Pattern with numbers
   r"solution \d+"         # Matches "solution 1", "solution 2", etc.

   # Complex patterns
   r"(fix|resolve).*bug"   # "fix the bug", "resolve this bug"
   ```

3. **Testing Patterns**
   ```python
   import re

   # Test your patterns
   pattern = r"problem"
   test_names = ["User login problem", "Solution for problem", "Bug fix"]

   for name in test_names:
       if re.search(pattern, name, re.IGNORECASE):
           print(f"MATCH: {name}")
   ```

## Data Source Discovery

### Step 4: Obtain Notion Data Source IDs

1. **Method 1: Extract from Notion URLs**
   ```bash
   # Navigate to your Notion database in browser
   # Copy URL from address bar
   # Example URL:
   https://www.notion.so/workspace/Database-Name-12345678-90ab-cdef-1234-567890abcdef?v=view-id

   # Data source ID is the UUID in the URL:
   12345678-90ab-cdef-1234-567890abcdef
   ```

2. **Method 2: Use Notion API Discovery**
   ```python
   # Create discovery script
   import requests
   from production.config.conf import Config

   def discover_databases():
       headers = {
           "Authorization": f"Bearer {Config.NOTION_API_TOKEN}",
           "Notion-Version": "2025-09-03"
       }

       response = requests.post(
           "https://api.notion.com/v1/search",
           headers=headers,
           json={"filter": {"property": "object", "value": "database"}}
       )

       databases = response.json().get("results", [])
       for db in databases:
           title = db.get("title", [{}])[0].get("text", {}).get("content", "Untitled")
           print(f"Database: {title}")
           print(f"ID: {db['id']}")
           print("---")

   discover_databases()
   ```

### Step 5: Validate Data Source IDs

1. **Format Validation**
   ```python
   from production.utils.data_source_validator import DataSourceValidator

   # Validate UUID format
   data_source_id = "12345678-90ab-cdef-1234-567890abcdef"
   validation = DataSourceValidator.validate_data_source_format(data_source_id)

   if validation['valid']:
       print("✅ Valid data source ID format")
   else:
       print("❌ Invalid format:", validation['errors'])
   ```

2. **Accessibility Test**
   ```python
   # Test if integration can access the database
   import requests
   from production.config.conf import Config

   def test_database_access(data_source_id):
       headers = {
           "Authorization": f"Bearer {Config.NOTION_API_TOKEN}",
           "Notion-Version": "2025-09-03"
       }

       response = requests.get(
           f"https://api.notion.com/v1/databases/{data_source_id}",
           headers=headers
       )

       if response.status_code == 200:
           db_info = response.json()
           print(f"✅ Accessible: {db_info.get('title', [{}])[0].get('text', {}).get('content', 'Database')}")
           return True
       else:
           print(f"❌ Access denied: {response.status_code}")
           return False
   ```

### Step 6: Map Task Types to Data Sources

1. **Create Mapping Table**
   ```
   Task Type    | Purpose                    | Notion Database ID
   -------------|----------------------------|-------------------
   problem      | User issues, requirements  | uuid-for-problems-db
   solution     | Proposed solutions         | uuid-for-solutions-db
   bug          | Defects and fixes         | uuid-for-bugs-db
   ```

2. **Verify Each Mapping**
   - Ensure each task type has a corresponding Notion database
   - Test integration access to each database
   - Confirm database schema matches expected structure

## Next Steps

Continue with:

- **Validation Steps**: Testing configuration before production deployment

## Quick Reference

### Configuration Template
```python
"NEW_WORKSPACE_ID": {
    "workspace_name": "Workspace Name",
    "data_sources": {
        "task_type_1": "notion-uuid-1",
        "task_type_2": "notion-uuid-2"
    },
    "classification_rules": {
        "task_type_1": ["pattern1", "pattern2"],
        "task_type_2": ["pattern3", "pattern4"]
    },
    "default_data_source": "task_type_1"
}
```

### Testing Commands
```bash
# Validate configuration
airflow dags trigger test_task_router

# Test classification
airflow dags trigger test_task_classifier

# Test migration (limited)
airflow dags trigger clickup_to_notion_migration --conf '{"target_spaces": ["NEW_WORKSPACE_ID"], "max_batches": 1}'
```