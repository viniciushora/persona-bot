import React, { Component } from "react";
import { Breadcrumb } from "matx";
import EditPersona from "../material-kit/edits/EditPersona";

class PersonaEdit extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Edição", path: "/edits" },
              { name: "Personas" }
            ]}
          />
        </div>
        <EditPersona />
      </div>
    );
  }
}

export default PersonaEdit;