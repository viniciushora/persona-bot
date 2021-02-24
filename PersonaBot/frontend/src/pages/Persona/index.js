import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import { IoIosAddCircle } from 'react-icons/io';

import api from '../../services/api';
import './styles.css';

export default function Persona() {
    const [nome, setNome] = useState('');
    const [link_foto, setLink] = useState('');
    const [nivel, setNivel] = useState('');
    const [fk_arcana_arcana_id, setArcana] = useState(0);
    const [vida, setVida] = useState(0);
    const [sp, setSp] = useState(0);
    const [forca, setForca] = useState(0);
    const [magia, setMagia] = useState(0);
    const [resist, setResist] = useState(0);
    const [agilidade, setAgilidade] = useState(0);
    const [sorte, setSorte] = useState(0);
    const [fisico, setFisico] = useState(0);
    const [arma, setArma] = useState(0);
    const [fogo, setFogo] = useState(0);
    const [gelo, setGelo] = useState(0);
    const [eletrico, setEletrico] = useState(0);
    const [vento, setVento] = useState(0);
    const [psy, setPsy] = useState(0);
    const [nuclear, setNuclear] = useState(0);
    const [bencao, setBencao] = useState(0);
    const [maldicao, setMaldicao] = useState(0);
    const [onipotencia, setOnipotencia] = useState(0);
    const [niveis, setNiveis] = useState([]);
    const [habilidadesPersona, setHabilidadesPersona] = useState([]);
    const [habilidades, setHabilidades] = useState([]);

    const addHabilidade = (e) => {
        e.preventDefault();

        setHabilidadesPersona([...habilidadesPersona, ""])
        setNiveis([...niveis, ""])
    }

    const handleChangeNivel = (e, index) => {
        niveis[index] = e.target.value;
        setNiveis([...niveis]);
        console.log(niveis)
    }

    const handleChangeHabilidade = (e, index) => {
        habilidadesPersona[index] = e.target.value;
        setHabilidadesPersona([...habilidadesPersona]);
        console.log(habilidadesPersona)
    }

    useEffect(() => {
        api.get('habilidade')
        .then(response => {
            setHabilidades(response.data);
        })
    }, []);

    async function handleRegister (e) {
        try{
            e.preventDefault();

            const data = {
                nome,
                link_foto,
                nivel
            };

            const response = await api.post('persona', data);

            const fk_persona_persona_id = response.data['result'];

            const atributos = [vida, sp, forca, magia, resist, agilidade, sorte]
            const fraquezas = [fisico, arma, fogo, gelo, eletrico, vento, psy, nuclear, bencao, maldicao, onipotencia]

            const data1 = {
                fk_arcana_arcana_id,
                fk_persona_persona_id
            }

            const response1 = await api.post('persona_arcana', data1);

            const data2 = {
                fk_persona_persona_id,
                fraquezas
            }

            const response2 = await api.post('reacao_elemental', data2);

            const data3 = {
                fk_persona_persona_id,
                atributos
            }

            const response3 = await api.post('persona_atributo', data3);

            const data4 = {
                fk_persona_persona_id,
                niveis,
                habilidadesPersona
            }

            const response4 = await api.post('habilidade_persona', data4);

            alert('Persona cadastrada com sucesso.');
            document.getElementById("nomePersona").value = "";
            document.getElementById("fotoPersona").value = "";
            document.getElementById("nivelPersona").value = "";

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
                            <h1>Persona</h1>
                        </div>
                        <div class="row">
                            <input class="fix1" id="nomePersona" placeholder="Nome da Habilidade" value={nome} onChange={e => setNome(e.target.value)}/>
                        </div>
                        <div class="row">
                            <input id="fotoPersona" placeholder="Link da Foto da Persona" value={link_foto} onChange={e => setLink(e.target.value)}/>
                        </div>
                        <div class="row">
                            <input class="fix1" id="nivelPersona" placeholder="Nível Inicial da Persona" value={nivel} onChange={e => setNivel(e.target.value)}/>
                        </div>
                        <div class="row">
                            <select id="arcanaPersona" class="fix5 fix2" value={fk_arcana_arcana_id} onChange={e => setArcana(e.target.value)}>
                                <option value="0" selected disabled>Arcana da Persona</option>
                                <option value="1">Tolo</option>
                                <option value="2">Mago</option>
                                <option value="3">Sacerdotisa</option>
                                <option value="4">Imperatriz</option>
                                <option value="5">Imperador</option>
                                <option value="6">Hierofante</option>
                                <option value="7">Amantes</option>
                                <option value="8">Carruagem</option>
                                <option value="9">Justiça</option>
                                <option value="10">Eremita</option>
                                <option value="11">Fortuna</option>
                                <option value="12">Força</option>
                                <option value="13">Enforcado</option>
                                <option value="14">Morte</option>
                                <option value="15">Sobriedade</option>
                                <option value="16">Diabo</option>
                                <option value="17">Torre</option>
                                <option value="18">Estrela</option>
                                <option value="19">Lua</option>
                                <option value="20">Sol</option>
                                <option value="21">Julgamento</option>
                                <option value="22">Mundo</option>
                            </select>
                        </div>
                        <div class="row">
                            <p>HP Inicial</p>
                            <input class="fix2 atributo" id="hpPersona" value={vida} onChange={e => setVida(e.target.value)}/>
                        </div>
                        <div class="row">
                            <p>SP Inicial</p>
                            <input class="fix2 atributo" id="spPersona" value={sp} onChange={e => setSp(e.target.value)}/>
                        </div>
                        <div class="row">
                            <p>Força (St) Inicial</p>
                            <input class="fix2 atributo" id="stPersona" value={forca} onChange={e => setForca(e.target.value)}/>
                        </div>
                        <div class="row">
                            <p>Magia (Ma) Inicial</p>
                            <input class="fix2 atributo" id="maPersona" value={magia} onChange={e => setMagia(e.target.value)}/>
                        </div>
                        <div class="row">
                            <p>Resistência (En) Inicial</p>
                            <input class="fix2 atributo" id="enPersona" value={resist} onChange={e => setResist(e.target.value)}/>
                        </div>
                        <div class="row">
                            <p>Agilidade (Ag) Inicial</p>
                            <input class="fix2 atributo" id="agPersona" value={agilidade} onChange={e => setAgilidade(e.target.value)}/>
                        </div>
                        <div class="row">
                            <p>Sorte (Lu) Inicial</p>
                            <input class="fix2 atributo" id="luPersona" value={sorte} onChange={e => setSorte(e.target.value)}/>
                        </div>
                        <div class="row">
                            <h3>Reação Elemental</h3>
                        </div>
                        <div class="row">
                            <select id="e1" class="fix2" value={fisico} onChange={e => setFisico(e.target.value)}>
                                <option value="0" selected disabled>Físico</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e2" class="fix2" value={arma} onChange={e => setArma(e.target.value)}>
                                <option value="0" selected disabled>Arma de Fogo</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e3" class="fix2" value={fogo} onChange={e => setFogo(e.target.value)}>
                                <option value="0" selected disabled>Fogo</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e4" class="fix2" value={gelo} onChange={e => setGelo(e.target.value)}>
                                <option value="0" selected disabled>Gelo</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e5" class="fix2" value={eletrico} onChange={e => setEletrico(e.target.value)}>
                                <option value="0" selected disabled>Elétrico</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e6" class="fix2" value={vento} onChange={e => setVento(e.target.value)}>
                                <option value="0" selected disabled>Vento</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e7" class="fix2" value={psy} onChange={e => setPsy(e.target.value)}>
                                <option value="0" selected disabled>Psicocinésia (Psy)</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e8" class="fix2" value={nuclear} onChange={e => setNuclear(e.target.value)}>
                                <option value="0" selected disabled>Nuclear</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e9" class="fix2" value={bencao} onChange={e => setBencao(e.target.value)}>
                                <option value="0" selected disabled>Benção</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e10" class="fix2" value={maldicao} onChange={e => setMaldicao(e.target.value)}>
                                <option value="0" selected disabled>Maldição</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <select id="e11" class="fix2" value={onipotencia} onChange={e => setOnipotencia(e.target.value)}>
                                <option value="0" selected disabled>Onipotência</option>
                                <option value="1">Fraco</option>
                                <option value="2">Forte</option>
                                <option value="3">Nulo</option>
                                <option value="4">Drena</option>
                                <option value="5">Reflete</option>
                                <option value="6">Normal</option>
                            </select>
                        </div>
                        <div class="row">
                            <h3>Habilidades</h3>
                        </div>
                        <div class="row">
                            <div class="col-sm-5">
                                <Button class="btn bg-transparent" onClick={addHabilidade}><IoIosAddCircle class="icon-add"/></Button>
                            </div>
                        </div>
                            {
                                niveis.map((level, index) => (
                                    <div key={`hp-${index}`} class="row fix3">
                                        <div class="col-sm-1">
                                            <p>Nível</p>
                                        </div>
                                        <div class="col-sm-2">
                                        <input onChange={(e) => handleChangeNivel(e, index)} value={level} class="fix2"/>
                                        </div>
                                        <div class="col-sm-7">
                                        <select onChange={(e) => handleChangeHabilidade(e, index)}class="fix4">
                                            <option value="0" selected disabled>Habilidade</option>
                                            {
                                                habilidades.map((habilidade, index) => (
                                                    <option key={`hc-${index}`} value={habilidade.habilidade_id}>{habilidade.nome}</option>
                                                ))
                                            }
                                        </select>
                                        </div>
                                    </div>
                                ))
                            }
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