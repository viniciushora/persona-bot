import React, { Component, useState, useEffect } from "react";
import shortId from "shortid";
import { ValidatorForm, TextValidator } from "react-material-ui-form-validator";
import axios from "axios";
import {
  Button,
  Icon,
  Grid,
  InputLabel,
  MenuItem
} from "@material-ui/core";
import Select from 'react-select'
import "date-fns";

import api from "../../../services/api";
import './styles.css';

class FormPersonagem extends Component {
  state = {
    nome: "",
    usuario: "",
    foto: "",
    personas: [],
    fool: 1,
    fk_persona_persona_id: 0,
    vida: "",
    energia: "",
    nivel: null,
    hp: null,
    sp: null,
    personagemUltimoId: 0,
    personagemPersonaUltimoId: 0,
    habilidadesPersona: []
  };

  limparCampos = event => {
    this.setState({ nome : "" });
    this.setState({ usuario : "" });
    this.setState({ foto : "" });
    this.setState({ vida : "" });
    this.setState({ energia : "" });
  }

  componentDidMount() {
    // custom rule will have name 'isPasswordMatch'
    this.Personas();
    this.PersonagemId();
    this.PersonagemPersonaId();
    this.HabilidadesPersona();
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
      ValidatorForm.addValidationRule("isPasswordMatch", value => {
        if (value !== this.state.password) {
          return false;
        }
        return true;
      });
    }

  Personas() {
    api.get('persona').then(response => { this.setState( { personas: response.data} )});
  };

  PersonagemId() {
    api.get('personagem-ultimo-id').then(response => { this.setState( { personagemUltimoId: response.data } )});
  }

  PersonagemPersonaId() {
    api.get('personagem_persona-ultimo-id').then(response => { this.setState( { personagemPersonaUltimoId: response.data } )});
  }

  HabilidadesPersona() {
    api.get('skills').then(response => { this.setState( { habilidadesPersona: response.data } )});
  }

  nivelPersona(persona_id) {
    let nivel = false;
    for (let i = 0; i < this.state.personas.length; i ++) {
      if (this.state.personas[i]["persona_id"] == persona_id) {
        nivel = this.state.personas[i]["nivel"]
      }
    }
    return nivel;
  }

  habilidades(nivel, persona_id){
    var habilidades = [];
    for (var i = 0; i < this.state.habilidadesPersona.length; i ++) {
      if (this.state.habilidadesPersona[i]["nivel"] == nivel && this.state.habilidadesPersona[i]["fk_persona_persona_id"] == persona_id){
        habilidades.push(this.state.habilidadesPersona[i]["fk_habilidade_habilidade_id"])
      }
    }
    return habilidades;
  }

  componentWillUnmount() {
    // remove rule when it is not needed
    ValidatorForm.removeValidationRule("isPasswordMatch");
  }

  handleSubmit = async event => {
    console.log("submitted");

    try{
      const nome = this.state.nome;
      const usuario = this.state.usuario;
      const foto = this.state.foto;
      const personas = this.state.personas;
      let fool = this.state.fool;
      const fk_persona_persona_id = this.state.fk_persona_persona_id;
      const vida = this.state.vida;
      const energia = this.state.energia;
      var nivel = this.state.nivel;
      var hp = this.state.hp;
      var sp = this.state.sp;

      const fk_grupo_grupo_id = 1

      if (fool == 1)  {
        fool = false;
      } else {
        fool = true;
      }

      if (fk_persona_persona_id != 0 && hp != null && sp != null){
        hp = vida;
        sp = energia;

        nivel = this.nivelPersona(fk_persona_persona_id)

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
          foto,
          hp,
          sp,
          nivel
      };

      await api.post('personagem', data);

      const fk_personagem_personagem_id = this.state.personagemUltimoId + 1;

      nivel = this.nivelPersona(fk_persona_persona_id)

      const compendium = false;

      const data2 = {
          nivel,
          fk_personagem_personagem_id,
          fk_persona_persona_id,
          compendium
      }

      await api.post('personagem_persona', data2);

      const fk_personagem_persona_personagem_persona_id = this.state.personagemPersonaUltimoId + 1;

      const data3 = {
          nivel,
          fk_persona_persona_id
      }

      const habilidades = this.habilidades(nivel, fk_persona_persona_id);

      const data4 = {
          fk_personagem_persona_personagem_persona_id,
          habilidades
      }

      await api.post('persona_habilidade', data4);

      let notification = {
        id: shortId.generate(),
        heading: "Cadastro",
        icon: {
          name: "description",
          color: "primary"
        },
        timestamp: Date.now(),
        title: "Personagem cadastrado com sucesso.",
        subtitle: "ID = " + fk_personagem_personagem_id + "; Nome: " + nome,
        path: "/"
      }

      axios.post("/api/notification/add", notification);

      console.log(notification)

    } catch (err) {

        if (err == "missingFoolException") {
          let notification = {
            id: shortId.generate(),
            heading: "Cadastro",
            icon: {
              name: "warning",
              color: "primary"
            },
            timestamp: Date.now(),
            title: "Erro no cadastro de personagem",
            subtitle: "Você definiu a Arcana do Personagem como Fool, logo deve informar o HP e SP iniciais do personagem.",
            path: "/"
          }

          axios.post("/api/notification/add", notification);

        } else {
          let notification = {
            id: shortId.generate(),
            heading: "Cadastro",
            icon: {
              name: "warning",
              color: "primary"
            },
            timestamp: Date.now(),
            title: "Erro no cadastro de personagem",
            subtitle: "Tente novamente, alguma informação foi enviada com erros.",
            path: "/"
          }

          axios.post("/api/notification/add", notification);

        }
    }
  };

  handleChange = event => {
    event.persist();
    this.setState({ [event.target.name]: event.target.value });
  };

  handleChangeSelectArcana = (selectedOption) => {
    this.setState({ fool : selectedOption.value });
    if (selectedOption.value == 2) {
      document.getElementById("opcoesfool").style.display = "block";
    } else {
      document.getElementById("opcoesfool").style.display = "none";
      this.setState({ vida : "" });
      this.setState({ energia: "" });
    }
  };

  handleChangeSelectPersona = (selectedOption) => {
    this.setState({ fk_persona_persona_id : selectedOption.value });
  }

  render() {
    let {
      nome,
      usuario,
      foto,
      fool,
      fk_persona_persona_id,
      personas,
      vida,
      energia
    } = this.state;

    const options_arcana = [
      {value: 1, label: "Outra"},
      {value: 2, label: "Fool"}
    ]

    let options_persona = []
    let campo = {}

    for (let i = 0; i < personas.length; i ++) {
        campo = {value: personas[i]["persona_id"], label: personas[i]["nome"]}
        options_persona.push(campo);
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
              <TextValidator
                className="mb-16 w-100"
                label="Nome do Personagem"
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
                label="Nome de usuário do Discord"
                onChange={this.handleChange}
                type="text"
                name="usuario"
                value={usuario}
                validators={["required"]}
                errorMessages={["Este campo é obrigatório"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Foto"
                onChange={this.handleChange}
                type="text"
                name="foto"
                value={foto}
                validators={["required"]}
                errorMessages={["Este campo é obrigatório"]}
              />
              <InputLabel>Arcana</InputLabel>
              <Select
                className="mb-16 w-100"
                label="Arcana"
                onChange={this.handleChangeSelectArcana}
                name="fool"
                validators={["required"]}
                options={options_arcana}
                errorMessages={["Este campo é obrigatório"]}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12} xs={12}>
              <InputLabel>Persona</InputLabel>
              <Select
                className="mb-16 w-100"
                label="Persona"
                onChange={this.handleChangeSelectPersona}
                name="fk_persona_persona_id"
                validators={["required"]}
                options={options_persona}
                errorMessages={["Este campo é obrigatório"]}
              />
              <div className="invi" id="opcoesfool">
              <TextValidator
                className="mb-16 w-100"
                label="HP inicial"
                onChange={this.handleChange}
                id="hpPersonagem"
                type="number"
                name="vida"
                value={vida}
                validators={["isNumber", "isInteger", "isPositive"]}
                errorMessages={["O campo deve ser preenchiado com um número", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="SP inicial"
                onChange={this.handleChange}
                id="spPersonagem"
                type="number"
                name="energia"
                value={energia}
                validators={["isNumber", "isInteger", "isPositive"]}
                errorMessages={["O campo deve ser preenchiado com um número", "Este campo deve ser um número inteiro", "Este campo deve ser maior que 0"]}
              />
              </div>
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

export default FormPersonagem;
