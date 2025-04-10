### Need add a solo sed generation function... 
### Need to improve sed style
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