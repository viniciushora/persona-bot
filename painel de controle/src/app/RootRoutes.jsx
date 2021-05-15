import React from "react";
import { Redirect } from "react-router-dom";

import dashboardRoutes from "./views/dashboard/DashboardRoutes";
import utilitiesRoutes from "./views/utilities/UtilitiesRoutes";
import sessionRoutes from './views/sessions/SessionRoutes';

import materialRoutes from "./views/material-kit/MaterialRoutes";

import formsRoutes from "./views/cadastro/FormsRoutes";
import configRoutes from "./views/config/ConfigRoutes";
import editRoutes from "./views/edicao/EditRoutes";
import mapRoutes from "./views/map/MapRoutes";

const redirectRoute = [
  {
    path: "/",
    exact: true,
    component: () => <Redirect to="/dashboard/inicio" />
  }
];

const errorRoute = [
  {
    component: () => <Redirect to="/session/404" />
  }
];

const routes = [
  ...dashboardRoutes,
  ...sessionRoutes,
  ...materialRoutes,
  ...utilitiesRoutes,
  ...configRoutes,
  ...formsRoutes,
  ...editRoutes,
  ...mapRoutes,
  ...redirectRoute,
  ...errorRoute
];

export default routes;
