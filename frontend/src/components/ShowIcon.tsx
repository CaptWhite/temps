import { Box } from '@mui/material';
import ExcelIcon from '../assets/excel.svg?react';




interface ShowIconProps {
  parsedData: string[][];
  fileName?: string;
}

export const ShowIcon = ({ parsedData, fileName = 'data.csv' }: ShowIconProps) => {
  const handleDownload = () => {
    // Generar contenido CSV
    const csvContent =
      parsedData.map((field) => field.join(';').replaceAll('.', ',').replaceAll('°', 'º')) // Une las filas con saltos de línea
    const csvContent2 = csvContent.join('\n')
    // Crear Blob para el CSV
    const blob = new Blob([csvContent2], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    // Crear enlace de descarga
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
      <div onClick={handleDownload} style={{ cursor: 'pointer' }}>
        <ExcelIcon />
      </div>
    </Box>
  );
};