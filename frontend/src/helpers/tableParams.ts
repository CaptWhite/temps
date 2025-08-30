export const tableParams: any = 
  {
    position: {
      type : 'position',
      align : ["right", "left", "right", "right", "right", "right"],
      float : [false, false, true, true, true, true ],
      title : ["Id_", "Estrella", "AR", "Dec", "Pos X", "Pos Y"],
      parseNumbers: [(c: any) => c, (c: any) => c, 
        (c: any, t='degree') => (t!=='degree_dms') ? parseFloat(c).toFixed(8) : c, 
        (c: any, t='degree') => (t!=='degree_dms') ? parseFloat(c).toFixed(8) : c.slice(1,-2), 
        (c: any) => parseFloat(c).toFixed(8), 
        (c: any) => parseFloat(c).toFixed(8) ], 
      createRows :  (csv: any) => {
        const csvObj = csv.slice(1,-1).map((fila: any) => { return Object.fromEntries(fila.map((valor: any, i: number) => [csv[0][i], valor])) })

        const rows1 = csvObj.map(({ id, main_id, ar_app, dec_app, field_x, field_y }: any) => ({ id, star:main_id, ra:ar_app, dec:dec_app, pos_x:field_x, pos_y:field_y  }))

        const rows2 = csvObj.map(({ id, main_id, ra_app_dms, dec_app_hms, field_x, field_y }: any) => ({ id, star:main_id, ra:ra_app_dms, dec:dec_app_hms, pos_x:field_x, pos_y:field_y   }))  

        const rows3 = csvObj.map(({ id, main_id, ar_app_rad, dec_app_rad, field_x, field_y }: any) => ({ id, star:main_id, ra:ar_app_rad, dec:dec_app_rad, pos_x:field_x, pos_y:field_y  })) 

        return {rows1, rows2, rows3}
      }
    },

    simbad: {
      type : 'simbad',
      align : ["right", "left", "right", "right", "right", "right", "right", "right"],
      float : [false, false, true, true, false, false, false, false],
      title : ["Id", "Estrella", "AR(J2000)", "Dec(J2000)", "pmar", "pmdec", "plx", "vrz"],
      parseNumbers: [(c: any) => c, (c: any) => c,
        (c: any, t='degree') => (t!=='degree_dms') ? parseFloat(c).toFixed(8) : c, 
        (c: any, t='degree') => (t!=='degree_dms') ? parseFloat(c).toFixed(8) : c.slice(1,-2),
        (c: any) => c, (c: any) => c, (c: any) => c, (c: any) => c ], 
      createRows :  (csv: any) => {
        const csvObj = csv.slice(1,-1).map((fila: any) => { return Object.fromEntries(fila.map((valor: any, i: number) => [csv[0][i], valor])) })

        const rows1 = csvObj.map(({ id, main_id, ra, dec, pmra_x, pmdec_x, plx_value, rvz_radvel }: any) => ({ id, star:main_id, ra, dec, pmra:pmra_x, pmdec:pmdec_x, plx:plx_value, rvz:rvz_radvel  }))

        const rows2 = csvObj.map(({ id, main_id, ra_dms, dec_hms, pmra_x, pmdec_x, plx_value, rvz_radvel }: any) => ({ id, star:main_id, ra:ra_dms, dec:dec_hms, pmra:pmra_x, pmdec:pmdec_x, plx:plx_value, rvz:rvz_radvel   }))  

        const rows3 = csvObj.map(({ id, main_id, ra_rad, dec_rad, pmra_x, pmdec_x, plx_value, rvz_radvel }: any) => ({ id, star:main_id, ra:ra_rad, dec:dec_rad, pmra:pmra_x, pmdec:pmdec_x, plx:plx_value, rvz:rvz_radvel   })) 

        return {rows1, rows2, rows3}
      }
    },  
  
    placa: {
      type : 'placa',
      align : ["right", "left", "right", "right", "right", "right"],
      title : ["Id", "Estrella", "Pos X", "Pos Y", "AR Residual", "Dec Residual"],
      parseNumbers: [(c: any) => c, (c: any) => c, 
        (c: any) => parseFloat(c).toFixed(8), 
        (c: any) => parseFloat(c).toFixed(8), 
        (c: any) => parseFloat(c).toExponential(4), 
        (c: any) => parseFloat(c).toExponential(4) ], 
      createRows :  (csv: any) => {
        const csvObj = csv.slice(1,-1).map((fila: any) => { return Object.fromEntries(fila.map((valor: any, i: number) => [csv[0][i], valor])) })

        const rows1 = csvObj.map(({ id, main_id, field_x, field_y,  ra_resid, dec_resid}: any) => ({ id, star:main_id, pos_x:field_x, pos_y:field_y, ra_resid, dec_resid  }))

        const rows2 = csvObj.map(({ id, main_id, field_x, field_y,  ra_resid, dec_resid}: any) => ({ id, star:main_id, pos_x:field_x, pos_y:field_y, ra_resid, dec_resid  }))

        const rows3 = csvObj.map(({ id, main_id, field_x, field_y,  ra_resid, dec_resid}: any) => ({ id, star:main_id, pos_x:field_x, pos_y:field_y, ra_resid, dec_resid  }))

        return {rows1, rows2, rows3}
      }
    }, 
    plate: {
      type : 'plate',
      align : ["right", "right", "right"],
      title : ["Coef.", "AR Res.", "DEC Res."],
      parseNumbers: [(c: any) => c, 
        (c: any) => parseFloat(c).toExponential(8), 
        (c: any) => parseFloat(c).toExponential(8), 
       ], 
      createRows :  (csv: any) => {
        const csvObj = csv.slice(1,-1).map((fila: any) => { return Object.fromEntries(fila.map((valor: any, i: number) => [csv[0][i], valor])) })

        const rows1 = csvObj.map(({ Coef, AR, DEC}: any) => ({ Coef, AR, DEC}))
        const rows2 = rows1
        const rows3 = rows1

        return {rows1, rows2, rows3}
      }
    }  
  }