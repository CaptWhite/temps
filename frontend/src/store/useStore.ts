import { create } from 'zustand'
import { getResources } from '../helpers/getResources';

const today = new Date();
const todayString = today.toISOString().split('T')[0];

interface StoreState {
  modifiedImage: string | null;
  csvData: any[];
  csvPlate: any[];
  type: string;
  loading: boolean;
  error: string | null;
  imageFile: File | '';
  date: string;
  outputType: string;
  radio1: string;
  radio2: string;
}

interface StoreActions {
  setModifiedImage: (image: string | null) => void;
  setCsvData: (data: any[]) => void;
  setCsvPlate: (plate: any[]) => void;
  setType: (type: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setImageFile: (file: File | '') => void;
  setDate: (date: string) => void;
  setOutputType: (type: string) => void;
  setRadio1: (value: string) => void;
  setRadio2: (value: string) => void;
  fetchData: (imageFile: File | '', date: string) => Promise<void>;
}

export const useStore = create<StoreState & StoreActions>((set) => ({
  modifiedImage: null,
  csvData: [],
  csvPlate: [],
  type: 'image',
  loading: false,
  error: null,
  imageFile: '' as File | '',
  date: todayString,
  outputType: 'image',
  radio1: 'position',
  radio2: 'degree',
  setModifiedImage: (image: string | null) => set({ modifiedImage: image }),
  setCsvData: (data: any[]) => set({ csvData: data }),
  setCsvPlate: (plate: any[]) => set({ csvPlate: plate }),
  setType: (type: string) => set({ type: type }),
  setLoading: (loading: boolean) => set({ loading: loading }),
  setError: (error: string | null) => set({ error: error }),
  setImageFile: (file: File | '') => set({ imageFile: file }),
  setDate: (date: string) => set({ date: date }),
  setOutputType: (type: string) => set({ outputType: type }),
  setRadio1: (value: string) => set({ radio1: value }),
  setRadio2: (value: string) => set({ radio2: value }),
  fetchData: async (imageFile: File | '', date: string) => {
    set({ loading: true, error: null });
    try {
      if (!(imageFile instanceof File)) {
        set({ error: 'No image file provided', loading: false });
        return;
      }
      const result = await getResources(imageFile, date + "T00:00:00");
      if (result && Array.isArray(result)) {
        const [blobImage, parsedData, parsedPlate] = result;
        if (blobImage) {
          set({ modifiedImage: URL.createObjectURL(blobImage), csvData: parsedData, csvPlate: parsedPlate, loading: false });
        } else {
          set({ error: 'Image blob is undefined', loading: false });
        }
      } else {
        set({ error: 'Failed to fetch resources', loading: false });
      }
    } catch (err: any) {
      set({ error: err.message, loading: false });
    }
  },
}))