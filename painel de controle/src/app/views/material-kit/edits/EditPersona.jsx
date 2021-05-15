import React, { Component, Fragment } from "react";
import {
  Grid
} from "@material-ui/core";

import TableCard from "../../edicao/tabelas/PersonaTableCard";
import { withStyles } from "@material-ui/styles";

import "./styles.css";

import api from "../../../services/api";

class PersonaEdit extends Component {
  state = {
    personas: []
  };

  async componentDidMount() {
    await this.Persona();
  }

  async Persona(){
    await api.get('persona').then(response => { this.setState( { personas: response.data} )});
  }

  render() {
    let { theme } = this.props;

    return (
      <Fragment>
        <div className="tabela">
          <Grid container spacing={6}>
            <Grid item lg={6} md={6} sm={12} xs={12}>
                <TableCard personas={this.state.personas} theme={theme}/>
            </Grid>
          </Grid>
        </div>
      </Fragment>
    );
  }
}

export default withStyles({}, { withTheme: true })(PersonaEdit);