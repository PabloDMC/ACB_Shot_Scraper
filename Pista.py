from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

def draw_court(ax=None, color='black', lw=1, outer_lines=True):

    if ax is None:
        ax = plt.gca()

    # Crear las partes de la pista de baloncesto FIBA

    # Canasta
    hoop = Circle((0, 0), radius=45.72 / 2, linewidth=lw, color=color,
                  fill=False)

    # Tablero
    backboard = Rectangle((-90, -37.5), 180, -1, linewidth=lw,
                          color=color)

    # Pintura
    outer_box = Rectangle((-490 / 2, -157.5), 490, 580+120, linewidth=lw,
                          color=color, fill=False)

    # Circulo de tiros libres
    top_free_throw = Arc((0, 580-37.5), 360, 360, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    
    bottom_free_throw = Arc((0, 580-37.5), 360, 360, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    
    # Zona restringida
    restricted = Arc((0, 0), 2 * 125, 2 * 125, theta1=0, theta2=180,
                     linewidth=lw, color=color)

    # Linea de 3 puntos (se han adaptado las dimensiones a las coordenadas de los tiros de la pgania https://jv.acb.com/es)
    # Esquinas
    corner_three_a = Rectangle((-750 + 90, -157.5), 0, 419, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((750 - 90, -157.5), 0, 419, linewidth=lw,
                               color=color)
    # Arco
    three_arc = Arc((0, 120), 2 * 675, 2 * 675, theta1=12, theta2=180-12,
                    linewidth=lw, color=color)

    # Circulo central
    center_outer_arc = Arc((0, 1400-157.5), 2 * 180, 2 * 180, theta1=180,
                           theta2=0, linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box,
                      restricted, top_free_throw, bottom_free_throw,
                      corner_three_a, corner_three_b, three_arc,
                      center_outer_arc]
    if outer_lines:
        # Lineas delimitadoras del campo
        outer_lines = Rectangle((-750, -157.5), 1500, 1400, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Añadir los elementos de pista a los ejes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def shot_chart(anotado, fallado, title=None):
    """
    Carta de tiros encestados y fallados
    """
    plt.figure()
    draw_court()
    plt.plot(anotado['x'], anotado['y'], 'o', label='Anotado')
    plt.plot(fallado['x'], fallado['y'], 'x', markerfacecolor='none',
             label='Fallado')
    plt.legend()
    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    plt.title(title)
    plt.gca().set_axis_off()
    plt.show()
    return