import { Paper, Table, TableBody,  TableContainer, TableHead, TableRow, ThemeProvider, createTheme } from '@mui/material'
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import { styled } from '@mui/material/styles';
import { tableParams } from '../helpers/tableParams';

interface ShowTableProps {
  csv: any[];
  radio1: string;
  unit: string;
}

export const ShowTable = ({csv, radio1, unit}: ShowTableProps) => {
  const tParms = tableParams[radio1]

  // Tema personalizado
  const theme = createTheme({
    components: {
      MuiFormControlLabel: {
        styleOverrides: {
          label: {
            fontSize: "8px", // Tamaño de la fuente
          }
        },
      },
    },
  });

  const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
      backgroundColor: theme.palette.common.black,
      color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
      fontSize: 12,
    },
  }));
  
  const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    '&:last-child td, &:last-child th': {
      border: 0,
    },
  }));

  let rows: any[] | null = null
  const {rows1, rows2, rows3 } = tParms.createRows(csv)
  if (unit === 'degree')      {rows = rows1}
  if (unit === 'degree_dms')  {rows = rows2}
  if (unit === 'radian')      {rows = rows3}

  return (
    <>
        {rows && <ThemeProvider theme={theme}>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow >
                  {tParms.title.map((title: string, idx: number) => ( 
                    <StyledTableCell key={idx} align={tParms.align[idx]}>{title}</StyledTableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row, idx) => (
                  <StyledTableRow 
                    key={idx}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                  >
                    {Object.entries(row).map(([, col],idx) => (
                      <TableCell key={idx} align={tParms.align[idx]}>{tParms.parseNumbers[idx](col, unit)}</TableCell>
                    ))}
                  </StyledTableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </ThemeProvider>}
    </>
  )
}