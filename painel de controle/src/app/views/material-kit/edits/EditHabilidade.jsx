import React, { Component, Fragment } from "react";
import {
  Grid
} from "@material-ui/core";

import TableCard from "../../edicao/tabelas/HabilidadeTableCard";
import { withStyles } from "@material-ui/styles";

import "./styles.css";

import api from "../../../services/api";

class HabilidadeEdit extends Component {
  state = {
    habilidades: []
  };

  async componentDidMount() {
    await this.Habilidade();
  }

  async Habilidade(){
    await api.get('habilidade').then(response => { this.setState( { habilidades: response.data} )});
  }

  render() {
    let { theme } = this.props;

    return (
      <Fragment>
        <div className="tabela">
          <Grid container spacing={6}>
            <Grid item lg={6} md={6} sm={12} xs={12}>
                <TableCard habilidades={this.state.habilidades} theme={theme}/>
            </Grid>
          </Grid>
        </div>
      </Fragment>
    );
  }
}

export default withStyles({}, { withTheme: true })(HabilidadeEdit);