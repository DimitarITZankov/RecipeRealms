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
- POST /api/user/token/

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

### ------------------------------

```md
## Author
Dimitar Zankov  
GitHub: https://github.com/DimitarITZankov  
LinkedIn: https://linkedin.com/in/dimitar-zankov-581081379
