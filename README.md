# OrbitQuery - Database Performance Intelligence Platform

A full-stack Django application that demonstrates database performance optimisation techniques, including N+1 query detection and PostgreSQL index optimisation, using real space-launch data from Launch Library 2.

## Features

- **Launch Explorer**: Browse and search real launch data from Launch Library 2
- **Performance Lab**: Compare baseline (N+1) queries against optimised ORM queries
- **Index Lab**: Demonstrate PostgreSQL index impact using EXPLAIN ANALYZE
- **Benchmark History**: Track and analyse performance improvements over time
- **REST API**: Full API with OpenAPI documentation
- **Interactive Dashboard**: Real-time statistics and visualisations

## Technology Stack

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL 15
- **Frontend**: Django templates, Bootstrap 5, Chart.js
- **Testing**: pytest-django
- **API Documentation**: drf-spectacular

## Setup Instructions

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd orbitquery
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Start PostgreSQL with Docker:
```bash
docker-compose up -d
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Import launch data:
```bash
python manage.py sync_launches --limit 50
```

9. Run the development server:
```bash
python manage.py runserver
```

10. Access the application at http://localhost:8000

## Usage

### Importing Launch Data

Use the management command to import launch data from Launch Library 2:

```bash
# Import 50 launches (default)
python manage.py sync_launches

# Import 100 launches
python manage.py sync_launches --limit 100

# Import with pagination offset
python manage.py sync_launches --limit 50 --offset 50
```

### Running Performance Benchmarks

1. Navigate to the Performance Lab at `/performance/lab/`
2. Select a record limit and strategy
3. Click "Run Benchmark"
4. View the results and SQL queries

### Running Index Benchmarks

1. Navigate to the Index Lab at `/performance/index-lab/`
2. Run a baseline benchmark
3. Create an index using Django migrations:
```bash
python manage.py makemigrations launches
python manage.py migrate
```
4. Run the benchmark again to compare

### API Documentation

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

## Testing

Run tests with pytest:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=launches --cov=performance
```

## Project Structure

```
orbitquery/
├── config/              # Django project configuration
├── launches/            # Launch data app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── serializers.py   # DRF serializers
│   ├── services/        # API client
│   └── management/      # Management commands
├── performance/         # Performance benchmarking app
│   ├── models.py        # Benchmark models
│   ├── services.py      # Benchmark logic
│   └── views.py         # Performance views
├── templates/           # HTML templates
├── static/              # CSS, JS, images
└── tests/               # Test files
```

## Database Schema

### Launch Models

- **Launch**: Main launch record with foreign keys to related entities
- **LaunchStatus**: Launch status (Go, Success, Failure, etc.)
- **LaunchLocation**: Geographic launch location
- **LaunchPad**: Specific launch pad within a location
- **LaunchServiceProvider**: Company or agency conducting the launch
- **Mission**: Mission details and objectives
- **DataSyncRun**: Track import/synchronisation history

### Performance Models

- **BenchmarkRun**: Stores benchmark results including query counts, execution times, and query plans

## Demonstrated Skills

- Django ORM and relationship management
- N+1 query detection and optimisation
- PostgreSQL indexing and query planning
- REST API design and documentation
- Performance profiling and benchmarking
- Test-driven development
- Production deployment configuration

## API Endpoints

- `GET /api/launches/` - List all launches (paginated)
- `GET /api/launches/{id}/` - Retrieve single launch
- `GET /api/stats/` - Dashboard statistics
- `GET /api/history/` - Benchmark history

## Security Notes

- Never commit `.env` or real credentials
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` appropriately
- Use environment-specific database credentials

## Deployment

For production deployment:

1. Set environment variables for production
2. Use Gunicorn as the WSGI server:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```
3. Configure static file serving (nginx, whitenoise, etc.)
4. Use a production PostgreSQL instance
5. Enable SSL/TLS
6. Configure proper logging and monitoring

## License

MIT License

## Acknowledgments

- Launch data provided by [Launch Library 2](https://ll.thespacedevs.com/) by The Space Devs
- Built with Django and PostgreSQL
