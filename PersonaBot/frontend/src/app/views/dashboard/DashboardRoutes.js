import { MatxLoadable } from "matx";
import { authRoles } from "../../auth/authRoles";

const Inicio = MatxLoadable({
  loader: () => import("./Inicio")
})

const dashboardRoutes = [
  {
    path: "/dashboard/inicio",
    component: Inicio,
    auth: authRoles.admin
  }
];

export default dashboardRoutes;
