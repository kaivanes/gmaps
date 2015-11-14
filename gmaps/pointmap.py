from ipywidgets import widgets
from traitlets import List, Unicode, Bool

from . import ipy23_compat
from . import gmaps_traitlets


class PointMapWidget(widgets.DOMWidget):
    _view_name = Unicode('PointMapView', sync=True)
    _bounds = List(sync=True) 
    _data = List(sync=True)
    _info = List(sync=True)
    height = gmaps_traitlets.CSSDimension(sync=True)
    width = gmaps_traitlets.CSSDimension(sync=True)

    def __init__(self, data, height, width, info=None):
        if sum([int(len(x) == 2) for x in data]) != len(data):
            raise ValueError("Items in 'data' list must be of length 2 [ latitude, longitude ]")

        self._data = data
        self.height = height
        self.width = width

        if info is not None:
            self._info = info
        else:
            self._info = []

        self._bounds = self._calc_bounds()
        super(widgets.DOMWidget, self).__init__()

    def _calc_bounds(self):
        min_latitude = min(data[0] for data in self._data)
        min_longitude = min(data[1] for data in self._data)
        max_latitude = max(data[0] for data in self._data)
        max_longitude = max(data[1] for data in self._data)
        return [ (min_latitude, min_longitude), (max_latitude, max_longitude) ]


def pointmap(data, height="400px", width="700px", info=None):
    """
    Draw a list of markers on a map at given coordinates.

    Renders a list 'data' consisting of pairs of floats denoting (latitude, longitude),
    as a series of markers on a map

    Arguments
    ---------
    data: list (or Numpy Array) of pairs or triples of floats.
        This is a list of coordinate, possibly associated with a weight. 
        Each element in the list should be a pair 
        (either a list or a tuple) of floats, or a triple
        of floats. The first float should indicate the 
        coordinate's longitude and the second should indicate the 
        coordinate's latitude. If a third float is provided,
        it is interpreted as a weight for that data point.
        Google maps only accepts positive weights.

    Optional arguments
    ------------------
    height: int or string
        Set the height of the map. This can be either an int,
        in which case it is interpreted as a number of pixels, 
        or a string with units like "400px" or "20em".
    width: int or string
        Set the width of the map. This can be either an int,
        in which case it is interpreted as a number of pixels, 
        or a string with units like "400px" or "20em".
    info: list
        A list of strings representing the content of a popup
        window to be rendered when the relevant marker is clicked.

    Returns
    -------
    PointMapWidget
        IPython notebook widget containing the map. Display it
        with a call to 'display'.
    
    Examples
    --------
    >>> data = [ [ 37.782551,-122.445368 ],
    ...          [ 37.782745,-122.444586 ],
    ...          [ 37.782842,-122.443858 ] ]
    >>> w = pointmap(data)
    >>> display(w)
    """
    try:
        data = data.tolist()
    except AttributeError:
        # Not a Numpy Array.
        pass
    w = PointMapWidget(data, height, width, info)
    return w
