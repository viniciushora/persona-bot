import React, { Component, Fragment } from "react";
import {
  Grid
} from "@material-ui/core";

import TableCard from "../../edicao/tabelas/PersonagemTableCard";
import { withStyles } from "@material-ui/styles";

import "./styles.css";

import api from "../../../services/api";

class PersonagemEdit extends Component {
  state = {
    personagens: []
  };

  async componentDidMount() {
    await this.Personagem();
  }

  async Personagem(){
    await api.get('personagem').then(response => { this.setState( { personagens: response.data} )});
  }

  render() {
    let { theme } = this.props;

    return (
      <Fragment>
        <div className="tabela">
          <Grid container spacing={6}>
            <Grid item lg={6} md={6} sm={12} xs={12}>
                <TableCard personagens={this.state.personagens} theme={theme}/>
            </Grid>
          </Grid>
        </div>
      </Fragment>
    );
  }
}

export default withStyles({}, { withTheme: true })(PersonagemEdit);