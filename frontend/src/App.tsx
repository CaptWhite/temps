import { UpperForm } from "./components/UpperForm";
import { Box } from "@mui/material";
//import { ShowResults } from "./components/ShowResults";
import { Header } from "./components/Header";
import { ShowResults } from "./components/ShowResults";
//import { useStore } from "./store/useStore";


function App() {
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
        <UpperForm />
        <ShowResults />
      </Box>
    </>
  );
}

export default App;