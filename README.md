# RecipeRealms API
A RESTful backend API for managing recipes, tags, products and comments built with Django REST Framework and JWT authentication.

## Features
- User authentication with JWT
- CRUD operations for recipes
- Nested comments per recipe
- Tag and product management
- Image upload for recipes and profile (profile picture)
- Filtering recipes by tags, products and title

## Tech Stack
- Python
- Django & Django REST Framework
- PostgreSQL
- JWT Authentication
- Django ORM
- Linux-based development environment

## API Endpoints

### Authentication
- POST /api/user/register/
- POST /api/user/jwt-login/

### Recipes
- GET /api/recipe/recipes/
- POST /api/recipe/recipes/
- GET /api/recipe/recipes/{id}/
- PATCH /api/recipe/recipes/{id}/
- PUT /api/recipe/recipes/{id}/
- DELETE /api/recipe/recipes/{id}/

### Comments
- GET /api/recipe/recipes/{id}/comments/
- POST /api/recipe/recipes/{id}/post-comment/
- DELETE /api/recipe/recipes/{id}/post-comment/

### User
- GET /api/user/me
- PATCH /api/user/change-password/
- PUT /api/user/change-password/
- PUT /api/user/reset-password/
- POST api/user/me/upload-image/
- PATCH api/user/me/upload-image/

## Installation
1.Clone the repository
`git clone https://github.com/DimitarITZankov/RecipeRealms.git
    cd RecipeRealms`

2.Build and run the docker image
`docker compose up --build`

## How to setup the project
1. After installation, the server will be running on your localhost at: `http://localhost:4000/`
2. You can start exploring all endpoints from the main page: `http://localhost:4000/`

## How to use JWT Authentication
1. First, register a new account at: `http://localhost:4000/api/user/register/`
2. Log in using your credentials at: `http://localhost:4000/api/user/jwt-create/`
3. After logging in successfully, you will receive **two tokens**:
   - `access` token → use this in the **Authorization header** for all requests requiring authentication.
   - `refresh` token → use this to refresh your access token when it expires.
4. Example of using the `access` token in request headers:
  - `Authorization: Bearer <your_access_token>`

# Testing

The project includes **automated tests** for both the **recipe** and **user APIs** to ensure correctness and reliability.

## Recipe API Tests
Tests cover:
- **Public access** – unauthenticated users cannot access recipe endpoints.
- **Private access** – authenticated users can retrieve recipes and see full details.
- **Recipe creation** – can create recipes with:
  - New tags
  - Existing tags
  - Associated products
- **Recipe retrieval** – fetch single recipes with all details.
- **Custom actions** – uploading images and posting/deleting comments.
- **Query filtering** – filtering recipes by tags, products, or title.

## User API Tests
Tests cover:
- **User registration** – creating new users and ensuring passwords are properly handled.
- **Duplicate emails** – prevents creating multiple accounts with the same email.
- **Password validation** – enforces minimum password length.
- **JWT authentication** – ensures login works and returns access and refresh tokens.
- **Invalid credentials** – returns errors for wrong email or password.
- **Endpoint protection** – ensures `/me/` and other protected routes require authentication.

## How to Run Tests
To run all automated tests for the project:

1. Make sure your virtual environment is active and dependencies are installed:

```bash
pip install -r requirements.txt
```

2. Run in the terminal while you are in the project's root:

```bash
docker compose run --rm app sh -c "python manage.py test"
```

### ------------------------------

```md
## Author
Dimitar Zankov  
GitHub: https://github.com/DimitarITZankov  
LinkedIn: https://linkedin.com/in/dimitar-zankov-581081379
