import { UpperForm } from "./components/UpperForm";
import { Box } from "@mui/material";
import { ShowResults } from "./components/ShowResults";
import { Header } from "./components/Header";
import { useStore } from "./store/useStore";


function App() {
  const { 
    modifiedImage, 
    csvData, 
    csvPlate, 
    type, 
    setModifiedImage, 
    setCsvData, 
    setCsvPlate, 
    setType 
  } = useStore();

  const onNewImageModified = (newImageModified: string | null) => {
    setModifiedImage(newImageModified);
  };

  const onNewcsvData = (newcsvData: any[]) => {
    setCsvData(newcsvData);
  };

  const onNewcsvPlate = (newcsvPlate: any[]) => {
    setCsvPlate(newcsvPlate);
  };

  const onNewType = (type: string) => {
    setType(type);
  };

  return (
    <>
      <Header />
      <Box
        sx={{
          maxWidth: "800px",
          margin: "0 auto",
          textAlign: "center",
          padding: "20px",
          backgroundColor: "#f9f9f9",
          borderRadius: "8px",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        }}
      >
        <UpperForm
          onNewImageModified={onNewImageModified}
          onNewcsvData={onNewcsvData}
          onNewcsvPlate={onNewcsvPlate}
          onNewType={onNewType}
        />
        <ShowResults />
      </Box>
    </>
  );
}

export default App;