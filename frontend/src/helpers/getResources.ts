import axios from 'axios';
import { Base64 } from 'js-base64';

interface GetResourcesResponse {
  imagen: string;
  csv: string;
  plate: string;
}

export const getResources = async (
  imageFile: File,
  date: string
): Promise<[Blob, string[][], string[][]] | []> => {
  if (!imageFile || !date) { 
    alert("Por favor, selecciona un archivo y una fecha.");
    return [];
  }

  try {
      // Leer el archivo como ArrayBuffer
      const fileBuffer = await imageFile.arrayBuffer();
      // Convertir ArrayBuffer a Blob
      const fileBlob = new Blob([fileBuffer], { type: imageFile.type });

      const formData = new FormData();
      formData.append("file", fileBlob, imageFile.name);
      formData.append("filename", imageFile.name);
      formData.append("msg", "hello");
      formData.append("date", date);

      const response = await axios.post<GetResourcesResponse>(`${ import.meta.env.VITE_API_URL }/upload/`, formData, {
      // const response = await axios.post<GetResourcesResponse>(`/api/upload/`, formData, {
      //const response = await axios.post<GetResourcesResponse>(`http://localhost:8000/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'json' 
      });

      // Leer la imagen modificada desde la respuesta
      const imgBase64 = response.data.imagen;
      const decodedImg = Base64.toUint8Array(imgBase64);
      const blob = new Blob([decodedImg], { type: 'image/jpeg' });

      const csvString = response.data.csv
      let csvRows = csvString.split('\n');
      csvRows = csvRows.map((row: string) => row.trimEnd());
    //const parsedData: string[][] = csvRows.map((row: string) => row.split(','));
      const parsedData = csvRows.map(row => {
        // Expresión regular mejorada para manejar comillas escapadas
        const regex = /("((?:[^"]|"")*)"|[^,]+)/g;
        const matches = [...row.matchAll(regex)].map(match => match[1]);
        return matches;
     });
     

      const plateString = response.data.plate
      const plateRows = plateString.split('\n');
      const parsedPlate = plateRows.map((row: string) => row.trimEnd().split(','));


      return [blob, parsedData, parsedPlate]
  } catch (error) {
      console.error("Error al enviar la solicitud:", error);
      alert("Error al procesar la imagen. Por favor, inténtalo de nuevo.");
      return []
  }
}

