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

class FormConfig extends Component {
  state = {
    config: [],
    token: "",
    prefix: "",
    novo_token: "",
    novo_prefix: ""
  };

  async componentDidMount() {
    await this.Config();
    let config = this.state.config;
    this.setState({token: config[0].token});
    this.setState({prefix: config[0].prefix});
    this.setState({novo_token: config[0].token});
    this.setState({novo_prefix: config[0].prefix});
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
    async Config(){
      await api.get('config').then(response => { this.setState( { config: response.data} )});
    }

    handleChange = event => {
      event.persist();
      this.setState({ [event.target.name]: event.target.value });
    };

    handleChangeToken(parToken) {
        this.setState({ token: parToken });
        this.setState({ novoToken: parToken });
        let token = parToken;
        let data1 = {
          token
        }
        api.post('config/token', data1).then(data => data);
    };

    handleChangePrefix(parPrefix) {
      this.setState({ prefix: parPrefix });
      this.setState({ novo_prefix: parPrefix });
      let prefix = parPrefix;
      let data2 = {
        prefix
      }
      api.post('config/prefix', data2).then(data => data);
    }

    edicaoToken = (parToken) => {
      if (document.getElementById("campo1").disabled == true) {
        document.getElementById("campo1").disabled = false;
        document.getElementById("campo1").classList.add('aberto');
        document.getElementById("cancelar1").style.display = "block";
      } else {
        document.getElementById("campo1").disabled = true;
        document.getElementById("campo1").classList.remove('aberto');
        document.getElementById("cancelar1").style.display = "none";
        this.handleChangeToken(parToken);
        let notification = {
          id: shortId.generate(),
          heading: "Configurações",
          icon: {
          name: "settings",
          color: "primary"
          },
          timestamp: Date.now(),
          title: "Token do Bot atualizado",
          subtitle: "Novo token = " + parToken,
          path: "/"
        }
        axios.post("/api/notification/add", notification);
      }
    };

    edicaoPrefix = (parPrefix) => {
      if (document.getElementById("campo2").disabled == true) {
        document.getElementById("campo2").disabled = false;
        document.getElementById("campo2").classList.add('aberto');
        document.getElementById("cancelar2").style.display = "block";
      } else {
        document.getElementById("campo2").disabled = true;
        document.getElementById("campo2").classList.remove('aberto');
        document.getElementById("cancelar2").style.display = "none";
        this.handleChangePrefix(parPrefix);
        let notification = {
          id: shortId.generate(),
          heading: "Configurações",
          icon: {
          name: "settings",
          color: "primary"
          },
          timestamp: Date.now(),
          title: "Prefixo do Bot atualizado",
          subtitle: "Novo prefixo = " + parPrefix,
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

    console.log(novo_prefix)

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