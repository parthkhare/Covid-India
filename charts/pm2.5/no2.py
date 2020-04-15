var c = c0.select('NO2_column_number_density');

var start = ee.Date('2020-02-01');
var start2019 = start.advance(-1,'year');
var now = ee.Date(Date.now());
var now2019 = now.advance(-1,'year');

var s1 = start2019.format('YYYY-MMM-dd').cat(' to ').cat(now2019.format('YYYY-MMM-dd')).getInfo();
var s2 = start.format('YYYY-MMM-dd').cat(' to ').cat(now.format('YYYY-MMM-dd')).getInfo();

var im1 = c.filterDate(start2019,now2019)
  .mean().multiply(1e6); //micromol
var im2 = c.filterDate(start,now)
  .mean().multiply(1e6); //micromol

//var p=['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red'];
var p=['f1eef6','d7b5d8','df65b0','dd1c77','980043'];
var vis={min:50, max:300, palette:p};

var m1 = im1.gt(50);
var m2 = im2.gt(50);

var mapStyle = [
    {
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#444444"
            }
        ]
    },
    {
        "featureType": "administrative.neighborhood",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "hue": "#ff9700"
            },
            {
                "saturation": "-6"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [
            {
                "color": "#f2f2f2"
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "visibility": "off"
            },
            {
                "color": "#e3ffcc"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "all",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "lightness": 45
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "all",
        "stylers": [
            {
                "color": "#4FA5E0"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#deeeff"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "labels.text",
        "stylers": [
            {
                "color": "#deeeff"
            }
        ]
    }
];

ui.root.clear();
ui.root.add(ui.Map());
var Map1 = ui.root.widgets().get(0);

Map1.setOptions('mapStyle', {mapStyle: mapStyle});
Map1.setCenter(112, 30, 5);
Map1.addLayer(im1.updateMask(m1),vis,'2019',true,0.6);

var linkedMap = new ui.Map();
linkedMap.setOptions('mapStyle', {mapStyle: mapStyle});
linkedMap.addLayer(im2.updateMask(m2), vis, '2020',true,0.6);

// Link the default Map to the other map.
var linker = ui.Map.Linker([Map1, linkedMap]);

// Create a SplitPanel which holds the linked maps side-by-side.
var splitPanel = new ui.SplitPanel({
  firstPanel: linker.get(0),
  secondPanel: linker.get(1),
  orientation: 'horizontal',
  wipe: true,
  style: {stretch: 'both'}
});

// set legend position of panel
var legend = ui.Panel({
style: {
position: 'bottom-left',
padding: '8px 15px'
}
});

// Create legend title
var legendTitle = ui.Label({
value: 'NO2 (µmol/m²)',
style: {
fontWeight: 'bold',
margin: '0 0 0 0',
padding: '0'
}
});
 
// Add the title to the panel
legend.add(legendTitle);
 
// create the legend image
var lat = ee.Image.pixelLonLat().select('latitude');
var gradient = lat.multiply((vis.max-vis.min)/100.0).add(vis.min);
var legendImage = gradient.visualize(vis);
 
// create text on top of legend
var panel = ui.Panel({
widgets: [
ui.Label(vis['max'])
],
});
 
legend.add(panel);
 
// create thumbnail from the image
var thumbnail = ui.Thumbnail({
image: legendImage,
params: {bbox:'0,0,10,100', dimensions:'10x100'},
style: {padding: '1px', position: 'bottom-left'}
});
 
// add the thumbnail to the legend
legend.add(thumbnail);

// create text on top of legend
var panel = ui.Panel({
widgets: [
ui.Label(vis['min'])
],
});
 
legend.add(panel);

Map1.add(legend);
Map1.add(ui.Label(s1,{position:'top-left'}));
linkedMap.add(ui.Label(s2,{position:'top-right'}));

// Set the SplitPanel as the only thing in root.
ui.root.widgets().reset([splitPanel]);
