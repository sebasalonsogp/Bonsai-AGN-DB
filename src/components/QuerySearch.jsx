import { useState } from 'react';
import {QueryBuilder} from 'react-querybuilder';
import 'react-querybuilder/dist/query-builder.css';

// Query uses react-querybuilder https://www.npmjs.com/package/react-querybuilder

export default function QuerySearch() {
    const fields = [
        { name: 'firstName', label: 'First Name' },
        { name: 'lastName', label: 'Last Name' },
      ];
      
      const initialQuery = {
        combinator: 'and',
        rules: [
          { field: 'firstName', operator: 'beginsWith', value: 'Stev' },
          { field: 'lastName', operator: 'in', value: 'Vai,Vaughan' },
        ],
      };

      const [query, setQuery] = useState(initialQuery);

    return(
        <div>
            <QueryBuilder fields={fields} defaultQuery={query} onQueryChange={setQuery}/>
            <p>{JSON.stringify(query)}</p>
        </div>
    );
}