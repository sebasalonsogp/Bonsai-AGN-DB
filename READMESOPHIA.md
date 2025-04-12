### implement other cigale features...
### sort results by...
### fix select feature... select unique instead of by agn_id
### view selected values (be able to click and see what is selected on sed in pop up)
### if new query is started while old one exits/ not cleared:
1. pop up message asking if they want to clear the old
2. if yes then clean
3. if no then change current rule to include both old and new query 

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