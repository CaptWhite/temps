import { useEffect } from 'react';
import { useStore } from './store';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Header from './components/Header';
import UpperForm from './components/UpperForm';
import ShowResults from './components/ShowResults';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const setTimes = useStore((state) => state.setTimes);

  useEffect(() => {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    const dateTime = `${now.toISOString().slice(0, 10)}T${hours}:${minutes}:${seconds}`;

    const data = {
      date_time: dateTime,
      longitude: "02°09'32\"E",
      latitude: "41°23'19\"N",
    };

    const fetchInitialData = async () => {
      try {
       const response = await fetch(`${ import.meta.env.VITE_API_URL }/scaleTime/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (response.ok) {
          const result = await response.json();
          setTimes(result.data.date_time_sol, result.data.lon_hour, result.data.eot_hour, result.data.date_time_julian, result.data.date_time_gmst, result.data.date_time_mst, result.data.eoe_hour, result.data.sunrise, result.data.solar_noon, result.data.sunset, result.data.hour_italica, result.data.hour_babilonica);
        } else {
          console.error('Error en la petición a la API');
        }
      } catch (error) {
        console.error('Error de red:', error);
      }
    };

    fetchInitialData();
  }, [setTimes]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md">
        <Header />
        <UpperForm />
        <ShowResults />
      </Container>
    </ThemeProvider>
  );
}

export default App;

