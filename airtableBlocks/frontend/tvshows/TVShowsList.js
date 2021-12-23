import React from 'react';

import { useRecords } from '@airtable/blocks/ui';

export default function TVShowsList(props) {

    const {
        table
    } = props;

    const records = useRecords(table);

    return (
        <div>
            {
                records.map((record, index) => {
                    return (
                        <div key={record.id}>
                            <div>Primary Key value : {record.name}</div>
                        </div>
                    )
                })   
            }
            
        </div>
    )

}