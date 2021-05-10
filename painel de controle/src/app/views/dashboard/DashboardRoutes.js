import { MatxLoadable } from "matx";

const Inicio = MatxLoadable({
  loader: () => import("./Inicio")
})

const dashboardRoutes = [
  {
    path: "/dashboard/inicio",
    component: Inicio
  }
];

export default dashboardRoutes;
