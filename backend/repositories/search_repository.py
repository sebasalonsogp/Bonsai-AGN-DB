from typing import Any, Dict, List, Tuple, Optional
from sqlalchemy import select, and_, or_, text, func, String
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from database.models import SourceAGN, Photometry, RedshiftMeasurement, Classification


class SearchRepository:
    """
    Repository for handling complex search queries across multiple database tables.
    
    This repository implements the data access layer for search functionality,
    supporting complex query conditions from the frontend's QueryBuilder component
    and handling joins across the main AGN data tables.
    """

    async def execute_query(
        self, 
        db: AsyncSession, 
        query_data: Dict[str, Any],
        skip: int = 0,
        limit: int = 100,
        sort_field: Optional[str] = None,
        sort_direction: Optional[str] = "asc"
    ) -> Tuple[List[Dict[str, Any]], int]:
        """
        Execute a complex search query built from the frontend QueryBuilder.
        
        Processes the JSON-based query structure from the frontend QueryBuilder component,
        transforms it into SQL query conditions, and executes the search against the database.
        Handles pagination, sorting, and aggregating results across multiple tables.
        
        Args:
            db: Database session for executing the query
            query_data: Query data object from the frontend QueryBuilder with 'combinator' and 'rules'
            skip: Number of records to skip for pagination
            limit: Maximum number of records to return per page
            sort_field: Field name to sort results by (must exist in the field_map)
            sort_direction: Sort direction, either "asc" or "desc"
            
        Returns:
            A tuple containing:
                - List of result dictionaries with data from all joined tables
                - Total count of matching records (before pagination)
        """
        try:
            # Start with a base query that joins all tables
            stmt = self._build_base_query()
            
            # Apply the query conditions
            stmt = self._apply_query_conditions(stmt, query_data)
            
            # Get total count for pagination (without limit/offset)
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = await db.scalar(count_stmt)
            
            # Apply sorting if a sort field is provided
            if sort_field:
                stmt = self._apply_sorting(stmt, sort_field, sort_direction)
            
            # Apply pagination
            stmt = stmt.offset(skip).limit(limit)
            
            # Execute query
            logger.debug(f"Executing SQL: {stmt}")
            result = await db.execute(stmt)
            rows = result.all()
            
            # Convert to dictionaries
            results = []
            for row in rows:
                source = row.SourceAGN if hasattr(row, 'SourceAGN') else None
                photometry = row.Photometry if hasattr(row, 'Photometry') else None
                redshift = row.RedshiftMeasurement if hasattr(row, 'RedshiftMeasurement') else None
                classification = row.Classification if hasattr(row, 'Classification') else None
                
                # Create a dictionary with all available data
                item = {}
                
                if source:
                    item.update({
                        "agn_id": source.agn_id,
                        "ra": source.ra,
                        "declination": source.declination,
                    })
                
                if photometry:
                    item.update({
                        "band_label": photometry.band_label,
                        "filter_name": photometry.filter_name,
                        "mag_value": photometry.mag_value,
                        "mag_error": photometry.mag_error,
                        "extinction": photometry.extinction,
                    })
                
                if redshift:
                    item.update({
                        "redshift_type": redshift.redshift_type,
                        "z_value": redshift.z_value,
                        "z_error": redshift.z_error,
                    })
                
                if classification:
                    item.update({
                        "spec_class": classification.spec_class,
                        "gen_class": classification.gen_class,
                        "xray_class": classification.xray_class,
                        "best_class": classification.best_class,
                        "image_class": classification.image_class,
                        "sed_class": classification.sed_class,
                    })
                
                results.append(item)
            
            return results, total or 0
            
        except Exception as e:
            logger.error(f"Error executing search query: {str(e)}")
            raise
    
    def _build_base_query(self) -> Select:
        """
        Build a base query that joins all relevant tables for AGN data.
        
        Creates a SQLAlchemy select statement that joins the core tables:
        - SourceAGN (main table with coordinates)
        - Photometry (measurements in different bands/filters)
        - RedshiftMeasurement (redshift values and types)
        - Classification (various classification schemes)
        
        All joins are outer joins to ensure records are returned even if 
        they don't have data in all tables.
        
        Returns:
            SQLAlchemy select statement with all necessary joins
        """
        # Start with source table
        query = (
            select(
                SourceAGN, 
                Photometry, 
                RedshiftMeasurement, 
                Classification
            )
            .outerjoin(Photometry, SourceAGN.agn_id == Photometry.agn_id)
            .outerjoin(RedshiftMeasurement, SourceAGN.agn_id == RedshiftMeasurement.agn_id)
            .outerjoin(Classification, SourceAGN.agn_id == Classification.agn_id)
        )
        
        return query
    
    def _apply_query_conditions(self, stmt: Select, query_data: Dict[str, Any]) -> Select:
        """
        Apply query conditions from the frontend QueryBuilder to the SQL query.
        
        Transforms the JSON query structure into SQLAlchemy query conditions.
        The query_data object follows the react-querybuilder format with a
        'combinator' (and/or) and a list of 'rules' to apply.
        
        Args:
            stmt: Base SQLAlchemy select statement to modify
            query_data: Query structure from frontend with combinator and rules
            
        Returns:
            Updated SQLAlchemy select statement with WHERE conditions applied
        """
        # Check if we have rules to apply
        if not query_data or 'rules' not in query_data or not query_data['rules']:
            return stmt
        
        # Get the combinator (and/or)
        combinator = query_data.get('combinator', 'and').lower()
        
        # Get conditions based on rules
        conditions = self._process_rules(query_data['rules'])
        
        # Apply conditions based on combinator
        if conditions:
            if combinator == 'and':
                stmt = stmt.where(and_(*conditions))
            else:  # 'or'
                stmt = stmt.where(or_(*conditions))
        
        return stmt
    
    def _process_rules(self, rules: List[Dict[str, Any]]) -> List[Any]:
        """
        Process rules from the frontend QueryBuilder into SQLAlchemy conditions.
        
        Recursively processes rules, handling both simple conditions and
        nested rule groups. Each rule contains a field, operator, and value
        that are converted to the appropriate SQLAlchemy condition.
        
        Args:
            rules: List of rule objects from QueryBuilder
                  Each rule has field, operator, value properties or contains nested rules
            
        Returns:
            List of SQLAlchemy condition objects ready to be used in WHERE clauses
        """
        conditions = []
        
        for rule in rules:
            # Handle rule groups (nested conditions)
            if 'rules' in rule:
                nested_conditions = self._process_rules(rule['rules'])
                if nested_conditions:
                    if rule.get('combinator', 'and').lower() == 'and':
                        conditions.append(and_(*nested_conditions))
                    else:  # 'or'
                        conditions.append(or_(*nested_conditions))
                continue
            
            # Handle regular rules
            if all(k in rule for k in ['field', 'operator', 'value']):
                field = rule['field']
                operator = rule['operator']
                value = rule['value']
                
                # Skip if any required part is missing
                if not field or not operator:
                    continue
                
                # Map the field to the appropriate table column
                column = self._get_column_for_field(field)
                if not column:
                    logger.warning(f"Unknown field in query: {field}")
                    continue
                
                # Create the condition based on the operator
                condition = self._create_condition(column, operator, value)
                if condition is not None:  # Only add non-None conditions
                    conditions.append(condition)
                else:
                    logger.warning(f"Skipping rule with field={field}, operator={operator}, value={value} due to invalid condition")
        
        return conditions
    
    def _get_column_for_field(self, field: str) -> Optional[Any]:
        """
        Map a field name from the frontend to the corresponding SQLAlchemy column.
        
        Provides a mapping between frontend field names and the actual database columns
        they represent across different tables. This centralized mapping ensures consistent
        field references throughout the application.
        
        Args:
            field: Field name string from frontend
            
        Returns:
            SQLAlchemy column object or None if the field name isn't recognized
        """
        # Map field names to SQLAlchemy model columns
        field_map = {
            # Source columns
            'agn_id': SourceAGN.agn_id,
            'ra': SourceAGN.ra,
            'declination': SourceAGN.declination,
            
            # Photometry columns
            'band_label': Photometry.band_label,
            'filter_name': Photometry.filter_name,
            'mag_value': Photometry.mag_value,
            'mag_error': Photometry.mag_error,
            'extinction': Photometry.extinction,
            
            # Redshift columns
            'redshift_type': RedshiftMeasurement.redshift_type,
            'z_value': RedshiftMeasurement.z_value,
            'z_error': RedshiftMeasurement.z_error,
            
            # Classification columns
            'spec_class': Classification.spec_class,
            'gen_class': Classification.gen_class,
            'xray_class': Classification.xray_class,
            'best_class': Classification.best_class,
            'image_class': Classification.image_class,
            'sed_class': Classification.sed_class,
        }
        
        return field_map.get(field)
    
    def _create_condition(self, column: Any, operator: str, value: Any) -> Optional[Any]:
        """
        Create a SQLAlchemy condition based on column, operator and value.
        
        Handles various comparison operators and data type conversions to build
        appropriate SQLAlchemy filter conditions. Attempts to convert string values
        to appropriate numeric types for numeric columns.
        
        Args:
            column: SQLAlchemy column object to filter on
            operator: String operator from frontend (e.g., 'equals', 'contains', '>')
            value: Value to compare against, will be converted if necessary
            
        Returns:
            SQLAlchemy condition object or None if an invalid combination is provided
        """
        # Try to convert string values to appropriate types for numeric columns
        try:
            if hasattr(column.type, 'python_type') and column.type.python_type in (int, float):
                if isinstance(value, str) and value.strip():
                    try:
                        if column.type.python_type == int:
                            value = int(value)
                        else:
                            value = float(value)
                    except (ValueError, TypeError):
                        logger.warning(f"Could not convert value '{value}' to {column.type.python_type.__name__} for column {column.name}")
        except Exception as e:
            logger.warning(f"Error checking column type: {str(e)}")
        
        # Handle common operators
        try:
            if operator == 'equals' or operator == '=':
                return column == value
            elif operator == 'notEquals' or operator == '!=':
                return column != value
            elif operator == 'greaterThan' or operator == '>':
                return column > value
            elif operator == 'greaterThanOrEquals' or operator == '>=':
                return column >= value
            elif operator == 'lessThan' or operator == '<':
                return column < value
            elif operator == 'lessThanOrEquals' or operator == '<=':
                return column <= value
            elif operator == 'contains':
                if isinstance(column.type, String):
                    return column.contains(value)
                logger.warning(f"Contains operator not supported for column type {column.type}")
                return None
            elif operator == 'beginsWith':
                if isinstance(column.type, String):
                    return column.startswith(value)
                logger.warning(f"BeginsWith operator not supported for column type {column.type}")
                return None
            elif operator == 'endsWith':
                if isinstance(column.type, String):
                    return column.endswith(value)
                logger.warning(f"EndsWith operator not supported for column type {column.type}")
                return None
            elif operator == 'in':
                # Split comma-separated values for 'in' operator
                if isinstance(value, str):
                    values = [v.strip() for v in value.split(',')]
                    return column.in_(values)
                return column.in_([value])
            elif operator == 'notIn':
                if isinstance(value, str):
                    values = [v.strip() for v in value.split(',')]
                    return ~column.in_(values)
                return ~column.in_([value])
            elif operator == 'null':
                return column.is_(None)
            elif operator == 'notNull':
                return column.isnot(None)
            else:
                logger.warning(f"Unsupported operator: {operator}")
                return None
        except Exception as e:
            logger.error(f"Error creating condition for {column} {operator} {value}: {str(e)}")
            return None
    
    def _apply_sorting(self, stmt: Select, sort_field: str, sort_direction: str = "asc") -> Select:
        """
        Apply sorting to the query based on the specified field and direction.
        
        Applies ordering to the query results and handles NULL values appropriately.
        If the requested sort field doesn't exist in the schema, falls back to the default
        sort by agn_id to ensure consistent ordering.
        
        Args:
            stmt: SQLAlchemy select statement to apply sorting to
            sort_field: Field name to sort by (must exist in field_map)
            sort_direction: Sort direction ("asc" or "desc")
            
        Returns:
            Updated SQLAlchemy select statement with ORDER BY clause
        """
        # Get the column to sort by
        column = self._get_column_for_field(sort_field)
        
        if not column:
            logger.warning(f"Sort field {sort_field} not found in schema, falling back to default sort")
            # Fall back to sorting by AGN ID if the requested field isn't found
            column = SourceAGN.agn_id
        
        # Apply sorting with NULL values always at the bottom
        # Using case statement to handle NULL values
        if sort_direction.lower() == "desc":
            # For descending: NOT NULL values in desc order, then NULL values
            stmt = stmt.order_by(
                column.is_(None).asc(),  # NULLs last (False sorts before True)
                column.desc()
            )
        else:
            # For ascending: NOT NULL values in asc order, then NULL values
            stmt = stmt.order_by(
                column.is_(None).asc(),  # NULLs last (False sorts before True)
                column.asc()
            )
        
        return stmt 