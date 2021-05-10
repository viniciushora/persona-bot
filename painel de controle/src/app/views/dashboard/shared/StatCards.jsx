import React, { Component } from "react";
import {
  Grid,
  Card,
  Icon,
  IconButton,
  Tooltip,
} from "@material-ui/core";
import GitHubIcon from '@material-ui/icons/GitHub';

import api from '../../../services/api'

const StatCards = ({theme}) => {
  async function ligarBot() {
    await api.get('bot')
  }

  return (
    <Grid container spacing={3} className="mb-24">
      <Grid item xs={12} md={6}>
        <Card className="play-card p-sm-24 bg-paper" elevation={6}>
          <div className="flex flex-middle">
            <GitHubIcon
              style={{
                fontSize: "44px",
                opacity: 0.6,
                color: theme.palette.primary.main
              }}
            >
            </GitHubIcon>
            <div className="ml-12">
              <small className="text-primary">GitHub</small>
              <h6 className="m-0 mt-4 text-primary font-weight-500">Repositório do PersonaBot</h6>
            </div>
          </div>
          <Tooltip target="_blank" href='https://github.com/ViniciusHora1009/persona-bot' title="Visitar o repositório" placement="top">
            <IconButton>
              <Icon color="secondary">arrow_right_alt</Icon>
            </IconButton>
          </Tooltip>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card className="play-card p-sm-24 bg-paper" elevation={6}>
          <div className="flex flex-middle">
            <Icon
              style={{
                fontSize: "44px",
                opacity: 0.6,
                color: theme.palette.primary.main
              }}
            >
              attach_money
            </Icon>
            <div className="ml-12">
              <small className="text-primary">Apoie o criador</small>
              <h6 className="m-0 mt-4 text-primary font-weight-500">viniciushora100@gmail.com</h6>
            </div>
          </div>
          <Tooltip target="_blank" href='https://paypal.com' title="Pague um café" placement="top">
            <IconButton>
              <Icon color="secondary">arrow_right_alt</Icon>
            </IconButton>
          </Tooltip>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card className="play-card p-sm-24 bg-paper" elevation={6}>
          <div className="flex flex-middle">
            <Icon
              style={{
                fontSize: "44px",
                opacity: 0.6,
                color: theme.palette.primary.main
              }}
            >
              settings
            </Icon>
            <div className="ml-12">
              <small className="text-primary">Configure o Bot</small>
              <h6 className="m-0 mt-4 text-primary font-weight-500">
                Guia de Instalação
              </h6>
            </div>
          </div>
          <Tooltip target="_blank" href="https://github.com/ViniciusHora1009/persona-bot/blob/main/guias/Guia%20de%20Instala%C3%A7%C3%A3o%20do%20PersonaBot.md"title="Acessar o guia" placement="top">
            <IconButton>
              <Icon color="secondary">arrow_right_alt</Icon>
            </IconButton>
          </Tooltip>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card className="play-card p-sm-24 bg-paper" elevation={6}>
          <div className="flex flex-middle">
            <Icon
              style={{
                fontSize: "44px",
                opacity: 0.6,
                color: theme.palette.primary.main
              }}
            >
              android
            </Icon>
            <div className="ml-12">
              <small className="text-primary">Ligar o Bot</small>
              <h6 className="m-0 mt-4 text-primary font-weight-500">
                Explore o Metaverso
              </h6>
            </div>
          </div>
          <Tooltip title="Ligar o Bot" placement="top">
            <IconButton >
              <Icon onClick={ligarBot} color="secondary">play_circle_filled</Icon>
            </IconButton>
          </Tooltip>
        </Card>
      </Grid>
    </Grid>
  );
};

export default StatCards;
