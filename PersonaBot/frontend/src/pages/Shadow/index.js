import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import { IoIosAddCircle } from 'react-icons/io';

import api from '../../services/api';
import './styles.css';

export default function Persona() {
    const [fk_persona_persona_id, setPersonaId] = useState(0);
    const [codinome, setCodinome] = useState('');
    const [exp, setExp] = useState('');
    const [dinheiro, setDinheiro] = useState('');
    const [personas, setPersonas] = useState([]);
    const [itens, setItens] = useState([]);
    const [chances, setChances] = useState([]);
    const [dropItens, setDropItens] = useState([]);

    const addDrop = (e) => {
        e.preventDefault();

        setChances([...chances, ""])
        setDropItens([...dropItens, ""])
    }

    const handleChangeChance = (e, index) => {
        chances[index] = e.target.value;
        setChances([...chances]);
    }

    const handleChangeDropItem = (e, index) => {
        dropItens[index] = e.target.value;
        setDropItens([...dropItens]);
    }

    useEffect(() => {
        api.get('persona')
        .then(response => {
            setPersonas(response.data);
        });

        api.get('item')
        .then(response => {
            setItens(response.data);
        })
    }, []);

    async function handleRegister (e) {
        try{
            e.preventDefault();

            const data = {
                codinome,
                fk_persona_persona_id,
                exp,
                dinheiro
            };

            const response = await api.post('shadow', data);

            const fk_shadow_fk_persona_persona_id = response.data['result'];

            const data2 = {
                fk_shadow_fk_persona_persona_id,
                chances,
                dropItens
            }

            const response2 = await api.post('drop', data2);

            alert('Shadow cadastrada com sucesso.');
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
                            <h1>Shadow</h1>
                        </div>
                        <div class="row">
                            <input class="fix1" id="codinomeShadow" placeholder="Codinome da Shadow" value={codinome} onChange={e => setCodinome(e.target.value)}/>
                        </div>
                        <div class="row">
                            <select onChange={e => setPersonaId(e.target.value)}>
                                <option value="0" selected disabled>Persona</option>
                                    {
                                        personas.map((persona, index) => (
                                            <option key={`p-${index}`} value={persona.persona_id}>{persona.nome}</option>
                                        ))
                                    }
                            </select>
                        </div>
                        <div class="row">
                            <div class="col-sm-5">
                                <Button class="btn bg-transparent" onClick={addDrop}><IoIosAddCircle class="icon-add"/></Button>
                            </div>
                        </div>
                            {
                                chances.map((chance, index) => (
                                    <div key={`d-${index}`} class="row fix3">
                                        <div class="col-sm-1">
                                            <p>Chance (%)</p>
                                        </div>
                                        <div class="col-sm-2">
                                            <input onChange={(e) => handleChangeChance(e, index)} value={chance} class="fix2"/>
                                        </div>
                                        <div class="col-sm-7">
                                        <select onChange={(e) => handleChangeDropItem(e, index)}class="fix4">
                                            <option value="0" selected disabled>Item</option>
                                            {
                                                itens.map((item, index) => (
                                                    <option key={`i-${index}`} value={item.item_id}>{item.nome}</option>
                                                ))
                                            }
                                        </select>
                                        </div>
                                    </div>
                                ))
                            }
                        <div class="row">
                            <input class="fix1" id="expShadow" placeholder="Experiência recebida" value={exp} onChange={e => setExp(e.target.value)}/>
                        </div>
                        <div class="row">
                            <input class="fix1" id="dinheiroShadow" placeholder="Dinheiro recebido" value={dinheiro} onChange={e => setDinheiro(e.target.value)}/>
                        </div>
                        <div class="row">
                            <button type="submit">Finalizar Cadastro</button>
                        </div>
                    </form>
                </div>
                <div class="col-sm-6">
                </div>
            </div>
        </div>
    );
}