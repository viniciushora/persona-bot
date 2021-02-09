import React, { useState } from 'react';

import './global.css';

import Header from './Header';
import Routes from './routes';

function App() {
  const [counter, setCounter] = useState(0);

  function increment() {
    setCounter(counter + 1);
  }

  return (
    <body>
    <Header />
    <Routes />
    </body>
    
  );
}

export default App;
