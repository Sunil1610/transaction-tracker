import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import Dashboard from './dashboard/Dashboard.tsx';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


function App() {
  // const columnDefs = [
  //   { headerName: "Amount", field: "amount", sortable: true, filter: true },
  //   { headerName: "Description", field: "description", sortable: true, filter: true },
  //   { headerName: "Type", field: "type", sortable: true, filter: true },
  //   { headerName: "Tags", field: "tags", sortable: true, filter: true },
  //   {
  //     headerName: "Update",
  //     field: "update",
  //     cellRendererFramework: (params) => (
  //       <button onClick={() => handleUpdate(params.data)}>Update</button>
  //     ),
  //   },
  // ];

  // const handleUpdate = (data) => {
  //   alert('Update clicked for: ' + JSON.stringify(data));
  // };

  // const [rowData, setRowData] = useState([]);

  //   useEffect(() => {
  //       const fetchData = async () => {
  //           const response = await axios.get("http://localhost:8000/transactions/");
  //           setRowData(response.data);
  //       }
  //       fetchData();
  //   }, []);

    return (
      <Router>
        <Routes>
          <Route path="/ui/dashboard" element={< Dashboard />} />
        </Routes>
      </Router>
    );
}

export default App;
