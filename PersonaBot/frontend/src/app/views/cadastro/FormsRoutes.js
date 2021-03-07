import { MatxLoadable } from "matx";

const PersonagemForm = MatxLoadable({
  loader: () => import("./Personagem")
});

const PersonaForm = MatxLoadable({
  loader: () => import("./Persona")
});

const ShadowForm = MatxLoadable({
  loader: () => import("./Shadow")
});

const HabilidadeForm = MatxLoadable({
  loader: () => import("./Habilidade")
});

const ItemForm = MatxLoadable({
  loader: () => import("./Item")
});

const formsRoutes = [
  {
    path: "/cadastro/personagem",
    component: PersonagemForm
  },
  {
    path: "/cadastro/persona",
    component: PersonaForm
  },
  {
    path: "/cadastro/shadow",
    component: ShadowForm
  },
  {
    path: "/cadastro/habilidade",
    component: HabilidadeForm
  },
  {
    path: "/cadastro/item",
    component: ItemForm
  }
];

export default formsRoutes;
