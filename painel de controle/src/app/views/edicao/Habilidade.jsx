import React, { Component } from "react";
import { Breadcrumb } from "matx";
import EditHabilidade from "../material-kit/edits/EditHabilidade";

class HabilidadeEdit extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Edição", path: "/edits" },
              { name: "Habilidades" }
            ]}
          />
        </div>
        <EditHabilidade />
      </div>
    );
  }
}

export default HabilidadeEdit;