import logo from './logo.svg';
import './App.css';
import { Map } from './components/map'; 
import {Button,Tabs,Tab} from 'react-bootstrap';
import UploadFiles from "./components/upload-files-component";
import React, { useState } from 'react';
import TasksTable from "./components/table2"
import http from "./http-common";



function App() {
  const [selectedTab, setSelectedTab] = useState('data');
  const [refreshTable, setRefreshTable] = useState(false);

  const handleFileUploadComplete = () => {
    // Update table data and trigger a refresh
   
    setRefreshTable(true);
    
  };

  return (
    <div className="App">
      <Tabs
      id="controlled-tab"
      activeKey={selectedTab}
      onSelect={(k) => setSelectedTab(k)}
      className="mb-3"
    >
      <Tab eventKey="map" title="Карта">
      <Map />
      </Tab>
      <Tab eventKey="data" title="Загрузка данных">
      <UploadFiles onUploadComplete={handleFileUploadComplete}/>
      <TasksTable refresh={refreshTable}/>

      </Tab>
      </Tabs>


    </div>
  );
}

export default App;
