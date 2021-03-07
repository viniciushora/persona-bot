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
    name: "Listagem (WIP)",
    icon: "format_list_bulleted",
    path: "/naoexiste"
  },
  {
    name: "Edição (WIP)",
    icon: "edit",
    path: "/naoexiste"
  },

  {
    name: "Configurações",
    path: "/naoexiste",
    icon: "settings"
  },
  
  
];
