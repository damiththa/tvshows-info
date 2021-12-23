import {initializeBlock} from '@airtable/blocks/ui';
import React from 'react';
import TVshows from './tvshows/TVshows'

function TVShowsBlock() {
    return (
        <TVshows />
    )
}

initializeBlock(() => <TVShowsBlock />);
