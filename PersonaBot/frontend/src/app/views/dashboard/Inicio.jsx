import React, { Component, Fragment } from "react";
import {
  Grid,
  Card
} from "@material-ui/core";

import StatCards from "./shared/StatCards";
import { withStyles } from "@material-ui/styles";

class Dashboard1 extends Component {
  state = {};

  render() {
    let { theme } = this.props;

    return (
      <Fragment>
        <div className="pb-86 pt-30 px-30 bg-primary">
          <img width="20%" height="20%" src="https://raw.githubusercontent.com/ViniciusHora1009/persona-bot/main/imagens/persona-bot-circle.png"/>
        </div>

        <div className="analytics m-sm-30 mt--72">
          <Grid container spacing={3}>
            <Grid item lg={8} md={8} sm={12} xs={12}>

              <StatCards theme={theme}/>

            </Grid>

            <Grid item lg={4} md={4} sm={12} xs={12}>

            </Grid>
          </Grid>
        </div>
      </Fragment>
    );
  }
}

export default withStyles({}, { withTheme: true })(Dashboard1);
