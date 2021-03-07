import React, { Component } from "react";
import { Breadcrumb } from "matx";
import FormPersona from "../material-kit/forms/FormPersona";

class PersonaForm extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Cadastro", path: "/forms" },
              { name: "Persona" }
            ]}
          />
        </div>
        <FormPersona />
      </div>
    );
  }
}

export default PersonaForm;
