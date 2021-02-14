import React, { useState } from 'react';

import api from '../../services/api';
import './styles.css';

export default function Habilidade() {
    const [nome, setNome] = useState('');
    const [fk_atributo_atributo_id, setAtributo] = useState(0);
    const [fk_intensidade_intensidade_id, setIntensidade] = useState(0);
    const [fk_elemento_elemento_id, setElemento] = useState(0);
    const [vezes, setVezes] = useState('');

    async function handleRegister(e) {
        e.preventDefault();

        const data = {
            nome,
            fk_atributo_atributo_id,
            fk_intensidade_intensidade_id,
            fk_elemento_elemento_id,
            vezes
        };

        console.log(data)

        try {
            const response = await api.post('habilidade', data);

            document.getElementById("nomeHabilidade").value = "";

            alert('Habilidade cadastrada com sucesso.');
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
                            <h1>Habilidade</h1>
                        </div>
                        <div class="row">
                            <input id="nomeHabilidade" placeholder="Nome da Habilidade" value={nome} onChange={e => setNome(e.target.value)}/>
                        </div>
                        <div class="row">
                            <select id="atributoHabilidade" class="fix1" value={fk_atributo_atributo_id} onChange={e => setAtributo(e.target.value)}>
                                <option value="0" selected disabled>Atributo da Habilidade</option>
                                <option value="3">Força (St)</option>
                                <option value="4">Magia (Ma)</option>
                                <option value="5">Resistência (En)</option>
                                <option value="6">Agilidade (Ag)</option>
                                <option value="7">Sorte (Lu)</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="intensidadeHabilidade" value={fk_intensidade_intensidade_id} onChange={e => setIntensidade(e.target.value)}>
                                <option value="0" selected disabled>Intensidade da Habilidade</option>
                                <option value="1">Minúsculo</option>
                                <option value="2">Leve</option>
                                <option value="3">Médio</option>
                                <option value="4">Pesado</option>
                                <option value="5">Severo</option>
                                <option value="6">Colossal</option>
                                <option value="7">Outros</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="elementoHabilidade" class="fix1" value={fk_elemento_elemento_id} onChange={e => setElemento(e.target.value)}>
                                <option value="0" selected disabled>Elemento da Habilidade</option>
                                <option value="1">Físico</option>
                                <option value="2">Arma de Fogo</option>
                                <option value="3">Fogo</option>
                                <option value="4">Gelo</option>
                                <option value="5">Elétrico</option>
                                <option value="6">Vento</option>
                                <option value="7">Psicocinésia (Psy)</option>
                                <option value="8">Nuclear</option>
                                <option value="9">Benção</option>
                                <option value="10">Maldição</option>
                                <option value="11">Onipotência</option>
                                <option value="12">Doença</option>
                                <option value="13">Cura</option>
                                <option value="14">Suporte</option>
                                <option value="15">Passiva</option>
                                <option value="16">Navegação</option>
                            </select>
                        </div>
                        <div class="row">
                            <input id="vezesHabilidade" placeholder="Vezes de Ocorrência" value={vezes} onChange={e => setVezes(e.target.value)}/>
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