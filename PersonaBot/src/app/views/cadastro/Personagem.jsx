import React, { Component } from "react";
import { Breadcrumb } from "matx";
import FormPersonagem from "../material-kit/forms/FormPersonagem";

class PersonagemForm extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Cadastro", path: "/forms" },
              { name: "Personagem" }
            ]}
          />
        </div>
        <FormPersonagem />
      </div>
    );
  }
}

export default PersonagemForm;
