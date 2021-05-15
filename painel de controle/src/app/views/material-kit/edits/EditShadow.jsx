import React, { Component, Fragment } from "react";
import {
  Grid
} from "@material-ui/core";

import TableCard from "../../edicao/tabelas/ShadowTableCard";
import { withStyles } from "@material-ui/styles";

import "./styles.css";

import api from "../../../services/api";

class ShadowEdit extends Component {
  state = {
    shadows: [],
    shadow_info: ""
  };

  async componentDidMount() {
    await this.Shadow();
    await this.ShadowInfo();
  }

  async Shadow(){
    await api.get('shadow').then(response => { this.setState( { shadows: response.data} )});
  }

  async ShadowInfo(){
      let persona_id = 0;
      let data = "";
      for(let i=0; i < this.state.shadows.length; i++){
        persona_id = this.state.shadows[i].fk_persona_persona_id
        data = {
          persona_id
        }
        await api.post('persona-info', data).then(response => { this.setState( { shadow_info: response.data} )});
        this.state.shadows[i].foto = this.state.shadow_info[0].link_foto
        this.state.shadows[i].nome = this.state.shadow_info[0].nome
        this.setState({ shadows: [...this.state.shadows] } );
      }
  }

  render() {
    let { theme } = this.props;

    return (
      <Fragment>
        <div className="tabela">
          <Grid container spacing={6}>
            <Grid item lg={6} md={6} sm={12} xs={12}>
                <TableCard shadows={this.state.shadows} theme={theme}/>
            </Grid>
          </Grid>
        </div>
      </Fragment>
    );
  }
}

export default withStyles({}, { withTheme: true })(ShadowEdit);