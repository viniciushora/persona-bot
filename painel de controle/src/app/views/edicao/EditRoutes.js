import { MatxLoadable } from "matx";

const PersonagemEdit = MatxLoadable({
  loader: () => import("./Personagem")
});

const PersonaEdit = MatxLoadable({
  loader: () => import("./Persona")
});

const ShadowEdit = MatxLoadable({
  loader: () => import("./Shadow")
});

const HabilidadeEdit = MatxLoadable({
  loader: () => import("./Habilidade")
});

const ItemEdit = MatxLoadable({
  loader: () => import("./Item")
});

const editRoutes = [

  {
    path: "/edicao/personagens",
    component: PersonagemEdit
  },

  {
    path: "/edicao/personas",
    component: PersonaEdit
  },
  {
    path: "/edicao/shadows",
    component: ShadowEdit
  },
  {
    path: "/edicao/habilidades",
    component: HabilidadeEdit
  },
  {
    path: "/edicao/itens",
    component: ItemEdit
  }
];

export default editRoutes;
