
### ####################################################################################
#####    GRÁFICAS   ########################################################

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def graphics(ar, dec, zeta, theta, z, tMin, tMax, JDs):
  # global fig, gs, ax1, ax2, ax3
  # Primera fila - Tres gráficos

  # Crear una figura
  fig = plt.figure(figsize=(10, 8))
  fig.suptitle('')  # Título vacío para evitar 'Figure X'

  # Crear un GridSpec de 2 filas y 3 columnas
  gs = gridspec.GridSpec(2, 3)

  # Primera fila - Tres gráficos
  ax1 = fig.add_subplot(gs[0, 0])
  ax1.set_xlabel('Años', fontsize=9)
  ax1.set_ylabel('Angulo (segundos) ', fontsize=9)
  ax1.set_title('$ζ = 2306.2181\'\' T + 0.30188\'\' T^2 - 0.017998\'\' T^3$', fontsize=8)
  tex = ''
  ax1.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes )
  # Limitar los ejes
  ax1.set_xlim([tMin, tMax])
  ax1.plot(JDs, radian_to_degree(zeta), color='red')


  ax2 = fig.add_subplot(gs[0, 1])
  ax2.set_xlabel('Años', fontsize=9)
  ax2.set_ylabel('Angulo (segundos) ', fontsize=9)
  ax2.set_title('$𝜃 = 2004.3109\'\' T - 0.42665\'\' T^2 - 0.041833\'\' T^3$', fontsize=8)
  tex = ''
  ax2.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes )
  # Limitar los ejes
  ax2.set_xlim([tMin, tMax])
  ax2.plot(JDs, radian_to_degree(theta), color='red')


  ax3 = fig.add_subplot(gs[0, 2])
  ax3.set_xlabel('Años', fontsize=9)
  ax3.set_ylabel('Angulo (segundos) ', fontsize=9)
  ax3.set_title('$z = ζ + 0.79280\'\' T^2 + 0.000205\'\' T^3$', fontsize=8)
  tex = ''
  ax3.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax3.transAxes )
  # Limitar los ejes
  ax3.set_xlim([tMin, tMax])
  ax3.plot(JDs, radian_to_degree(z), color='red')

  # Segunda fila - Un solo gráfico que ocupe toda la fila (3 columnas)
  ax4 = fig.add_subplot(gs[1, :])
  ax4.set_xlabel('Años', fontsize=9)
  ax4.set_ylabel('Ascensión Recta (en grados) ', fontsize=9)
  ax4.set_title('Precesión desde el año 2000 hasta el 20000')
  tex = ''
  ax4.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax4.transAxes )
  # Limitar los ejes
  ax4.plot(JDs, radian_to_degree(dec), color='red')
  #ax4.plot(JDs, radian_to_degree(ar), color='blue')

  # Ajustar el layout para que no se solapen los elementos
  plt.tight_layout()

  # Mostrar los gráficos
  plt.show()

import matplotlib.pyplot as plt

def graphic3d(x1, x2, x3):
  # Graficar usando matplotlib
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  # Graficar el punto original
  ax.scatter(x1, x2, x3, color='red', label='Precesión  del Polo ecuatorial')
  ax.scatter(x1[0], x2[0], x3[0], color='blue', label='')
  ax.plot(x1, x2, x3, label='')

  # Configurar etiquetas y leyenda
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  ax.legend()

  # Mostrar la gráfica
  plt.show()



def graphicsNutation(ar, dec, dpsi, deps, w, tMin, tMax, JDs):
  
  # Crear una figura
  fig = plt.figure(figsize=(10, 8))
  fig.suptitle('')  # Título vacío para evitar 'Figure X'

  # Crear un GridSpec de 2 filas y 3 columnas
  gs = gridspec.GridSpec(2, 3)

  # Primera fila - Tres gráficos
  ax1 = fig.add_subplot(gs[0, 0])
  ax1.set_xlabel('Años', fontsize=9)
  ax1.set_ylabel('Angulo (segundos) ', fontsize=9)
  ax1.set_title('Notación en longitud\n Δψ=$-17.200 \\sin(Ω) - 1.319 \\sin(2*(f - d + Ω)) + ...$', fontsize=8)
  tex = ''
  ax1.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes )
  # Limitar los ejes
  ax1.set_xlim([tMin, tMax])
  ax1.plot(JDs, radian_to_degree(dpsi)*3600, color='red')


  ax2 = fig.add_subplot(gs[0, 1])
  ax2.set_xlabel('Años', fontsize=9)
  ax2.set_ylabel('Angulo (segundos) ', fontsize=9)
  ax2.set_title('Notación en oblicuidad\n Δϵ=$9.203\\cos(w) + 0.574\\cos(2*(f - d + w)) + ...$', fontsize=8)
  tex = ''
  ax2.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes )
  # Limitar los ejes
  ax2.set_xlim([tMin, tMax])
  ax2.plot(JDs, radian_to_degree(deps)*3600, color='red')


  ax3 = fig.add_subplot(gs[0, 2])
  ax3.set_xlabel('Años', fontsize=9)
  ax3.set_ylabel('cos(Ω)', fontsize=9)
  ax3.set_title('Ω: Longitud ascendente del nodo lunar\n$\\cos(Ω) = \\cos(125.04452 - 1934.136261 · T)$', fontsize=8)
  tex = ''
  ax3.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax3.transAxes )
  # Limitar los ejes
  ax3.set_xlim([tMin, tMax])
  cosw = [math.cos(it) for it in w]
  ax3.plot(JDs, cosw, color='red')

  # Segunda fila - Un solo gráfico que ocupe toda la fila (3 columnas)
  ax4 = fig.add_subplot(gs[1, :])
  ax4.set_xlabel('Años', fontsize=9)
  ax4.set_ylabel('Declinación (en grados) ', fontsize=9)
  ax4.set_title(f'Precesión desde el año {tMin} hasta el {tMax}')
  tex = ''
  ax4.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax4.transAxes )
  # Limitar los ejes
  ax4.plot(JDs, radian_to_degree(dec), color='red')
  #ax4.plot(JDs, radian_to_degree(ar), color='blue')

  # Ajustar el layout para que no se solapen los elementos
  plt.tight_layout()

  # Mostrar los gráficos
  plt.show()


def graphics_0_Aberration():
  global fig, gs
  # Crear una figura
  fig = plt.figure(figsize=(8, 8))
  fig.suptitle('ABERRACIÓN ANUAL', fontsize=18)  # Título vacío para evitar 'Figure X'

  # Crear un GridSpec de 2 filas y 3 columnas
  gs = gridspec.GridSpec(3, 3)
  return fig, gs

def graphics_9_Aberration(): 
  global fig, gs
  # Ajustar el layout para que no se solapen los elementos
  plt.tight_layout()

  # Mostrar los gráficos
  plt.show(block=True)


def graphics_Aberration(ar, dec, ar_astro, dec_astro, descr_astro, item, tMin, tMax, JDs):
  global fig, gs, ax1, ax2, ax3
  # Primera fila - Tres gráficos

  ax1 = fig.add_subplot(gs[item, 0])
  ax1.set_xlabel('Dias', fontsize=9)
  ax1.set_ylabel('Ascension Recta (seg) ', fontsize=9)
  ax1.set_title('', fontsize=8)
  tex = ''
  ax1.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes )
  # Limitar los ejes
  ax1.set_xlim([tMin - JDs[0], tMax - JDs[0]])
  ax1.plot(JDs - JDs[0], (ar - ar_astro)*3600, color='red')


  ax2 = fig.add_subplot(gs[item, 1])
  ax2.set_xlabel('Días', fontsize=9)
  ax2.set_ylabel('Declinación (seg) ', fontsize=9)
  ax2.set_title(descr_astro, fontsize=12, color='red')
  tex = ''
  ax2.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes )
  # Limitar los ejes
  ax2.set_xlim([tMin - JDs[0], tMax - JDs[0]])
  ax2.plot(JDs - JDs[0], (dec - dec_astro)*3600, color='red')


  ax3 = fig.add_subplot(gs[item, 2])
  ax3.set_xlabel('Ascención recta (seg)', fontsize=9)
  ax3.set_ylabel('Declinación (seg) ', fontsize=9)
  ax3.set_title('', fontsize=8)
  tex = ''
  ax3.text(1, 0, tex, fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax3.transAxes )
  # Limitar los ejes
  ax3.set_xlim([-40, 40])
  ax3.set_ylim([-40, 40])
  ax3.plot((ar - ar_astro)*3600, (dec - dec_astro)*3600, color='red')





### ####################################################################################
if __name__ == "__main__":
    date = '2024-06-04 21:00:00'
    spl = date.replace('-', ' ').replace(':', ' ').split(' ')
    jdate = julian_date(int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3]), int(spl[4]))
    print (jdate)
    print()

