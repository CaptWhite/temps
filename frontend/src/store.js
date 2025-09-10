import { create } from 'zustand'

export const useStore = create((set) => ({
  utc: null,
  tai: null,
  gps: null,
  tt: null,
  eot: null,
  eoe: null,
  oficial: null,
  civil: null,
  solarMedia: null,
  solarVerdadera: null,
  juliana: null,
  gmst: null,
  mst: null,
  gast: null,
  ast: null,
  sunrise: null,
  solarNoon: null,
  sunset: null,
  hourItalica: null,
  hourBabilonica: null,
  isUpdating: true,
 
  setTimes: (utcTime, lon_hour, eot_hour, date_time_julian, date_time_gmst, date_time_mst, eoe_hour, sunrise, solar_noon, sunset, hour_italica, hour_babilonica) => {
    const utcDate = new Date(utcTime);
    const oficialDate = new Date(utcDate.getTime() + 2 * 60 * 60 * 1000);
    const civilDate = new Date(utcDate.getTime() + lon_hour * 60 * 60 * 1000);
    const solarMediaDate = new Date(utcDate.getTime() + lon_hour * 60 * 60 * 1000);
    const solarVerdaderaDate = new Date(solarMediaDate.getTime() - eot_hour * 60 * 60 * 1000);
    
    const utcHours = utcDate.getUTCHours() + utcDate.getUTCMinutes() / 60 + utcDate.getUTCSeconds() / 3600 + utcDate.getUTCMilliseconds() / 3600000;
    const tai = utcHours + 37 / 3600;
    const gps = utcHours + 18 / 3600;
    const tt = utcHours + 69.184 / 3600;

    set({ 
      utc: utcTime, 
      tai: tai,
      gps: gps,
      tt: tt,
      eot: eot_hour,
      eoe: eoe_hour,
      oficial: oficialDate.toISOString(), 
      civil: civilDate.toISOString(), 
      solarMedia: solarMediaDate.toISOString(),
      solarVerdadera: solarVerdaderaDate.toISOString(),
      juliana: date_time_julian,
      gmst: date_time_gmst,
      mst: date_time_mst,
      gast: date_time_gmst + eoe_hour,
      ast: date_time_mst + eoe_hour,
      sunrise: sunrise,
      solarNoon: solar_noon,
      sunset: sunset,
      hourItalica: hour_italica,
      hourBabilonica: hour_babilonica
    });
  },

  incrementTimes: () => set((state) => {
    if (state.utc) {
      const newUTCTime = new Date(new Date(state.utc).getTime() + 1000).toISOString();
      const newOficialTime = new Date(new Date(state.oficial).getTime() + 1000).toISOString();
      const newCivilTime = new Date(new Date(state.civil).getTime() + 1000).toISOString();
      const newSolarMediaTime = new Date(new Date(state.solarMedia).getTime() + 1000).toISOString();
      const newSolarVerdaderaTime = new Date(new Date(state.solarVerdadera).getTime() + 1000).toISOString();
      const newJuliana = state.juliana + (1/86400);
      const newGsmt = state.gmst + 1.002737909/3600;
      const newMst = state.mst + 1.002737909/3600;
      const newGast = state.gast + 1.002737909/3600;
      const newAst = state.ast + 1.002737909/3600;
      const newTai = state.tai + 1/3600;
      const newGps = state.gps + 1/3600;
      const newTt = state.tt + 1/3600;
      const newHourItalica = state.hourItalica + 1/3600;
      const newHourBabilonica = state.hourBabilonica + 1/3600;
      
      return { 
        utc: newUTCTime, 
        tai: newTai,
        gps: newGps,
        tt: newTt,
        oficial: newOficialTime, 
        civil: newCivilTime, 
        solarMedia: newSolarMediaTime,
        solarVerdadera: newSolarVerdaderaTime,
        juliana: newJuliana,
        gmst: newGsmt,
        mst: newMst,
        gast: newGast,
        ast: newAst,
        hourItalica: newHourItalica,
        hourBabilonica: newHourBabilonica
      };
    }
    return {};
  }),

  toggleUpdate: () => set((state) => ({ isUpdating: !state.isUpdating })),
}))
