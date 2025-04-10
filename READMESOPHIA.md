### Need to add clear function on query
### Need to fix sed generation after query data
**First, stop any running containers and remove volumes**
   ```bash
   docker-compose -f docker-compose.dev.yml down -v
   ```
**Then start the development environment**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```
**And if you need to see the logs**
   ```bash
   docker-compose -f docker-compose.dev.yml logs -f
   ```