import React, { Component } from "react";
import { Breadcrumb } from "matx";
import EditShadow from "../material-kit/edits/EditShadow";

class ShadowEdit extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Edição", path: "/edits" },
              { name: "Shadows" }
            ]}
          />
        </div>
        <EditShadow />
      </div>
    );
  }
}

export default ShadowEdit;