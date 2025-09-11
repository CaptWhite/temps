import { useState } from 'react';
import { useStore } from '../store';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';

const UpperForm = () => {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');

  const [formData, setFormData] = useState({
    date: now.toISOString().slice(0, 10),
    time: `${hours}:${minutes}:${seconds}`,
    longitude: "02°09'32\"E",
    latitude: "41°23'19\"N",
  });

  const setTimes = useStore((state) => state.setTimes);
  const toggleUpdate = useStore((state) => state.toggleUpdate);
  const isUpdating = useStore((state) => state.isUpdating);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleProcess = async () => {
    const { date, time, longitude, latitude } = formData;
    const dateTime = `${date}T${time}`;

    const data = {
      date_time: dateTime,
      longitude,
      latitude,
    };

    try {
      const response = await axios.post<GetResourcesResponse>(`${ import.meta.env.VITE_API_URL }/scaleTime/`, formData, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        setTimes(result.data.date_time_sol, result.data.lon_hour, result.data.eot_hour, result.data.date_time_julian, result.data.date_time_gmst, result.data.date_time_mst, result.data.eoe_hour);
      } else {
        console.error('Error en la petición a la API');
      }
    } catch (error) {
      console.error('Error de red:', error);
    }
  };

  return (
    <Box sx={{ p: 2}}>
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 2, mb: 2 }}>
        <TextField
          id="date"
          name="date"
          label="Data"
          type="date"
          value={formData.date}
          onChange={handleChange}
          fullWidth
          inputProps={{ style: { fontSize: '0.9rem' } }}
          InputLabelProps={{
            shrink: true,
            style: { fontSize: '0.9rem' }
          }}
        />
        <TextField
          id="time"
          name="time"
          label="Hora"
          type="time"
          value={formData.time}
          onChange={handleChange}
          fullWidth
          inputProps={{
            step: 1,
            style: { fontSize: '0.9rem' }
          }}
          InputLabelProps={{
            shrink: true,
            style: { fontSize: '0.9rem' }
          }}
        />
        <TextField
          id="longitude"
          name="longitude"
          label="Longitud"
          value={formData.longitude}
          onChange={handleChange}
          fullWidth
          inputProps={{ style: { fontSize: '0.9rem' } }}
          InputLabelProps={{ style: { fontSize: '0.9rem' } }}
        />
        <TextField
          id="latitude"
          name="latitude"
          label="Latitud"
          value={formData.latitude}
          onChange={handleChange}
          fullWidth
          inputProps={{ style: { fontSize: '0.9rem' } }}
          InputLabelProps={{ style: { fontSize: '0.9rem ' } }}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleProcess}
          sx={{ width: '50%' }}
        >
          Processar
        </Button>
        <Button
          variant="contained"
          color={isUpdating ? 'secondary' : 'primary'}
          onClick={toggleUpdate}
          sx={{ width: '50%' }}
        >
          {isUpdating ? 'Pausar' : 'Rependre'}
        </Button>
      </Box>
    </Box>
  );
};

export default UpperForm;

