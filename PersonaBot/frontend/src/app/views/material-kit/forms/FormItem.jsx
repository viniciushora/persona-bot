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

class FormItem extends Component {
  state = {
    nome: "",
    fk_tipo_item_tipo_id: 0,
    valor: ""
  };

  limparCampos = event => {
    this.setState({ nome: "" });
    this.setState({ valor : "" });
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
        const fk_tipo_item_tipo_id = this.state.fk_tipo_item_tipo_id;
        const valor = this.state.valor;

        var valor_item = null;
        if (valor > 0) {
            valor_item = valor;
        }

        const data = {
            nome,
            fk_tipo_item_tipo_id,
            valor_item
        };

        await api.post('item', data);



        let notification = {
            id: shortId.generate(),
            heading: "Cadastro",
            icon: {
            name: "description",
            color: "primary"
            },
            timestamp: Date.now(),
            title: "Item cadastrado com sucesso.",
            subtitle: "Nome = " + nome + "; Tipo: " + fk_tipo_item_tipo_id,
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
            title: "Erro no cadastro da Item",
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

    handleChangeSelectTipoItem = (selectedOption) => {
        this.setState({ fk_tipo_item_tipo_id : selectedOption.value });
        if (selectedOption.value > 6 && selectedOption.value < 10){
            document.getElementById("opcaovalor").style.display = "block";
        } else {
            document.getElementById("opcaovalor").style.display = "none";
            this.setState({ valor : "" });
        }
    }

  render() {
    let {
        nome,
        fk_tipo_item_tipo_id,
        valor
    } = this.state;

    let options_tipo_item = [
        {value: 1, label: "Consumíveis"},
        {value: 2, label: "Cartas de Habilidade"},
        {value: 3, label: "Materiais"},
        {value: 4, label: "Tesouros"},
        {value: 5, label: "Essenciais"},
        {value: 6, label: "Itens-chave"},
        {value: 7, label: "Armas corpo-a-corpo"},
        {value: 8, label: "Armas à distância"},
        {value: 9, label: "Armadura"},
        {value: 10, label: "Acessórios"},
        {value: 11, label: "Roupas"},
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
                label="Nome do Item"
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
              <InputLabel>Tipo do Item</InputLabel>
              <Select
                className="mb-16 w-100"
                label="Tipo do Item"
                onChange={this.handleChangeSelectTipoItem}
                name="fk_tipo_item_tipo_id"
                validators={["required"]}
                options={options_tipo_item}
                errorMessages={["Este campo é obrigatório"]}
              />
            <div className="invi" id="opcaovalor">
                <TextValidator
                    className="mb-16 w-100"
                    label="Valor (Armadura ou Ataque)"
                    onChange={this.handleChange}
                    type="number"
                    name="valor"
                    value={valor}
                    validators={["required", "isNumber", "isInteger", "isPositive"]}
                    errorMessages={["Este campo é obrigatório", "Este campo deve ser um número", "O valor do número deve ser um inteiro", "O valor deve ser positivo"]}
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

export default FormItem;