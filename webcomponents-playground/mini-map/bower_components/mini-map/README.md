[![Published on webcomponents.org](https://img.shields.io/badge/webcomponents.org-published-blue.svg)](https://www.webcomponents.org/element/jifalops/mini-map)

# mini-map
A drag-to-resize google-map with optional directions.

## Installation

```
bower install --save jifalops/mini-map
```

## Demo
Note: The demo is not working, but the element works when installed via bower.
<!--
```
<custom-element-demo>
  <template is="dom-bind">
    <script src="../webcomponentsjs/webcomponents-lite.js"></script>
    <link rel="import" href="mini-map.html">
    <next-code-block></next-code-block>
    <script>
      var lat = document.getElementById('lat');
      var lng = document.getElementById('lng');
      var refLat = document.getElementById('refLat');
      var refLng = document.getElementById('refLng');
      var map = document.getElementById('map');
      map.icon = 'marker.png';
      function update() {
        map.lat = Number(lat.value);
        map.lng = Number(lng.value);
        map.refLat = Number(refLat.value);
        map.refLng = Number(refLng.value);
      }
    </script>
  </template>
</custom-element-demo>
```
-->

```html
<input id="lat" value="1"/>lat<br/>
<input id="lng" value="1"/>lat<br/>
<input id="refLat" value="2"/>refLat<br/>
<input id="refLng" value="2"/>refLng<br/>
<button onclick="update()">Update</button><br/>
<mini-map id="map" api-key="AIzaSyAUPOaJubJnaRTPUd_xX8MOA62gRtSlfCc"></mini-map>
```

Full demo:
[webcomponents.org](https://www.webcomponents.org/element/jifalops/mini-map/demo/demo/index.html)
| [github](https://jifalops.github.io/mini-map/components/mini-map/demo/).

API: [webcomponents.org](https://www.webcomponents.org/element/jifalops/mini-map/mini-map)
| [github](https://jifalops.github.io/mini-map).

## Contributing

1. Fork it on Github.
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## License

[MIT](https://opensource.org/licenses/MIT)
