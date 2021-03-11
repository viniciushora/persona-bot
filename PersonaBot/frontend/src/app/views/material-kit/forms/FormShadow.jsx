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

class FormShadow extends Component {
  state = {
    fk_persona_persona_id: 0,
    codinome: "",
    exp: "",
    dinheiro: "",
    personas: [],
    itens: [],
    chances: [],
    dropItens: []
  };

  limparCampos = event => {
    this.setState({ codinome : "" });
    this.setState({ exp : "" });
    this.setState({ chances : [] });
    this.setState({ dropItens : [] });
  }

  componentDidMount() {
    // custom rule will have name 'isPasswordMatch'
    this.Personas();
    this.Itens();
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

  Personas() {
    api.get('persona').then(response => { this.setState( { personas: response.data} )});
  };


  Itens() {
    api.get('item').then(response => { this.setState( { itens: response.data } )});
  }

  handleSubmit = async event => {
    console.log("submitted");

    try{
        const fk_persona_persona_id = this.state.fk_persona_persona_id;
        const codinome = this.state.codinome;
        const exp = this.state.exp;
        const dinheiro = this.state.dinheiro;
        const personas = this.state.personas;
        const itens = this.state.itens;
        const chances = this.state.chances;
        const dropItens = this.state.dropItens;

        const data = {
            codinome,
            fk_persona_persona_id,
            exp,
            dinheiro
        };

        await api.post('shadow', data);

        const fk_shadow_fk_persona_persona_id = fk_persona_persona_id;

        const data2 = {
            fk_shadow_fk_persona_persona_id,
            chances,
            dropItens
        }

        await api.post('drop', data2);

        let notification = {
            id: shortId.generate(),
            heading: "Cadastro",
            icon: {
            name: "description",
            color: "primary"
            },
            timestamp: Date.now(),
            title: "Shadow cadastrada com sucesso.",
            subtitle: "ID = " + fk_persona_persona_id + "; Codinome: " + codinome,
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
            title: "Erro no cadastro da Shadow",
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

    addItem = event => {
        event.persist();

        this.setState({ chances: [...this.state.chances, ""] } );
        this.setState({ dropItens: [...this.state.dropItens, ""] })
    }

    handleChangeItem = (selectedOption, index) => {
        this.state.dropItens[index] = selectedOption.value;
        this.setState({ dropItens: [...this.state.dropItens] } );
    }

    handleChangeChance = (event, index) => {
        this.state.chances[index] = event.target.value;
        this.setState({ chances: [...this.state.chances] } );
    }

    handleRemoveInputDrop = (position) => {
        this.setState( { chances: [...this.state.chances.filter((_, index) => index != position)] } );
        this.setState( { dropItens: [...this.state.dropItens.filter((_, index) => index != position)] } );
    }

    handleChangeSelectPersona = (selectedOption) => {
        this.setState({ fk_persona_persona_id : selectedOption.value });
    }

  render() {
    let {
        fk_persona_persona_id,
        codinome,
        exp,
        dinheiro,
        personas,
        itens,
        chances,
        dropItens
    } = this.state;


    let options_persona = []
    let campo = {}

    for (let i = 0; i < personas.length; i ++) {
        campo = {value: personas[i]["persona_id"], label: personas[i]["nome"]}
        options_persona.push(campo);
    }

    let options_item = []
    campo = {}

    for (let i = 0; i < itens.length; i ++) {
        campo = {value: itens[i]["item_id"], label: itens[i]["nome"]}
        options_item.push(campo);
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
                label="Codinome da Shadow"
                onChange={this.handleChange}
                type="text"
                name="codinome"
                value={codinome}
                validators={[
                  "required",
                  "minStringLength: 2",
                  "maxStringLength: 50"
                ]}
                errorMessages={["Este campo é obrigatório"]}
              />
              <InputLabel>Identidade da Shadow</InputLabel>
              <Select
                className="mb-16 w-100"
                label="Persona"
                onChange={this.handleChangeSelectPersona}
                name="fk_persona_persona_id"
                validators={["required"]}
                options={options_persona}
                errorMessages={["Este campo é obrigatório"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Experiência adquiria ao matar"
                onChange={this.handleChange}
                type="number"
                name="exp"
                value={exp}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número", "O valor do número deve ser um inteiro", "O valor deve ser positivo"]}
              />
              <TextValidator
                className="mb-16 w-100"
                label="Dinheiro dropado ao matar"
                onChange={this.handleChange}
                type="number"
                name="dinheiro"
                value={dinheiro}
                validators={["required", "isNumber", "isInteger", "isPositive"]}
                errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "O valor do número deve ser um inteiro", "O valor deve ser positivo"]}
              />
            </Grid>
            <Grid item lg={6} md={6} sm={12} xs={12}>
                <h5>Itens Dropados</h5>
                <Button color="primary" onClick={this.addItem} variant="contained" >
                    <Icon>add</Icon>
                    <span className="pl-8 capitalize">Adicionar Item</span>
                </Button>
                {
                    chances.map((chance, index) => (
                        <>
                        <h6 className="fix1">Item {index + 1}</h6>
                        <TextValidator
                            className="mb-16 w-100"
                            key={`c-${index}`}
                            label="Chance de drop (%)"
                            onChange={(event) => this.handleChangeChance(event, index)}
                            type="number"
                            name="chances"
                            value={chance}
                            validators={["required", "isNumber", "isInteger", "isInRange0to100"]}
                            errorMessages={["Este campo é obrigatório", "Este campo deve ser um número inteiro", "O valor do número deve ser um inteiro", "O valor desse campo deve estar entre 0 e 100."]}
                        />
                        <InputLabel>Item</InputLabel>
                        <Select
                            className="mb-16 w-100"
                            label="Item"
                            key={`i-${index}`}
                            onChange={(selectedOption) => this.handleChangeItem(selectedOption, index)}
                            name="dropItens"
                            options={options_item}
                            validators={["required"]}
                            errorMessages={["Este campo é obrigatório"]}
                        />
                        <Button color="secondary" onClick={() => {this.handleRemoveInputDrop(index)}} variant="contained" >
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

export default FormShadow;