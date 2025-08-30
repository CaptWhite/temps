interface ShowImageProps {
  type: string;
  modifiedImage: string | null;
}

export const ShowImage = ({type, modifiedImage}: ShowImageProps) => { 

  return (
    <>
      <div style={{ marginTop: "20px" }}>
        { modifiedImage && type === 'image' &&   (
          <div>
            <h2>Imatge processada: </h2>
            <img src={modifiedImage} alt="Modificada" style={{ maxWidth: "100%", maxHeight: "700px" }} />
          </div>
        )}
      </div>       
    </>
  )
}