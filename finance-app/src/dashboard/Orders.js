import * as React from 'react';
import { useContext } from 'react';
import Title from './Title';
import TransactionsContext from '../TransactionsContext';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';


// Generate Order Data
function createData(id, date, name, shipTo, paymentMethod, amount) {
  return { id, date, name, shipTo, paymentMethod, amount };
}

function preventDefault(event) {
  event.preventDefault();
}


export default function Orders() {
  const rows = useContext(TransactionsContext);

  if (!rows) {
    rows = []
  } else if (rows.length > 0) {
    console.log(rows);
    rows.forEach(element => {
      element.id = element._id;
    });
  }

  
  const columns = [
    {
      field: 'timestamp',
      headerName: 'Date',
      sortable: true,
      filter: true,
      resizable: true,
      valueGetter: (params) => (new Date(params.data.timestamp * 1000)).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }),
      comparator: (v1, v2) =>
        new Date(v1) - new Date(v2)
    },
    { field: 'Description', headerName: 'Description', sortable: true, resizable: true, filter: true },
    { field: 'Type', headerName: 'Type', sortable: true, resizable: true, filter: true },
    { field: 'Source', headerName: 'Source', sortable: true, resizable: true, filter: true },
    { field: 'Amount', headerName: 'Amount', sortable: true, resizable: true, filter: true },
  ];

  return (
    <React.Fragment>
      <Title>Recent Transactions</Title>
      <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
        <AgGridReact
          rowData={rows}
          columnDefs={columns}
          pagination={true}
          paginationPageSize={10}
        />
      </div>
    </React.Fragment>
  );
}