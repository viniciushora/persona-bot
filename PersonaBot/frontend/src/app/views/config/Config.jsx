import React, { Component } from "react";
import { Breadcrumb } from "matx";
import FormConfig from "../material-kit/forms/FormConfig";

class Config extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Configurações", path: "/config" },
            ]}
          />
        </div>
        <FormConfig />
      </div>
    );
  }
}

export default Config;