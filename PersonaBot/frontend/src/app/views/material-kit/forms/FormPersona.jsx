import React, { Component, useState, useEffect } from "react";
import shortId from "shortid";
import { ValidatorForm, TextValidator } from "react-material-ui-form-validator";
import axios from "axios";
import {
  Button,
  Icon,
  Grid,
  InputLabel,
  MenuItem,
  Radio,
  RadioGroup,
  FormControlLabel
} from "@material-ui/core";
import Select from 'react-select'
import "date-fns";

import api from "../../../services/api";
import './styles.css';

class FormPersona extends Component {
  state = {
    nome: "",
    link_foto: "",
    nivel: "",
    fk_arcana_arcana_id: 0,
    vida: "",
    sp: "",
    forca: "",
    magia: "",
    resist: "",
    agilidade: "",
    sorte: "",
    fisico: 6,
    arma: 6,
    fogo: 6,
    gelo: 6,
    eletrico: 6,
    vento: 6,
    psy: 6,
    nuclear: 6,
    bencao: 6,
    maldicao: 6,
    onipotencia: 6,
    niveis: [],
    habilidadesPersona: [],
    habilidades: [],
    personaUltimoId: 0
  };

  limparCampos = event => {
    this.setState({ nome : "" });
    this.setState({ link_foto : "" });
    this.setState({ nivel : "" });
    this.setState({ forca : "" });
    this.setState({ vida : "" });
    this.setState({ sp : "" });
    this.setState({ magia : "" });
    this.setState({ resist : "" });
    this.setState({ agilidade : "" });
    this.setState({ sorte : "" });
    this.setState({ fisico : 6 });
    this.setState({ arma : 6 });
    this.setState({ fogo : 6 });
    this.setState({ gelo : 6 });
    this.setState({ eletrico : 6 });
    this.setState({ vento : 6 });
    this.setState({ psy : 6 });
    this.setState({ nuclear : 6 });
    this.setState({ bencao : 6 });
    this.setState({ maldicao : 6 });
    this.setState({ onipotencia : 6 });
    this.setState({ niveis : [] });
    this.setState({ habilidadesPersona : [] });
  }

  componentDidMount() {
    // custom rule will have name 'isPasswordMatch'
    this.Habilidades();
    this.PersonaId();
    ValidatorForm.addValidationRule("isPositive", value => {
        if (Number(value) > 0){
            return true;
        } else {
            return false;
        }
    });
    ValidatorForm.addValidationRule("isInteger", value => {
        if (parseInt(Number(value)) == value){
            return true;
        } else {
            return false;
        }
    });
  }

  Habilidades() {
    api.get('habilidade').then(response => { this.setState( { habilidades: response.data} )});
  };


  PersonaId() {
    api.get('persona-ultimo-id').then(response => { this.setState( { personaUltimoId: response.data } )});
  }

  handleSubmit = async event => {
    console.log("submitted");

    try{
        const nome = this.state.nome;
        const link_foto = this.state.link_foto;
        const nivel = this.state.nivel;
        const fk_arcana_arcana_id = this.state.fk_arcana_arcana_id;
        const vida = this.state.vida;
        const sp = this.state.sp;
        const forca = this.state.forca;
        const magia = this.state.magia;
        const resist = this.state.resist;
        const agilidade = this.state.agilidade;
        const sorte = this.state.sorte;
        const fisico = this.state.fisico;
        const arma = this.state.arma;
        const fogo = this.state.fogo;
        const gelo = this.state.gelo;
        const eletrico = this.state.eletrico;
        const vento = this.state.vento;
        const psy = this.state.psy;
        const nuclear = this.state.nuclear;
        const bencao = this.state.bencao;
        const maldicao = this.state.maldicao;
        const onipotencia = this.state.onipotencia;
        const niveis = this.state.niveis;
        const habilidadesPersona = this.state.habilidadesPersona;
        const fk_persona_persona_id = this.state.personaUltimoId + 1;

        const data = {
            nome,
            link_foto,
            nivel
        };

        await api.post('persona', data);

        const atributos = [vida, sp, forca, magia, resist, agilidade, sorte]
        const fraquezas = [fisico, arma, fogo, gelo, eletrico, vento, psy, nuclear, bencao, maldicao, onipotencia]

        const data1 = {
            fk_arcana_arcana_id,
            fk_persona_persona_id
        }

        await api.post('persona_arcana', data1);

        const data2 = {
            fk_persona_persona_id,
            fraquezas
        }

        await api.post('reacao_elemental', data2);

        const data3 = {
            fk_persona_persona_id,
            atributos
        }

        await api.post('persona_atributo', data3);

        const data4 = {
            fk_persona_persona_id,
            niveis,
            habilidadesPersona
        }

        await api.post('habilidade_persona', data4);

        this.setState({ personaUltimoId: this.state.personaUltimoId + 1 });

        let notification = {
            id: shortId.generate(),
            heading: "Cadastro",
            icon: {
            name: "description",
            color: "primary"
            },
            timestamp: Date.now(),
            title: "Persona cadastrada com sucesso.",
            subtitle: "ID = " + fk_persona_persona_id + "; Nome: " + nome,
            path: "/"
        }

      axios.post("/api/notification/add", notification);

    } catch (err) {
        let notification = {
            id: shortId.generate(),
            heading: "Cadastro",
            icon: {
              name: "warning",
              color: "primary"
            },
            timestamp: Date.now(),
            title: "Erro no cadastro da Persona",
            subtitle: "Tente novamente, alguma informação foi enviada com erros.",
            path: "/"
        }

        axios.post("/api/notification/add", notification);

        }
    };

    handleChange = event => {
        event.persist();
        this.setState({ [event.target.name]: event.target.value });
    };

    handleChangeSelectArcana = (selectedOption) => {
        this.setState({ fk_arcana_arcana_id: selectedOption.value});
    };

    addHabilidade = event => {
        event.persist();

        this.setState({ habilidadesPersona: [...this.state.habilidadesPersona, ""] } );
        this.setState({ niveis: [...this.state.niveis, ""] })
    }

    handleChangeHabilidade = (selectedOption, index) => {
        this.state.habilidadesPersona[index] = selectedOption.value;
        this.setState({ habilidadesPersona: [...this.state.habilidadesPersona] } );
    }

    handleChangeNivel = (event, index) => {
        this.state.niveis[index] = event.target.value;
        this.setState({ niveis: [...this.state.niveis] } );
    }

    handleRemoveInputHabilidade = (position) => {
        this.setState( { niveis: [...this.state.niveis.filter((_, index) => index != position)] } );
        this.setState( { habilidadesPersona: [...this.state.habilidadesPersona.filter((_, index) => index != position)] } );
    }

  render() {
    let {
        nome,
        link_foto,
        nivel,
        fk_arcana_arcana_id,
        vida,
        sp,
        forca,
        magia,
        resist,
        agilidade,
        sorte,
        fisico,
        arma,
        fogo,
        gelo,
        eletrico,
        vento,
        psy,
        nuclear,
        bencao,
        maldicao,
        onipotencia,
        niveis,
        habilidadesPersona,
        habilidades,
        personaUltimoId
    } = this.state;

    const options_arcana = [
        {value: 1, label: 'Fool'},
        {value: 2, label: 'Mago'},
        {value: 3, label: 'Sacerdotisa'},
        {value: 4, label: 'Imperatriz'},
        {value: 5, label: 'Imperador'},
        {value: 6, label: 'Hierofante'},
        {value: 7, label: 'Amantes'},
        {value: 8, label: 'Carruagem'},
        {value: 9, label: 'Justiça'},
        {value: 10, label: 'Eremita'},
        {value: 11, label: 'Fortuna'},
        {value: 12, label: 'Força'},
        {value: 13, label: 'Enforcado'},
        {value: 14, label: 'Morte'},
        {value: 15, label: 'Sobriedade'},
        {value: 16, label: 'Diabo'},
        {value: 17, label: 'Torre'},
        {value: 18, label: 'Estrela'},
        {value: 19, label: 'Lua'},
        {value: 20, label: 'Sol'},
        {value: 21, label: 'Julgamento'},
        {value: 22, label: 'Mundo'},
    ]

    let options_habilidade = [];
    let campo = {};

    for (let i = 0; i < habilidades.length; i ++) {
        campo = {value: habilidades[i]["habilidade_id"], label: habilidades[i]["nome"]};
        options_habilidade.push(campo);
    }

    return (
      <div>
        <ValidatorForm
          ref="form"
          onSubmit={this.handleSubmit}
          onError={errors => null}
        >
          <Grid container spacing={6}>
            <Grid item lg={6} md={6} sm={12} xs={12}>
                <h5>Informações Gerais</h5>
              <TextValidator
                className="mb-16 w-100"
                label="Nome da Persona"
                onChange={this.handleChange}
                type="text"
                name="nome"
                value={nome}
                validators={[
                  "required",
                  "minStringLength: 2",
                  "maxStringLength: 50"
                ]}
                errorMessages={["Este campo é obrigatório"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Link da foto da Persona"
                onChange={this.handleChange}
                type="text"
                name="link_foto"
                value={link_foto}
                validators={["required"]}
                errorMessages={["Este campo é obrigatório"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Nível inicial da Persona"
                onChange={this.handleChange}
                type="number"
                name="nivel"
                value={nivel}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              <InputLabel>Arcana</InputLabel>
              <Select
                className="mb-16 w-100"
                label="Arcana"
                onChange={this.handleChangeSelectArcana}
                name="fk_arcana_arcana_id"
                options={options_arcana}
                validators={["required"]}
                errorMessages={["Este campo é obrigatório"]}
              >
              </Select>
              <h5>Atributos</h5>
              <TextValidator
                className="mb-16 w-100"
                label="HP inicial"
                onChange={this.handleChange}
                type="number"
                name="vida"
                value={vida}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="SP inicial"
                onChange={this.handleChange}
                type="number"
                name="sp"
                value={sp}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Força (St) inicial"
                onChange={this.handleChange}
                type="number"
                name="forca"
                value={forca}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Magia (Ma) inicial"
                onChange={this.handleChange}
                type="number"
                name="magia"
                value={magia}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Resistência (En) inicial"
                onChange={this.handleChange}
                type="number"
                name="resist"
                value={resist}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Agilidade (Ag) inicial"
                onChange={this.handleChange}
                type="number"
                name="agilidade"
                value={agilidade}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Sorte (Lu) inicial"
                onChange={this.handleChange}
                type="number"
                name="sorte"
                value={sorte}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12} xs={12}>
                <h5>Interação Elemental</h5>
                <InputLabel>Físico</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={fisico}
                    name="fisico"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Arma de Fogo</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={arma}
                    name="arma"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Fogo</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={fogo}
                    name="fogo"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Gelo</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={gelo}
                    name="gelo"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Elétrico</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={eletrico}
                    name="eletrico"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Vento</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={vento}
                    name="vento"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Psicocinésia (Psy)</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={psy}
                    name="psy"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Nuclear</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={nuclear}
                    name="nuclear"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Benção</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={bencao}
                    name="bencao"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Maldição</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={maldicao}
                    name="maldicao"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <InputLabel>Onipotência</InputLabel>
                <RadioGroup
                    className="mb-16"
                    value={onipotencia}
                    name="onipotencia"
                    onChange={this.handleChange}
                    row
                >
                    <FormControlLabel
                    value="1"
                    control={<Radio color="secondary" />}
                    label="Fraco"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="2"
                    control={<Radio color="secondary" />}
                    label="Forte"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="3"
                    control={<Radio color="secondary" />}
                    label="Nulo"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="4"
                    control={<Radio color="secondary" />}
                    label="Drena"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="5"
                    control={<Radio color="secondary" />}
                    label="Reflete"
                    labelPlacement="end"
                    />
                    <FormControlLabel
                    value="6"
                    control={<Radio color="secondary" />}
                    label="Normal"
                    labelPlacement="end"
                    />
                </RadioGroup>
                <h5>Habilidades</h5>
                <Button color="primary" onClick={this.addHabilidade} variant="contained" >
                    <Icon>add</Icon>
                    <span className="pl-8 capitalize">Adicionar Habilidade</span>
                </Button>
                {
                    niveis.map((level, index) => (
                        <>
                        <h6 className="fix1">Habilidade {index + 1}</h6>
                        <TextValidator
                            className="mb-16 w-100"
                            key={`n-${index}`}
                            label="Nível de aprendizado"
                            onChange={(event) => this.handleChangeNivel(event, index)}
                            type="number"
                            name="niveis"
                            value={level}
                            validators={["required", "isNumber", "isInteger", "isPositive"]}
                            errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
                        />
                        <InputLabel>Habilidade</InputLabel>
                        <Select
                            className="mb-16 w-100"
                            label="Habilidade"
                            key={`s-${index}`}
                            onChange={(selectedOption) => this.handleChangeHabilidade(selectedOption, index)}
                            name="habilidadesPersona"
                            options={options_habilidade}
                            validators={["required"]}
                            errorMessages={["Este campo é obrigatório"]}
                        />
                        <Button color="secondary" onClick={() => {this.handleRemoveInputHabilidade(index)}} variant="contained" >
                            <Icon>delete</Icon>
                        </Button>
                        </>
                    ))
                }
            </Grid>
          </Grid>
          <Button color="primary" variant="contained" type="submit">
            <Icon>send</Icon>
            <span className="pl-8 capitalize">Cadastrar</span>
          </Button>
          <Button onClick={this.limparCampos} className="fix2" color="primary" variant="contained">
            <Icon>delete_sweep</Icon>
            <span className="pl-8 capitalize">Limpar campos</span>
          </Button>
        </ValidatorForm>
      </div>
    );
  }
}

export default FormPersona;
