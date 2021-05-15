import React, { Component, Fragment } from "react";
import {
  Grid
} from "@material-ui/core";

import TableCard from "../../edicao/tabelas/ItemTableCard";
import { withStyles } from "@material-ui/styles";

import "./styles.css";

import api from "../../../services/api";

class ItemEdit extends Component {
  state = {
    itens: []
  };

  async componentDidMount() {
    await this.Item();
  }

  async Item(){
    await api.get('item').then(response => { this.setState( { itens: response.data} )});
  }

  render() {
    let { theme } = this.props;

    return (
      <Fragment>
        <div className="tabela">
          <Grid container spacing={6}>
            <Grid item lg={6} md={6} sm={12} xs={12}>
                <TableCard itens={this.state.itens} theme={theme}/>

            </Grid>
          </Grid>
        </div>
      </Fragment>
    );
  }
}

export default withStyles({}, { withTheme: true })(ItemEdit);