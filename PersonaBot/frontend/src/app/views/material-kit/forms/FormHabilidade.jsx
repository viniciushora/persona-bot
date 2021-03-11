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

class FormHabilidade extends Component {
  state = {
    nome: "",
    fk_atributo_atributo_id: 0,
    fk_intensidade_intensidade_id: 0,
    fk_elemento_elemento_id: 0,
    vezes: ""
  };

  limparCampos = event => {
    this.setState({ nome: "" });
    this.setState({ vezes : "" });
  }

  componentDidMount() {
    // custom rule will have name 'isPasswordMatch'
    ValidatorForm.addValidationRule("isPositive", value => {
        if (Number(value) >= 0){
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
    ValidatorForm.addValidationRule("isInRange0to100", value => {
        if (Number(value) > 0 && Number(value) <= 100){
            return true;
        } else {
            return false;
        }
    });
  }

  handleSubmit = async event => {
    console.log("submitted");

    try{
        const nome = this.state.nome;
        const fk_atributo_atributo_id = this.state.fk_atributo_atributo_id;
        const fk_intensidade_intensidade_id = this.state.fk_intensidade_intensidade_id;
        const fk_elemento_elemento_id = this.state.fk_elemento_elemento_id;
        const vezes = this.state.vezes;

        const data = {
            nome,
            fk_atributo_atributo_id,
            fk_intensidade_intensidade_id,
            fk_elemento_elemento_id,
            vezes
        };

        await api.post('habilidade', data);


        let notification = {
            id: shortId.generate(),
            heading: "Cadastro",
            icon: {
            name: "description",
            color: "primary"
            },
            timestamp: Date.now(),
            title: "Habilidade cadastrada com sucesso.",
            subtitle: "Nome = " + nome + "; Elemento: " + fk_elemento_elemento_id + "; Intensidade: " + fk_intensidade_intensidade_id,
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
            title: "Erro no cadastro da Habilidade",
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

    handleChangeSelectElemento = (selectedOption) => {
        this.setState({ fk_elemento_elemento_id : selectedOption.value });
    };

    handleChangeSelectIntensidade = (selectedOption) => {
        this.setState({ fk_intensidade_intensidade_id : selectedOption.value });
    };

    handleChangeSelectAtributo = (selectedOption) => {
        this.setState({ fk_atributo_atributo_id : selectedOption.value });
    };

  render() {
    let {
        nome,
        fk_atributo_atributo_id,
        fk_intensidade_intensidade_id,
        fk_elemento_elemento_id,
        vezes
    } = this.state;

    let options_atributo = [
        {value: 3, label: "Força (St)"},
        {value: 4, label: "Magia (Ma)"},
        {value: 5, label: "Resistência (En)"},
        {value: 6, label: "Agilidade (Ag)"},
        {value: 7, label: "Sorte (Lu)"}
    ]

    let options_intensidade = [
        {value: 1, label: "Minúsculo"},
        {value: 2, label: "Leve"},
        {value: 3, label: "Médio"},
        {value: 4, label: "Pesado"},
        {value: 5, label: "Severo"},
        {value: 6, label: "Colossal"},
        {value: 7, label: "Outro"}
    ]

    let options_elemento = [
        {value: 1, label: "Físico"},
        {value: 2, label: "Arma de Fogo"},
        {value: 3, label: "Fogo"},
        {value: 4, label: "Gelo"},
        {value: 5, label: "Elétrico"},
        {value: 6, label: "Vento"},
        {value: 7, label: "Psicocinésia (Psy)"},
        {value: 8, label: "Nuclear"},
        {value: 9, label: "Benção"},
        {value: 10, label: "Maldição"},
        {value: 11, label: "Onipotência"},
        {value: 12, label: "Doença"},
        {value: 13, label: "Cura"},
        {value: 14, label: "Suporte"},
        {value: 15, label: "Passiva"},
        {value: 16, label: "Navegação"}
    ]

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
                label="Nome da Habilidade"
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
              <InputLabel>Elemento da Habilidade</InputLabel>
              <Select
                className="mb-16 w-100"
                label="Elemento da Habilidade"
                onChange={this.handleChangeSelectElemento}
                name="fk_elemento_elemento_id"
                validators={["required"]}
                options={options_elemento}
                errorMessages={["Este campo é obrigatório"]}
              />
              <InputLabel>Intensidade da Habilidade</InputLabel>
              <Select
                className="mb-16 w-100"
                label="Intensidade da Habilidade"
                onChange={this.handleChangeSelectIntensidade}
                name="fk_intensidade_intensidade_id"
                validators={["required"]}
                options={options_intensidade}
                errorMessages={["Este campo é obrigatório"]}
              />
              <InputLabel>Atributo da Habilidade</InputLabel>
              <Select
                className="mb-16 w-100"
                label="Atributo da Habilidade"
                onChange={this.handleChangeSelectAtributo}
                name="fk_atributo_atributo_id"
                validators={["required"]}
                options={options_atributo}
                errorMessages={["Este campo é obrigatório"]}
              />
                <TextValidator
                    className="mb-16 w-100"
                    label="Vezes de ocorrência"
                    onChange={this.handleChange}
                    type="number"
                    name="vezes"
                    value={vezes}
                    validators={["required", "isNumber", "isInteger", "isPositive"]}
                    errorMessages={["Este campo é obrigatório", "Este campo deve ser um número", "O valor do número deve ser um inteiro", "O valor deve ser positivo"]}
                />
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

export default FormHabilidade;