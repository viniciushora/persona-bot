import "babel-polyfill";

import React from "react";
import ReactDOM from "react-dom";
import "./_index.scss";

import * as serviceWorker from "./serviceWorker";
import App from "./app/App";


ReactDOM.render(<App />, document.getElementById("root"));

serviceWorker.unregister();
