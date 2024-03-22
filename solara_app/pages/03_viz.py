import ee
import geemap

import solara

year = solara.reactive(2019)


class Map(geemap.Map):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()

    def add_ee_data(self):
        ee.Authenticate()
        ee.Initialize(project='starthack-417820')

        # Load MODIS land cover images for multiple years
        years = range(2002, 2021)  # 2002 to 2020
        lc_images = []

        # Visualization parameters
        igbpLandCoverVis = {
            'min': 1.0,
            'max': 17.0,
            'palette': [
                '05450a', '086a10', '54a708', '78d203', '009900', 'c6b044',
                'dcd159', 'dade48', 'fbff13', 'b6ff05', '27ff87', 'c24f44',
                'a5a5a5', 'ff6d4c', '69fff8', 'f9ffa4', '1c0dff'
            ]
        }

        col = ee.ImageCollection('MODIS/006/MCD12Q1').select('LC_Type1');

        # A FeatureCollection defining Brazil boundary.
        fc = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017').filter(
            'country_na == "Brazil"'
        )

        # Clip the DEM by the Southeast Asia boundary FeatureCollection.
        # Iterate over the ImageCollection and clip each image to the FeatureCollection.
        col_clip = col.map(lambda img: img.clipToCollection(fc))
        DOY = col_clip.filterDate('2002-01-01', '2021-01-01');

        distinctDOY = col.filterDate('2002-01-01', '2021-01-01');

        num_images = distinctDOY.size().getInfo()

        print("Number of images in the collection:", num_images)
        print(f"HAAALO;: {year.value}")
        layer_names = ['MODIS ' + str(year) for year in range(2002, 2021)]
        print(layer_names)

        brazil_shapefile = ee.FeatureCollection("projects/starthack-417820/assets/Brazil")

        self.centerObject(brazil_shapefile)

        images = geemap.modis_timeseries(asset_id='MODIS/006/MCD12Q1', band_name='LC_Type1', roi=brazil_shapefile,
                                         start_year=2003, end_year=2021,
                                         start_date='01-01', end_date='12-31')

        # add map from 2020 to the map
        self.addLayer(images.first(), igbpLandCoverVis, '2020')

        self.add_legend(title="MODIS Land Cover", builtin_legend='MODIS/006/MCD12Q1')
        self.addLayerControl()


def update_year(x):
    print(x)


@solara.component
def Page():
    with solara.Column(style={"width": "100%"}):  # This is your main content area
        solara.Markdown("\n")
        solara.SliderInt(label="Vergleiche 2020 mit Jahr:", min=2002, max=2019, step=1, value=year,
                         on_value=update_year),

        Map.element(center=[40, -100], zoom=4, height="600px")
