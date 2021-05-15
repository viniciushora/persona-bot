import React, { Component } from "react";
import { Breadcrumb } from "matx";
import EditPersonagem from "../material-kit/edits/EditPersonagem";

class PersonagemEdit extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Edição", path: "/edits" },
              { name: "Personagens" }
            ]}
          />
        </div>
        <EditPersonagem />
      </div>
    );
  }
}

export default PersonagemEdit;