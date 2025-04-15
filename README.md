
# Summary
Service allows to get resounces balance from Tron blockchain network and save it to database

# Installation
### Dependencies
- python  
```sh
python -m pip install -r requirements.txt
```

- uv (installation is unnescessary)  
```sh
uv sync
```

### Apply migrations
Project uses mariadb as database (can be swap replaced with mysql)
- python
```sh
alembic upgrade head
```
- uv 
```sh
uv alembic upgrade head
```

# Start
- python
```sh
python main.py
```
- uv
```sh
uv run main.py
```

# Run tests
- python
```sh
pytest
```
- uv
```sh
uv pytest
```

# Usage
After succesfull run, server will be available at http://localhost:8000 by default  
You can find it's endpoints specification at openapi.yaml
