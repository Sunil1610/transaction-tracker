import * as React from 'react';
import { useContext, useRef } from 'react';
import Title from './Title.tsx';
import TransactionsContext from '../TransactionsContext.tsx';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import ButtonRenderer from './GridButtonRenderer.tsx';
import './grid.css'

export default function Transactions() {
  var rows: any[] = useContext(TransactionsContext);
  const gridRef = useRef<AgGridReact | null>(null);
  if (!rows) {
    rows = [];
  } else if (rows.length > 0) {
    console.log(rows);
    rows.forEach(element => {
      element.id = element._id;
    });
  }

  const onGridReady = (params) => {
    console.log(params.api.autoSizeAllColumns(true));
    console.log(params.api);
  };
  
  const columns = [
    {
      field: 'timestamp',
      headerName: 'Date',
      sortable: true,
      filter: true,
      resizable: true,
      valueGetter: (params) => (new Date(params.data.timestamp * 1000)).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }),
      comparator: (v1, v2) =>
      new Date(v1).getTime() - new Date(v2).getTime()
    },
    { field: 'Description', headerName: 'Description', sortable: true, resizable: true, filter: true },
    { field: 'Type', headerName: 'Type', sortable: true, resizable: true, filter: true },
    { field: 'Source', headerName: 'Source', sortable: true, resizable: true, filter: true },
    { field: 'Amount', headerName: 'Amount', sortable: true, resizable: true, filter: true },
    {
      field: 'Action', headerName: "Action",
      resizable: true, filter: true ,
      cellRenderer: ButtonRenderer
    }
  ];

  return (
    <React.Fragment>
      <Title>Recent Transactions</Title>
      <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
        <AgGridReact
          rowData={rows}
          columnDefs={columns}
          components={{ButtonRenderer}}
          pagination={true}
          ref={gridRef}
          paginationPageSize={10}
          onGridReady={onGridReady}
          onFirstDataRendered={() => {
            console.log("onFirstDataRendered");
            if (gridRef.current) {
              gridRef.current.columnApi.autoSizeAllColumns(true);
            }
          }}
        />
      </div>
    </React.Fragment>
  );
}