import React from 'react';

import { useBase } from '@airtable/blocks/ui';
import TVShowsList from './TVShowsList'

function TVshows() {
    
    const base = useBase();
    const tables = base.tables;

    return (
        <div>
            <div>tv shows component here</div>
            <div>ID : {base.id}</div>
            <div>name : {base.name}</div>

            <div>number of tables: {tables.length}</div>
            
            <h3>Table Information</h3>
            {
                tables.map((table) => {
                    return (
                        <div>
                            <br />
                            <div>Name: {table.name}</div>
                            <div>ID: {table.id}</div>
                            <div>Description: {table.description}</div>

                            <h4>Records Info</h4>
                            <TVShowsList table={table}/>

                        </div>
                    )
                })
            }
        </div>
    )
}

export default TVshows;