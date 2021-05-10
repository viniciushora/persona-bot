import React, { Component } from "react";
import { Breadcrumb } from "matx";
import FormItem from "../material-kit/forms/FormItem";

class ItemForm extends Component {
  render() {
    return (
      <div className="m-sm-30">
        <div  className="mb-sm-30">
          <Breadcrumb
            routeSegments={[
              { name: "Cadastro", path: "/forms" },
              { name: "Item" }
            ]}
          />
        </div>
        <FormItem />
      </div>
    );
  }
}

export default ItemForm;
