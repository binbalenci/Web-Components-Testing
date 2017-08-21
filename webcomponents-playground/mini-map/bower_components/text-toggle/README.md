[![Published on webcomponents.org](https://img.shields.io/badge/webcomponents.org-published-blue.svg)](https://www.webcomponents.org/element/jifalops/text-toggle)

# text-toggle
Show one of two strings based on a condition. Clickability optional.

## Installation

```
bower install --save jifalops/text-toggle
```

## Demo
See full demo for examples using Polymer.
<!--
```
<custom-element-demo>
  <template is="dom-bind">
    <script src="../webcomponentsjs/webcomponents-lite.js"></script>
    <link rel="import" href="text-toggle.html">
    <style>
      text-toggle {
        font-weight: bold;
        font-family: 'monospace';
      }
    </style>
    <next-code-block></next-code-block>
    <script>
      var reader = document.getElementById('reader');
      var writer = document.getElementById('writer');
      var cond = false;
      function toggle() {
        cond = !cond;
        reader.cond = cond;
        writer.cond = cond; // To mimic Polymer example
      }
      function read() {
        cond = writer.cond;
        reader.cond = cond;
      }
    </script>
  </template>
</custom-element-demo>
```
-->

```html

1. Show text based on outside condition.<br/>
<button onclick="toggle();">Toggle</button>
<text-toggle id="reader" t="true" f="false"></text-toggle>
<br/><br/>


2. Using element as control.
<text-toggle click-events t="true" f="false"></text-toggle>
<br/><br/>

3. As an HTML anchor.
<text-toggle link t="true" f="false"></text-toggle>
<br/><br/>

4. Chaging an outside condition.
<text-toggle id="writer" link t="true" f="false" onclick="setTimeout(read());"></text-toggle>
<br/><br/>
```

Full demo:
[webcomponents.org](https://www.webcomponents.org/element/jifalops/text-toggle/demo/demo/index.html)
| [github](https://jifalops.github.io/text-toggle/components/text-toggle/demo/).

API: [webcomponents.org](https://www.webcomponents.org/element/jifalops/text-toggle/text-toggle)
| [github](https://jifalops.github.io/text-toggle).

## Contributing

1. Fork it on Github.
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## License

[MIT](https://opensource.org/licenses/MIT)
