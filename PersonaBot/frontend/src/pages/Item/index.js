import React, { useState, useEffect } from 'react';

import api from '../../services/api';
import './styles.css';

export default function Item() {
    const [nome, setNome] = useState('');
    const [fk_tipo_item_tipo_id, setTipo] = useState(0);
    const [valor, setValor] = useState('');

    useEffect(() => {
        if (fk_tipo_item_tipo_id>6 && fk_tipo_item_tipo_id < 10) {
            document.getElementById("valorItem").style.display = "block";
        } else {
            document.getElementById("valorItem").style.display = "none";
        }
    }, [fk_tipo_item_tipo_id]);

    async function handleRegister(e) {
        e.preventDefault();
        document.getElementById("nomeItem").value = "";

        var valor_item = null;
        if (valor > 0) {
            valor_item = valor;
        }

        const data = {
            nome,
            fk_tipo_item_tipo_id,
            valor_item
        };

        console.log(data)

        try {
            const response = await api.post('item', data);

            alert('Item cadastrado com sucesso.');
        } catch (err) {
            alert('Erro no cadastro, tente novamente.');
        }
    }

    return (
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-6 area-botoes">
                    <form onSubmit={ handleRegister }>
                    <div class="row">
                            <h1>Item</h1>
                        </div>
                        <div class="row">
                            <input id="nomeItem" placeholder="Nome do item" value={nome} onChange={e => setNome(e.target.value)}/>
                        </div>
                        <div class="row">
                            <select class="fix1" id="tipoItem" value={fk_tipo_item_tipo_id} onChange={e => setTipo(e.target.value)}>
                                <option value="0" selected disabled>Tipo do Item</option>
                                <option value="1">Consumíveis</option>
                                <option value="2">Cartas de Habilidade</option>
                                <option value="3">Materiais</option>
                                <option value="4">Tesouros</option>
                                <option value="5">Essenciais</option>
                                <option value="6">Itens-chave</option>
                                <option value="7">Armas corpo-a-corpo</option>
                                <option value="8">Armas à distância</option>
                                <option value="9">Armadura</option>
                                <option value="10">Acessórios</option>
                                <option value="11">Roupas</option>
                            </select>
                        </div>
                        <div class="row">
                            <input id="valorItem" class="invi" placeholder="Valor do Item (Dano ou Armadura)" value={valor} onChange={e => setValor(e.target.value)}/>
                        </div>
                        <div class="row">
                            <button type="submit">Cadastrar</button>
                        </div>
                    </form>
                </div>
                <div class="col-sm-6">
                </div>
            </div>
        </div>
    );
}