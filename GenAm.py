"""
Provides a simple console utility to animate an arbitrary higher-dimensional
function with some sensible defaults via matplotlib. Can only for the moment
use functions defined in numpy (which do not need to be indicated by np.sin,
np.cos, etc. and can instead be specified as sin, cos, etc.).
"""

from numpy import *
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D


fig3d = plt.figure()
ax = Axes3D(fig3d, auto_add_to_figure=False)
fig3d.add_axes(ax)

def setup():
    """
    Takes user input and returns the relevant values - the independent variables
    the higher-dimensional function will be evaluated on, whether or not the
    boundaries on the z-axis change with the function, the boundaries for the
    x, y, and z axes (set to a dummy -10, 10 if z is constant), the function
    itself, and the xy meshes over which the function will be evaluated.
    """
    limits = [  [float(input('Lower bound for x: ')),
                 float(input('Upper bound for x: '))],
                [float(input('Lower bound for y: ')),
                 float(input('Upper bound for y: '))] ]
    y_n = input('Should the z-value shown vary with the function? Y/N: ').lower()[0]
    variable_zlims = {'y': True, 'n': False}[y_n]
    if not variable_zlims:
        limits.append([float(input('Lower bound for z: ')),
                       float(input('Upper bound for z: '))])
    else:
        limits.append([-10, 10])

    meshes = meshgrid(arange(*limits[0], 0.1), arange(*limits[1], 0.1))
    variables = input('Input the independent variables as x, y, a, b, c ... : ')
    independents = list(variables.replace(', ', ''))
    funcstring = input('Input the function in terms of the previous variables: ')
    return independents, variable_zlims, limits, funcstring, meshes


def function(funcstring: str, x: float | list[ndarray], y: float | list[ndarray],
             higher: dict[str: float]) -> float | list[ndarray]:
    """
    Evaluates the function indicated by funcstring at the given values, returning
    the resultant float or mesh (as a list of numpy arrays).
    """
    return eval(funcstring, globals(), dict(**{'x': x, 'y': y}, **higher))


def animfunc(frame: int, max: int, sf: int | float, independents: list[str],
             variable_zlims: bool, limits: list[list[float]], funcstring: str,
            meshes: tuple, show_detailed: bool = True):
    """
    Performs the necessary actions for a single frame, taking the frame number,
    the maximum frame to increase to, the scale factor by which the increase
    in the higher-dimensional variable is computed, the list of independent
    variables, whether or not the boundaries for the z-axis vary, the boundaries
    for each axis, the string indicating the function to be evaluated, and the
    xy meshes over which the function is evaluated.
    
    The higher-dimensional variables increase together linearly from 0, given
    by the frame divided by the scale factor sf.
    """
    xlims, ylims, zlims = limits
    ax.cla()
    ax.set_xlim(*xlims)
    ax.set_ylim(*ylims)
    ax.set_zlim(*zlims)
    higher =independents[2:]
    if frame < max:
        higher = {param: frame / sf for param in higher}
    else:
        higher = {param: (max - (frame - max)) / sf for param in higher}
    if variable_zlims:
        limits[2][0] = 2 * abs(function(funcstring, xlims[0], ylims[0], higher))
        limits[2][1] = -1 * limits[2][0]
    z = function(funcstring, *meshes, higher)
    ax.plot_surface(*meshes, z, color='blue')
    if show_detailed:
        print(f'Frame: {frame}\n\t{str(higher)[1:-1].replace(":", " = ")}')


def animate(independents: list[str], variable_zlims: bool, limits: 
            list[list[int | float]], funcstring: str, meshes: tuple):
    """
    Does the background work of creating the animation and saving as a gif
    with the name provided to console.
    """

    def wrapped(frame):
        """
        Wraps the animfunc as a function of the frame supplemented by the arguments
        to animate.
        """
        return animfunc(frame, 100, 10, independents, variable_zlims,
                        limits, funcstring, meshes)

    filename = input('\nInput the name of the gif to save the animation to: ')
    print('Close the pyplot figure window to begin saving the animation.')
    anim = FuncAnimation(fig3d, wrapped, frames=200, interval=0.0001, repeat=False)
    plt.show()
    anim.save(f'{filename}.gif')


def main():
    animate(*setup())


if __name__ == '__main__':
    main()
