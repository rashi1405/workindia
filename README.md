# **City Navigator**

# Welcome to the City Navigator Challenge! 👋

## Making Educated Guesses

When working on this City Navigator challenge, you may encounter areas where the requirements aren't completely clear. Rather than getting stuck, make educated guesses and document your assumptions. This approach will help you complete the assignment within the deadline while demonstrating your problem-solving skills.

### How to Document Your Assumptions

1. **Comment your code** - Add clear comments explaining your assumptions directly in the code.
2. **Explain your reasoning** - For each assumption, briefly explain why you made that particular choice.
3. **Document your assumptions here** - List all assumptions you made during the development below:
```
- **Assumption**: [Brief description of assumption]
  - **Reasoning**: [Explanation of why this assumption was made]
- **Assumption**: [Brief description of assumption]
  - **Reasoning**: [Explanation of why this assumption was made]
```

## TLDR Requirements

Build a Django application called **City Navigator** that allows users to:

- **Create and manage 2D maps** (grids) stored in the database.  
- **Determine if a path exists** between two points in a map using **4-directional movement**.

1. Implement the **Map model** in `maps/models.py`.
2. Complete **MapView** for creating, reading, updating, and deleting maps.
3. Complete **MapNavigationView** for determining if a path exists between two points in a map.

---

## **Detailed Requirements**

### 1. Users
- Use Django’s built-in authentication (or a custom setup if you prefer).  
- Each **user** can create multiple maps.  
- (Optional but recommended) Make maps **public** or **private** (private maps visible only to their owner).

### 2. Map Model
In `maps/models.py`, create a model named `Map` (or `CityMap`, if you prefer). It should have:
- **Name**: A unique identifier for the map that is human-readable.
- **Owner**: A relationship to the user who created the map.
- **Layout**: A 2D grid representation of the city with roads and blocked areas.
- **Public** (optional): A flag indicating whether other users can view this map.

Example structure for the layout:

```json
[
  ["R", "R", "#"],
  ["R", "#", "R"],
  ["R", "R", "R"]
]
```
where:
`"R"` = road (traversable)
`"#"` = blocked (impassable)

### 3. MapView

Implement **CRUD operations** for the Map model using Django views (class-based views). Specifically:

- **Create**: Let a user provide a name, and a 2D layout (JSON) for the map.

- **Read**:
  - **ListView**: Show all maps belonging to the current user.
  - **DetailView**: Show a specific map's name and layout.

- **Update**: Allow the user to edit the map's layout.

- **Delete**: Allow the user to delete a map.

Make sure you **respect ownership**:
> Only the owner can update or delete a map (unless you add more complex permissions).


### 4. MapNavigationView

Create a view (e.g., `MapNavigationView`) that:

- Takes a **map ID** (or slug) to identify which map's layout to use.

- Receives **start and end coordinates** (`(row_s, col_s)` and `(row_e, col_e)`) from the user (via GET request).

- Runs a **pathfinding function** to determine if there is a path from start to end. Movement is restricted to up, down, left, right on `"R"` cells only.

- Return **success or failure** based on whether a path exists. Output should be in **JSON format**.


### 5. Testing

Include tests to verify:

- **Model**: Creating a map, ownership, etc.
- **MapView**: Ensuring only owners can edit or delete a map, etc.
- **MapNavigationView**: Checking correctness. Test both reachable and unreachable paths, plus any edge cases you seem fit.

---


## **Setup Instructions**
**0. Prerequisites**
   - Python (recommended 3.8 or higher)
   - pip (Python package manager)

**1. Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

**2. Create and activate a virtual environment**
   ```bash
   # Install virtualenv if not already installed
   pip install virtualenv

   # On Windows
   python -m virtualenv env
   env\Scripts\activate

   # On macOS/Linux
   python3 -m virtualenv env
   source env/bin/activate
   ```

**3. Install dependencies**
   ```bash
   pip install -r requirements.txt
   # Or if no requirements.txt exists:
   pip install django
   ```

**4. Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

**5. Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

**6. Run the development server**
   ```bash
   python manage.py runserver
   ```
   The application will be available at http://127.0.0.1:8000/

**7. Running tests**
   ```bash
   python manage.py test maps
   ```