# OrbitQuery - Project Summary for Resume

## One-Line Description
OrbitQuery is a full-stack Django application that demonstrates database performance optimisation techniques using real space-launch data from Launch Library 2.

## Technical Skills Demonstrated

### Backend Development
- **Python & Django 5.0**: Built a complete web application with models, views, serializers, and management commands
- **Django ORM**: Designed relational database models with foreign keys, indexes, and complex relationships
- **PostgreSQL**: Implemented production-grade database with migrations, indexes, and query optimisation
- **REST API**: Created RESTful endpoints with Django REST Framework and OpenAPI documentation
- **Performance Optimisation**: Identified and resolved N+1 query problems using select_related() and prefetch_related()
- **Database Indexing**: Demonstrated index impact using EXPLAIN ANALYZE and performance benchmarking

### Data Integration
- **API Integration**: Integrated with Launch Library 2 API with pagination, error handling, and data validation
- **Data Synchronisation**: Built management command for safe upserts and duplicate prevention
- **Data Modeling**: Normalised database schema supporting complex relationships (launches, providers, locations, missions)

### Testing & Quality
- **Automated Testing**: Wrote unit tests with pytest-django for models and services
- **Test Coverage**: Ensured data integrity, uniqueness constraints, and API contract validation
- **CI/CD Ready**: Project structured for continuous integration with proper test configuration

### DevOps & Deployment
- **Docker Compose**: Containerised PostgreSQL for reproducible development environment
- **Environment Management**: Used python-dotenv for secure configuration management
- **Production Configuration**: Prepared settings for deployment with Gunicorn, static files, and security best practices
- **Git Workflow**: Followed conventional commit practices with meaningful commit messages

### Frontend Development
- **Django Templates**: Built responsive, accessible HTML templates with proper inheritance
- **CSS Design**: Created modern dark-themed UI with custom CSS and Bootstrap 5
- **Interactive Features**: Implemented real-time benchmarking with live result display
- **User Experience**: Designed intuitive navigation, filters, and pagination for data exploration

## Resume Description

**OrbitQuery - Database Performance Intelligence Platform**
Built a full-stack Django application demonstrating database performance optimisation using real space-launch data from Launch Library 2. Implemented N+1 query detection and resolution using Django ORM optimisation techniques (select_related, prefetch_related). Created PostgreSQL index lab with EXPLAIN ANALYZE to measure query performance improvements. Developed REST API with OpenAPI documentation, automated testing with pytest, and production-ready deployment configuration with Docker Compose. Successfully imported 100+ launch records with complex relational data, reducing query count by 95% through ORM optimisation.

## GitHub Repository Description

OrbitQuery is a production-quality Django application that demonstrates database performance optimisation techniques. Features include N+1 query detection and resolution, PostgreSQL index optimisation with EXPLAIN ANALYZE, REST API with OpenAPI docs, automated testing, and a modern dark-themed dashboard. Uses real space-launch data from Launch Library 2 API to demonstrate practical performance improvements.

## Five Interview Questions with Answers

### 1. How did you identify and fix the N+1 query problem?

**Answer**: I used Django Debug Toolbar to monitor query counts during page loads. I noticed that the launch list page was issuing one additional query per launch to access related objects (status, provider, location, mission). I fixed this by using `select_related()` for foreign key relationships and `prefetch_related()` for many-to-many relationships, reducing queries from 51 to 3 for a 50-record dataset.

### 2. How do you measure database performance improvements?

**Answer**: I built a benchmarking service that runs both baseline and optimised query strategies multiple times and records median execution times. I capture SQL query counts using Django's `CaptureQueriesContext`, measure execution time with `time.perf_counter()`, and use PostgreSQL's EXPLAIN ANALYZE to examine query plans. This allows me to quantify improvements and compare before/after scenarios.

### 3. How do you handle API data integrity and updates?

**Answer**: I use Django's `update_or_create()` method with external identifiers to ensure no duplicates during repeated imports. The sync command runs in database transactions to prevent partial updates, handles nullable API fields safely, and records sync history including counts of created, updated, and skipped records. This ensures data consistency even if the API is temporarily unavailable.

### 4. What is your approach to database indexing?

**Answer**: I start by analysing query patterns in the application, particularly for frequently filtered or sorted fields like `net` (launch date) and `status`. I use EXPLAIN ANALYZE to examine query plans and identify sequential scans that could benefit from indexes. I create indexes through Django migrations, measure performance before and after, and document the actual improvement rather than assuming every index helps. For small datasets, sequential scans may be faster, so I rely on measurements.

### 5. How do you ensure the application is production-ready?

**Answer**: I follow security best practices: environment variables for secrets, DEBUG=False in production, proper ALLOWED_HOSTS configuration, and CSRF protection. I use Gunicorn as the WSGI server, configure static file serving, and prepare deployment documentation. The project includes automated tests, Docker Compose for reproducible environments, comprehensive README with setup instructions, and proper .gitignore to exclude sensitive files.

## How to Demonstrate During Project Review

### N+1 Query Experiment
1. Navigate to `/performance/lab/`
2. Run a baseline benchmark with 50 records - observe ~51 queries
3. Run an optimised benchmark with the same limit - observe ~3 queries
4. Show the 95% query reduction and improved execution time
5. Display the SQL queries to demonstrate the difference

### Index Experiment
1. Navigate to `/performance/index-lab/`
2. Run a baseline benchmark on date-filtered queries
3. Show the EXPLAIN ANALYZE output (sequential scan)
4. Apply the index migration: `python manage.py migrate launches 0004`
5. Run the benchmark again - show improved execution time
6. Display the new query plan (index scan)
7. Revert if needed: `python manage.py migrate launches 0003`

## Known Limitations and Future Improvements

### Current Limitations
- Benchmark requires authenticated user (can be made optional for read-only benchmarks)
- Small dataset may not show significant index benefits
- No caching layer implemented (Redis could be added)
- No background task queue for scheduled syncs (Celery could be added)
- Limited chart visualisations (Chart.js integration could be expanded)

### Future Improvements
- Add Celery for scheduled data synchronisation
- Implement Redis caching for frequently accessed data
- Add more sophisticated visualisations with D3.js
- Implement user authentication and authorisation for benchmark runs
- Add API rate limiting and pagination optimisation
- Create Docker production image for easy deployment
- Add CI/CD pipeline with GitHub Actions
- Implement more complex query patterns for benchmarking
