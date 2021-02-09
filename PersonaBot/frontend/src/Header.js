import React from 'react';

import './global.css';

export default function Header() {
    return (
        <header>
            <div class="container-fluid">
                <div class="cabecalho row">
                    <div class="col-sm-5">
                        <img class="img-header" src="https://raw.githubusercontent.com/ViniciusHora1009/persona-bot/main/imagens/persona-bot-circle.png"/> 
                    </div>
                    <div class="col-sm-2">
                    </div>
                    <div class="col-sm-1">
                        <a class="opcao-header" href="/">CADASTRO</a>
                    </div>
                    <div class="col-sm-1">
                    </div>
                    <div class="col-sm-1">
                        <a class="opcao-header" href="/listagem">LISTAGEM</a>
                    </div>
                    <div class="col-sm-2">
                    </div>
                </div>
            </div>
        </header>
    );
}