import { Box, FormControl, FormControlLabel, FormLabel, Radio, RadioGroup, ThemeProvider, createTheme} from '@mui/material';
import { ShowImage } from './ShowImage';
import { ShowIcon } from './ShowIcon';
import { ShowTable } from './ShowTable';
import { useStore } from '../store/useStore';
// Tema personalizado
const theme = createTheme({  
  components: {    
    MuiFormControlLabel: {      
      styleOverrides: {        
        label: {          
          fontSize: "12px", // Tamaño de la fuente        
        }
      },    
    },  
  },
});

export const ShowResults = () => {
  const {
    type,
    modifiedImage,
    csvData,
    csvPlate,
    radio1,
    radio2,
    setRadio1,
    setRadio2
  } = useStore();
  const handleRadio1Change = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;    
    setRadio1(value);  
  }  
  const handleRadio2Change = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;    
    setRadio2(value);      
  }    
  console.log({csvData})

  return (
    <>       
      <ShowImage type={type} modifiedImage={modifiedImage} />      
      { csvData.length > 0 && type === 'table' && (
      <div style={{ marginTop: "10px"}}>        
        <Box display="flex" flexWrap="wrap" justifyContent="center" alignItems="center" gap={2} >
          {/* Selector de tipo de salida */}          
          <Box
            flex="1 1 auto" border={1} marginBottom={3} padding={1} maxWidth={{ xs: "100%", sm: "45%" }}>            
            <FormControl>
              <FormLabel id="demo-radio-buttons-group-label">Tipus de Taula</FormLabel>
              <ThemeProvider theme={theme}>                
                <RadioGroup                  
                  aria-labelledby="demo-radio-buttons-group-label" defaultValue="position"
                  name="radio-buttons-group" value={radio1} row onChange={handleRadio1Change} >
                  <FormControlLabel value="position" control={<Radio size="small" />} label="Posició" />
                  <FormControlLabel value="simbad"   control={<Radio size="small" />} label="Simbad"   />
                  <FormControlLabel value="placa"    control={<Radio size="small" />} label="Placa"    />
                </RadioGroup>
              </ThemeProvider>
            </FormControl>              
          </Box>          
          <Box
            flex="1 1 auto" border={1} marginBottom={3} padding={1} maxWidth={{ xs: "100%", sm: "45%" }}>
            <FormControl>
              <FormLabel id="demo-radio-buttons-group-label">Unitats</FormLabel>
                <ThemeProvider theme={theme}>
                  <RadioGroup                  
                  aria-labelledby="demo-radio-buttons-group-label" defaultValue="value"
                  name="radio-buttons-group" value={radio2} row onChange={handleRadio2Change} >
                  <FormControlLabel value="degree" control={<Radio size="small" />} label="000°" />
                  <FormControlLabel value="degree_dms"   control={<Radio size="small" />} label="0°00'00&quot;"   />
                  <FormControlLabel value="radian"    control={<Radio size="small" />} label="Radians"    />
                </RadioGroup>
              </ThemeProvider>
            </FormControl>
          </Box>
          <Box flex="1 1 auto" border={0} marginBottom={3} padding={1} maxWidth={{ xs: "100%", sm: "16.66%" }} >
            <ShowIcon parsedData={csvData} />
          </Box>
        </Box>
        {csvData.length > 0 && type === 'table' &&  radio1 === 'placa' &&
          <ShowTable csv={csvPlate} radio1={'plate'} unit={radio2}/>
        }

        <ShowTable csv={csvData} radio1={radio1} unit={radio2}/>
      </div>
      )}
    </>
  )}