import React, { Component } from "react";
import { Breadcrumb } from "matx";
import EditItem from "../material-kit/edits/EditItem";

class ItemEdit extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Edição", path: "/edits" },
              { name: "Itens" }
            ]}
          />
        </div>
        <EditItem />
      </div>
    );
  }
}

export default ItemEdit;