import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import 'antd/dist/antd.css';

import './styles/ant.less';
import Routes from './Routes';
import GlobalStyle from './styles/globalStyle';
import GlobalProvider from './contexts/GlobalProvider';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <GlobalProvider>
          <Routes />
          <ToastContainer position="bottom-right" />
          <GlobalStyle />
        </GlobalProvider>
      </BrowserRouter>
    </div>
  );
}
export default App;
