import React from 'react';
import { Link } from 'react-router-dom';

import './styles.css';

export default function Cadastro() {
    return (
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-6 area-botoes">
                    <div class="row">
                        <Link to="/persona" className="link">
                            <button>Persona</button>
                        </Link>
                    </div>
                    <div class="row">
                        <button>Shadow</button>
                    </div>
                    <div class="row">
                        <button>Personagem</button>
                    </div>
                    <div class="row">
                        <Link to="/item" className="link">
                            <button>Item</button>
                        </Link>
                    </div>
                    <div class="row">
                        <Link to="/habilidade" className="link">
                            <button>Habilidade</button>
                        </Link>
                    </div>
                </div>
                <div class="col-sm-6">
                </div>
            </div>
        </div>
    );
}