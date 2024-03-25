import React, {useState} from 'react';
import axios from 'axios';
import Button from '@mui/material/Button'; // Import Material-UI Button
import './grid.css'

export default function ButtonRenderer(props) {
  const [dropdownVisible, setDropdownVisible] = useState(false);
 
  const toggleDropdown = () => {
     setDropdownVisible(!dropdownVisible);
     console.log(dropdownVisible);
  };
 
  return (
    <div className="button-renderer">
      <Button variant="contained" onClick={toggleDropdown} className="ag-btn">
        Options
      </Button>
        <div className="dropdown-menu" ngif="dropdownVisible">
          <div className="dropdown-item" onClick={() => console.log('Splitwise')}>
            Splitwise
          </div>
          <div className="dropdown-item" onClick={() => console.log('Category')}>
            Category
          </div>
          <div className="dropdown-item" onClick={() => console.log('Tag')}>
            Tag
          </div>
        </div>
    </div>
 );
 }