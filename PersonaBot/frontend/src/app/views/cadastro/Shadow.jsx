import React, { Component } from "react";
import { Breadcrumb } from "matx";
import FormShadow from "../material-kit/forms/FormShadow";

class ShadowForm extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Cadastro", path: "/cadastro"},
              { name: "Shadow" }
            ]}
          />
        </div>
        <FormShadow />
      </div>
    );
  }
}

export default ShadowForm;
