import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Cadastro from './pages/Cadastro';
import Item from './pages/Item';
import Habilidade from './pages/Habilidade';
import Persona from './pages/Persona';
import Shadow from './pages/Shadow';
import Personagem from './pages/Personagem';

export default function Routes() {
    return (
        <BrowserRouter>
            <Switch>
                <Route path="/" exact component={Cadastro}/>
                <Route path="/item" component={Item}/>
                <Route path="/habilidade" component={Habilidade}/>
                <Route path="/persona" component={Persona}/>
                <Route path="/shadow" component={Shadow}/>
                <Route path="/personagem" component={Personagem}/>
            </Switch>
        </BrowserRouter>
    );
}