import "babel-polyfill";
// import cssVars from "css-vars-ponyfill";

import React from "react";
import ReactDOM from "react-dom";
import "./_index.scss";

import * as serviceWorker from "./serviceWorker";
import App from "./app/App";

// cssVars();

ReactDOM.render(<App />, document.getElementById("root"));

serviceWorker.unregister();
