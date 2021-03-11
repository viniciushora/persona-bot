import React, { Component, useState, useEffect } from "react";
import shortId from "shortid";
import { ValidatorForm, TextValidator } from "react-material-ui-form-validator";
import axios from "axios";
import {
  Button,
  Icon,
  Grid,
  InputLabel
} from "@material-ui/core";
import Select from 'react-select'
import "date-fns";

import api from "../../../services/api";
import './styles.css';

var json = require('../../../../bot/config.json');

class FormConfig extends Component {
  state = {
    token: json.token,
    prefix: json.prefix,
    novo_token: json.token,
    novo_prefix: json.prefix
  };

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
    salvarJson(){
      var obj = {
        "token": this.state.token,
        "prefix": this.state.prefix,
        "dbname": json.dbname,
        "user": json.user,
        "host": json.host,
        "password": json.password
      }
      api.post("/api/bot-config", obj);
    }

    handleChange = event => {
      event.persist();
      this.setState({ [event.target.name]: event.target.value });
    };

    handleChangeToken(token) {
        this.setState({ token: token });
        this.setState({ novoToken: token });
    };

    handleChangePrefix(prefix) {
      this.setState({ prefix: prefix });
      this.setState({ novo_prefix: prefix });
    };

    edicaoToken = (token) => {
      if (document.getElementById("campo1").disabled == true) {
        document.getElementById("campo1").disabled = false;
        document.getElementById("campo1").classList.add('aberto');
        document.getElementById("cancelar1").style.display = "block";
      } else {
        document.getElementById("campo1").disabled = true;
        document.getElementById("campo1").classList.remove('aberto');
        document.getElementById("cancelar1").style.display = "none";
        this.handleChangeToken(token);
        this.salvarJson();
        let notification = {
          id: shortId.generate(),
          heading: "Configurações",
          icon: {
          name: "settings",
          color: "primary"
          },
          timestamp: Date.now(),
          title: "Token do Bot atualizado",
          subtitle: "Novo token = " + this.state.token,
          path: "/"
        }
        axios.post("/api/notification/add", notification);
      }
    }

    edicaoPrefix = (prefix) => {
      if (document.getElementById("campo2").disabled == true) {
        document.getElementById("campo2").disabled = false;
        document.getElementById("campo2").classList.add('aberto');
        document.getElementById("cancelar2").style.display = "block";
      } else {
        document.getElementById("campo2").disabled = true;
        document.getElementById("campo2").classList.remove('aberto');
        document.getElementById("cancelar2").style.display = "none";
        this.handleChangePrefix(prefix);
        this.salvarJson();
        let notification = {
          id: shortId.generate(),
          heading: "Configurações",
          icon: {
          name: "settings",
          color: "primary"
          },
          timestamp: Date.now(),
          title: "Prefixo do Bot atualizado",
          subtitle: "Novo prefixo = " + prefix,
          path: "/"
        }
        axios.post("/api/notification/add", notification);
      }
    }

    cancelarToken = event => {
      event.persist();
      document.getElementById("campo1").disabled = true;
      document.getElementById("campo1").classList.remove('aberto');
      document.getElementById("cancelar1").style.display = "none";
      this.setState({ novo_token: this.state.token });
    }

    cancelarPrefix = event => {
      event.persist();
      document.getElementById("campo2").disabled = true;
      document.getElementById("campo2").classList.remove('aberto');
      document.getElementById("cancelar2").style.display = "none";
      this.setState({ novo_prefix: this.state.prefix });
    }

  render() {
    let {
      novo_token,
      novo_prefix
    } = this.state;

    return (
      <div>
        <ValidatorForm
          ref="form"
          onError={errors => null}
        >
          <Grid container spacing={6}>
            <Grid item lg={6} md={6} sm={12} xs={12}>
              <TextValidator
                className="mb-16 w-100"
                label="Token do Bot"
                id="campo1"
                type="text"
                onChange={this.handleChange}
                name="novo_token"
                value={novo_token}
                disabled
              />
              <Button id="cancelar1" className="botoes-config fix4 invi" color="secondary" variant="contained" onClick={this.cancelarToken}>
                <Icon>cancel</Icon>
              </Button>
              <Button className="botoes-config fix3" color="primary" variant="contained" onClick={() => this.edicaoToken(novo_token)}>
                <Icon>edit</Icon>
              </Button>
              <TextValidator
                className="mb-16 w-100"
                label="Prefixo do Bot"
                disabled
                id ="campo2"
                onChange={this.handleChange}
                type="text"
                name="novo_prefix"
                value={novo_prefix}
              />
              <Button id="cancelar2" className="botoes-config fix4 invi" color="secondary" variant="contained" onClick={this.cancelarPrefix}>
                <Icon>cancel</Icon>
              </Button>
              <Button className="botoes-config fix3" color="primary" variant="contained" onClick={() => this.edicaoPrefix(novo_prefix)}>
                <Icon>edit</Icon>
              </Button>
            </Grid>
          </Grid>
        </ValidatorForm>
      </div>
    );
  }
}

export default FormConfig;