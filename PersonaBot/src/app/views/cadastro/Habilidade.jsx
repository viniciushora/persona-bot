import React, { Component } from "react";
import { Breadcrumb } from "matx";
import FormHabilidade from "../material-kit/forms/FormHabilidade";

class HabilidadeForm extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Cadastro", path: "/forms" },
              { name: "Habilidade" }
            ]}
          />
        </div>
        <FormHabilidade />
      </div>
    );
  }
}

export default HabilidadeForm;
