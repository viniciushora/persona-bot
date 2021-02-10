import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Cadastro from './pages/Cadastro';
import Item from './pages/Item';
import Habilidade from './pages/Habilidade';

export default function Routes() {
    return (
        <BrowserRouter>
            <Switch>
                <Route path="/" exact component={Cadastro}/>
                <Route path="/item" component={Item}/>
                <Route path="/habilidade" component={Habilidade}/>
            </Switch>
        </BrowserRouter>
    );
}