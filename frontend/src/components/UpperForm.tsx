import { Box,  Button, MenuItem, Select, TextField, FormControl, Divider, CircularProgress } from "@mui/material";
import { useStore } from "../store/useStore";

export const UpperForm = () => {
  const {
    imageFile,
    date,
    outputType,
    loading,
    setImageFile,
    setDate,
    setOutputType,
    fetchData,
    setType
  } = useStore();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && (file.type === "image/jpeg" || file.type === "image/png" || file.name.endsWith(".fits") || file.name.endsWith(".zip"))) {
      setImageFile(file);
    } else {
      alert("Por favor, selecciona un archivo JPG, PNG o FITS o ZIP.");
    }
  };

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDate(e.target.value);
  };

  const handleSelectChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setOutputType(value);
    setType(value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (imageFile) {
      await fetchData(imageFile, date);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Box display="flex"  flexWrap="wrap" justifyContent="center" alignItems="center" gap={2} >

        {/* Campo de selección de archivo */}
        <Box flex="1 1 auto" maxWidth={{ xs: "100%", sm: "60%" }}  padding={1} >
          <TextField type="file" onChange={handleFileChange}  accept=".jpg,.png,.fits,.zip"  />
        </Box>

        {/* Selector de fecha */}
        <Box flex="1 1 auto" maxWidth={{ xs: "100%", sm: "20%" }}  padding={1} >
          <TextField type="date" value={date} onChange={handleDateChange} fullWidth />
        </Box>

        {/* Selector de tipo de salida */}
        <Box  flex="1 1 auto"  maxWidth={{ xs: "100%", sm: "20%" }}  padding={1} >
          <FormControl fullWidth> 
            <Select labelId="output-type-label" value={outputType} onChange={handleSelectChange} >
              <MenuItem value="image">Imatge</MenuItem>
              <MenuItem value="table">Taula</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Box>
   
        {/* Botón de envío */}
        <Box sx={{ margin: "20px" }}>
          <Button type="submit" variant="contained" color="primary" disabled={loading}>
            {loading ? 'Carregant ...' : 'PROCESSAR'}
          </Button>
        </Box>


    <Divider></Divider>  

    {/* Spinner */}
    {loading && (   
      <Box sx={{ display: 'flex', justifyContent: "center", alignItems: "center"}}>
        <CircularProgress/>
      </Box>
    )}
  </form>
  )
}