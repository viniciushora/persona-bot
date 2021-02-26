import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import { IoIosAddCircle } from 'react-icons/io';

import api from '../../services/api';
import './styles.css';

export default function Persona() {
    const [nome, setNome] = useState('');
    const [usuario, setUsuario] = useState('');
    const [exp, setExp] = useState('');
    const [foto, setFoto] = useState('');
    const [personas, setPersonas] = useState([]);
    const [fool, setFool] = useState(-1);
    const [fk_persona_persona_id, setPersonaId] = useState(0);
    const [vida, setVida] = useState('');
    const [energia, setEnergia] = useState('');
    const [nivel, setNivel] = useState(null);
    const [hp, setHp] = useState(null);
    const [sp, setSp] = useState(null);

    useEffect(() => {
        api.get('persona')
        .then(response => {
            setPersonas(response.data);
        });
    }, []);

    useEffect(() => {
        if (fool == 1) {
            document.getElementById("hpPersonagem").style.display = "block";
            document.getElementById("spPersonagem").style.display = "block";
        } else {
            document.getElementById("hpPersonagem").style.display = "none";
            document.getElementById("spPersonagem").style.display = "none";
        }
    }, [fool]);

    async function handleRegister (e) {
        //try{
            e.preventDefault();

            const fk_grupo_grupo_id = 1

            if (fool == 0)  {
                setFool(false);
            } else {
                setFool(true);
            }

            if (fk_persona_persona_id != 0 && hp != null && sp != null){
                setHp(vida);
                setSp(energia);

                const pesquisa = {
                    fk_persona_persona_id
                }

                const response0 = await api.get('persona-nivel', pesquisa);

                setNivel(response0.data['result'])
            } else if (fool == 1 && fk_persona_persona_id != 0 || hp != null || sp != null){
                throw "missingFoolException"
            }

            const persona_equipada = fk_persona_persona_id

            const data = {
                nome,
                fk_grupo_grupo_id,
                usuario,
                fool,
                persona_equipada,
                hp,
                sp,
                nivel
            };

            const response = await api.post('personagem', data);

            const fk_personagem_personagem_id = response.data['result']

            const pesquisa2 = {
                fk_persona_persona_id
            }

            const response2 = await api.post('persona-nivel', pesquisa2);

            setNivel(response2.data['result']);

            const compendium = false;

            const data2 = {
                nivel,
                fk_personagem_personagem_id,
                fk_persona_persona_id,
                compendium
            }

            const response3 = await api.post('personagem_persona', data2)

            const fk_personagem_persona_personagem_persona_id = response3.data['result']

            const data3 = {
                nivel,
                fk_persona_persona_id
            }

            const response4 = await api.post('skills', data3)

            const habilidades = response4.data['habilidades']

            const data4 = {
                fk_personagem_persona_personagem_persona_id,
                habilidades
            }

            const response5 = await api.post('persona_habilidade', data4)

            alert('Personagem cadastrado com sucesso.');
        //} catch (err) {
        //    if (err == "missingFoolException") {
        //        alert('Você definiu a Arcana do Personagem como Fool, logo deve informar o HP e SP iniciais do personagem.');
        //    } else {
        //        alert('Erro no cadastro, tente novamente.');
        //    }
        //}
    }

    return (
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm-6 area-botoes">
                    <form onSubmit={ handleRegister }>
                    <div class="row">
                        <h1>Personagem</h1>
                    </div>
                    <div class="row fix1">
                        <input id="nomePersonagem" placeholder="Nome do personagem" value={nome} onChange={e => setNome(e.target.value)}/>
                    </div>
                    <div class="row">
                        <input id="usuarioPersonagem" placeholder="Nome do usuário (Discord)" value={usuario} onChange={e => setUsuario(e.target.value)}/>
                    </div>
                    <div class="row fix1">
                        <input id="fotoPersonagem" placeholder="Link da foto do personagem" value={foto} onChange={e => setFoto(e.target.value)}/>
                    </div>
                    <div class="row">
                        <select class="fix2" id="foolPersonagem" value={fool} onChange={e => setFool(e.target.value)}>
                            <option value="-1" selected disabled>Arcana Fool?</option>
                            <option value="0">Não</option>
                            <option value="1">Sim</option>
                        </select>
                    </div>
                    <div class="row">
                        <select onChange={e => setPersonaId(e.target.value)}>
                            <option value="0" selected disabled>Persona do personagem</option>
                                {
                                    personas.map((persona, index) => (
                                        <option key={`p-${index}`} value={persona.persona_id}>{persona.nome}</option>
                                    ))
                                }
                        </select>
                    </div>
                    <div class="row">
                        <input id="hpPersonagem" class="invi" placeholder="HP inicial do Personagem" value={vida} onChange={e => setVida(e.target.value)}/>
                    </div>
                    <div class="row">
                        <input id="spPersonagem" class="invi" placeholder="SP inicial do Personagem" value={energia} onChange={e => setEnergia(e.target.value)}/>
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