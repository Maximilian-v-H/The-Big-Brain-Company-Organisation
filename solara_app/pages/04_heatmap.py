import ee
import geemap
import reacton

import solara


class PopulationHeatmap(geemap.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()

    def add_ee_data(self):
        # Initialize the Earth Engine library.
        ee.Initialize()

        # Load the shapefile for Brazil.
        brazil_shapefile = ee.FeatureCollection("projects/starthack-417820/assets/Brazil")

        # Load the .tif files into an ImageCollection.
        burned_collection = ee.ImageCollection("projects/starthack-417820/assets/bra")

        # Get the number of images in the ImageCollection.
        num_images = burned_collection.size().getInfo()
        print("Number of images in the collection:", num_images)

        # Convert the ImageCollection to a single multiband image.
        burned_image = burned_collection.toBands()

        # Reduce the multiband image to a single band image that represents the sum of all bands.
        burned_count = burned_image.reduce(ee.Reducer.sum())

        # Normalize the burned count to a range of 0 to 1.
        max_burned_count = burned_count.reduceRegion(reducer=ee.Reducer.max(), geometry=brazil_shapefile, scale=800,
                                                     maxPixels=1e13).get('sum').getInfo()
        normalized_burned_count = burned_count.divide(max_burned_count)

        # Define a color palette for the heatmap.
        heatmap_palette = ['blue', 'yellow', 'red']

        # Add the heatmap layer to the map.
        self.addLayer(normalized_burned_count, {'min': 0, 'max': 1, 'palette': heatmap_palette}, 'Burned Area Heatmap')

        # Define a Gaussian kernel with a radius of 3 pixels.
        gaussian_kernel = ee.Kernel.gaussian(radius=200, units='pixels', sigma=1)

        # Convolve the image with the Gaussian kernel to blur it.
        blurred_burned_count = normalized_burned_count.convolve(gaussian_kernel)

        # Define a color palette for the heatmap.
        # Define a color palette for the heatmap.
        heatmap_palette = ['#FF4500', '#B22222', '#8B0000', '#800000', '#550000', '#300000']

        # Add the heatmap layer to the map.
        self.addLayer(blurred_burned_count, {'min': 0, 'max': 1, 'palette': heatmap_palette}, 'Burned Area Heatmap')
        self.addLayer(brazil_shapefile, name='Brazil', opacity=0.5)


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        PopulationHeatmap.element(
            center=[-14.235004, -51.92528],
            zoom=4,
            height="600px",
        )
