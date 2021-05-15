export const navigations = [
  {
    name: "Início",
    path: "/dashboard/inicio",
    icon: "dashboard"
  },
  {
    name: "Cadastro",
    icon: "description",
    children: [
      {
        name: "Personagem",
        path: "/cadastro/personagem",
        iconText: "P1"
      },
      {
        name: "Persona",
        path: "/cadastro/persona",
        iconText: "P2"
      },
      {
        name: "Shadow",
        path: "/cadastro/shadow",
        iconText: "S"
      },
      {
        name: "Item",
        path: "/cadastro/item",
        iconText: "I"
      },
      {
        name: "Habilidade",
        path: "/cadastro/habilidade",
        iconText: "H"
      }
    ]
  },
  {
    name: "Edição",
    icon: "edit",
    children: [
      {
        name: "Personagens",
        path: "/edicao/personagens",
        iconText: "P1"
      },
      {
        name: "Personas",
        path: "/edicao/personas",
        iconText: "P2"
      },
      {
        name: "Shadows",
        path: "/edicao/shadows",
        iconText: "S"
      },
      {
        name: "Itens",
        path: "/edicao/itens",
        iconText: "I"
      },
      {
        name: "Habilidades",
        path: "/edicao/habilidades",
        iconText: "H"
      }
    ]
  },
  {
    name: "Configurações",
    path: "/config",
    icon: "settings"
  },
];
