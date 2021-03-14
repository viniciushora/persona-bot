import { MatxLoadable } from "matx";

const Config = MatxLoadable({
  loader: () => import("./Config")
});

const configRoutes = [
  {
    path: "/config",
    component: Config
  },
];

export default configRoutes;