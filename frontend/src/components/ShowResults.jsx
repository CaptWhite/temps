import { useEffect } from 'react';
import { useStore } from '../store';
import {
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Box
} from '@mui/material';

const ShowResults = () => {
  const utc = useStore((state) => state.utc);
  const tai = useStore((state) => state.tai);
  const gps = useStore((state) => state.gps);
  const tt = useStore((state) => state.tt);
  const eot = useStore((state) => state.eot);
  const eoe = useStore((state) => state.eoe);
  const oficial = useStore((state) => state.oficial);
  const civil = useStore((state) => state.civil);
  const solarMedia = useStore((state) => state.solarMedia);
  const solarVerdadera = useStore((state) => state.solarVerdadera);
  const juliana = useStore((state) => state.juliana);
  const gmst = useStore((state) => state.gmst);
  const mst = useStore((state) => state.mst);
  const gast = useStore((state) => state.gast);
  const ast = useStore((state) => state.ast);
  const sunrise = useStore((state) => state.sunrise);
  const solarNoon = useStore((state) => state.solarNoon);
  const sunset = useStore((state) => state.sunset);
  const hourItalica = useStore((state) => state.hourItalica);
  const hourBabilonica = useStore((state) => state.hourBabilonica);
  const incrementTimes = useStore((state) => state.incrementTimes);
  const isUpdating = useStore((state) => state.isUpdating);

  useEffect(() => {
    if (utc && isUpdating) {
      const interval = setInterval(() => {
        incrementTimes();
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [utc, incrementTimes, isUpdating]);

  const formatTime = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const hours = String(date.getUTCHours()).padStart(2, '0');
    const minutes = String(date.getUTCMinutes()).padStart(2, '0');
    const seconds = String(date.getUTCSeconds()).padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
  };

  const formatDecimalTime = (decimalTime, includeMilliseconds = false) => {
    if (decimalTime === null || decimalTime === undefined) return '';

    const sign = decimalTime < 0 ? '-' : '';
    const absTotalSeconds = Math.abs(decimalTime * 3600);

    const hours = Math.floor(absTotalSeconds / 3600);
    const minutes = Math.floor((absTotalSeconds % 3600) / 60);
    const seconds = Math.floor(absTotalSeconds % 60);

    let formattedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    if (includeMilliseconds) {
      const milliseconds = Math.round((absTotalSeconds - Math.floor(absTotalSeconds)) * 1000);
      formattedTime += `.${String(milliseconds).padStart(3, '0')}`;
    }

    return sign + formattedTime;
  };

  const renderCell = (title, value, isDate = false, isDecimal = false, includeMilliseconds = false) => (
    <Box display="flex">
      <Typography variant="body2" sx={{ textAlign: 'right', flex: 1, paddingRight: 1, fontSize: '0.7rem' }}>{title}:</Typography>
      <Typography variant="body2" sx={{ textAlign: 'left', flex: 1, fontSize: '0.7rem' }}>
        {isDate ? formatTime(value) : (isDecimal ? formatDecimalTime(value, includeMilliseconds) : value)}
      </Typography>
    </Box>
  );

  return (
    <Box sx={{ p: 2 }}>
      {utc && (
        <TableContainer component={Paper}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontSize: '0.7rem', textAlign: 'center', fontWeight: 'bold' }}>Escales atòmiques</TableCell>
                <TableCell sx={{ fontSize: '0.7rem', textAlign: 'center', fontWeight: 'bold' }}>Escales per rotació</TableCell>
                <TableCell sx={{ fontSize: '0.7rem', textAlign: 'center', fontWeight: 'bold' }}>Paràmetres del Sol</TableCell>
                <TableCell sx={{ fontSize: '0.7rem', textAlign: 'center', fontWeight: 'bold' }}>Altres dades</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow>
                <TableCell align="center">{renderCell('UTC', utc, true)}</TableCell>
                <TableCell align="center">{renderCell('UT1', utc, true)}</TableCell>
                <TableCell align="center">{renderCell('EoT', eot, false, true)}</TableCell>
                <TableCell align="center">{renderCell('Juliana', juliana.toFixed(4))}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell align="center">{renderCell('TAI', tai, false, true)}</TableCell>
                <TableCell align="center">{renderCell('Civil', civil, true)}</TableCell>
                <TableCell align="center">{renderCell('EoE', eoe, false, true, true)}</TableCell>
                <TableCell></TableCell>
              </TableRow>
              <TableRow>
                <TableCell align="center">{renderCell('GPS', gps, false, true)}</TableCell>
                <TableCell align="center" sx={{ color: 'red' }}>{renderCell('Oficial', oficial, true)}</TableCell>
                <TableCell></TableCell>
                <TableCell></TableCell>
              </TableRow>
              <TableRow>
                <TableCell align="center">{renderCell('TT', tt, false, true)}</TableCell>
                <TableCell align="center">{renderCell('Solar Mitjana', solarMedia, true)}</TableCell>
                <TableCell align="center">{renderCell('Sortida de Sol', sunrise)}</TableCell>
                <TableCell align="center">{renderCell('Hora Itàlica', hourItalica, false, true)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell></TableCell>
                <TableCell align="center">{renderCell('Solar Vertadera', solarVerdadera, true)}</TableCell>
                <TableCell align="center">{renderCell('Migdia', solarNoon)}</TableCell>
                <TableCell align="center">{renderCell('Hora Babilònica', hourBabilonica, false, true)}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell></TableCell>
                <TableCell align="center">{renderCell('GMST', gmst, false, true, true)}</TableCell>
                <TableCell align="center">{renderCell('Posta de Sol', sunset)}</TableCell>
                <TableCell></TableCell>
              </TableRow>
              <TableRow>
                <TableCell></TableCell>
                <TableCell align="center">{renderCell('MST', mst, false, true, true)}</TableCell>
                <TableCell></TableCell>
                <TableCell></TableCell>
              </TableRow>
              <TableRow>
                <TableCell></TableCell>
                <TableCell align="center">{renderCell('GAST', gast, false, true, true)}</TableCell>
                <TableCell></TableCell>
                <TableCell></TableCell>
              </TableRow>
              <TableRow>
                <TableCell></TableCell>
                <TableCell align="center">{renderCell('AST', ast, false, true, true)}</TableCell>
                <TableCell></TableCell>
                <TableCell></TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default ShowResults;
