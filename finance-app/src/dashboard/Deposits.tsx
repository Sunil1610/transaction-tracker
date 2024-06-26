import React, {useState} from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Title from './Title.tsx';
import IconButton from '@mui/material/IconButton';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';

function preventDefault(event) {
  event.preventDefault();
}

export default function Deposits() {
  const [open, setOpen] = useState(false);

  return (
    <React.Fragment>
      <Title>Recent expenses
      <IconButton onClick={() => setOpen(true)}>
        <CalendarTodayIcon />
      </IconButton>
    </Title>
      <Typography component="p" variant="h4">
        $3,024.00
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        on 15 March, 2019
      </Typography>
      <div>
        <Link color="primary" href="#" onClick={preventDefault}>
          View balance
        </Link>
      </div>
    </React.Fragment>
  );
}
