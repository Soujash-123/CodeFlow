from pyflowchart import Flowchart
code = """from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        vertex = queue.popleft()
        print(vertex, end=" ")

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

# Example graph representation using adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Starting node for BFS traversal
start_node = 'A'

print("Breadth First Traversal starting from {}: ".format(start_node))
bfs(graph, start_node)
"""
fc = Flowchart.from_code(code)
print(fc.flowchart())

code = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Flowchart</title>
<style type="text/css">
  .end-element { fill : #FFCCFF; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.3.0/raphael.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/flowchart/1.17.1/flowchart.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.1/js/bootstrap.bundle.min.js"></script>
<script>
    window.onload = function () {
        var chart;

        function drawFlowchart() {
            var code = `'''+fc.flowchart()+'''`;

            if (chart) {
              chart.clean();
            }

            chart = flowchart.parse(code);
            chart.drawSVG('canvas', {
              'x': 0,
              'y': 0,
              'line-width': 3,
              'line-length': 50,
              'text-margin': 10,
              'font-size': 14,
              'font': 'normal',
              'font-family': 'Helvetica',
              'font-weight': 'normal',
              'font-color': 'black',
              'line-color': 'black',
              'element-color': 'black',
              'fill': 'white',
              'yes-text': 'yes',
              'no-text': 'no',
              'arrow-end': 'block',
              'scale': 1,
              'symbols': {
                'start': {
                  'font-size': 14,
                  'font-color': 'yellow',
                  'element-color': 'blue',
                  'fill': 'green',
                  'class': 'start-element'
                },
                'inputoutput': {
                  'font-color': 'black',
                  'element-color': 'black',
                  'fill': 'bisque'
                },
                'operation': {
                  'font-color': 'black',
                  'element-color': 'black',
                  'fill': 'linen'
                },
                'subroutine': {
                  'font-color': 'black',
                  'element-color': 'blue',
                  'fill': 'lightgreen'
                },
                'condition': {
                  'font-color': 'red',
                  'element-color': 'black',
                  'fill': 'yellow'
                },
                'end':{
                  'font-size': 20,
                  'class': 'end-element'
                }
              },
              'flowstate' : {
                'request' : { 'fill' : 'blue'},
                'invalid': {'fill' : '#444444'},
                'approved' : { 'fill' : '#58C4A3', 'font-size' : 12, 'yes-text' : 'APPROVED', 'no-text' : 'n/a' },
                'rejected' : { 'fill' : '#C45879', 'font-size' : 12, 'yes-text' : 'n/a', 'no-text' : 'REJECTED' }
              }
            });
        }

        // Draw flowchart initially
        drawFlowchart();
    };

    //derived from https://stackoverflow.com/a/64800570
    //we need to use web browser canvas to generate a image. In this case png
    let imageUtil = {};

    /**
     * converts a base64 encoded data url SVG image to a PNG image
     * @param originalBase64 data url of svg image
     * @param width target width in pixel of PNG image
     * @param secondTry used internally to prevent endless recursion
     * @return {Promise<unknown>} resolves to png data url of the image
     */
    imageUtil.base64SvgToBase64Png = function (originalBase64, width, height, secondTry) {
        return new Promise(resolve => {
            let img = document.createElement('img');
            img.onload = function () {
                if (!secondTry && (img.naturalWidth === 0 || img.naturalHeight === 0)) {
                    let svgDoc = base64ToSvgDocument(originalBase64);
                    let fixedDoc = fixSvgDocumentFF(svgDoc);
                    return imageUtil.base64SvgToBase64Png(svgDocumentToBase64(fixedDoc), width, height, true).then(result => {
                        resolve(result);
                    });
                }

                let canvas2 = document.createElement("canvas");
                canvas2.width = width;
                canvas2.height = height;
                let ctx = canvas2.getContext("2d");
                ctx.drawImage(img, 0, 0, canvas2.width, canvas2.height);
                try {
                    let data = canvas2.toDataURL('image/png');
                    resolve(data);
                } catch (e) {
                    resolve(null);
                }
            };
            img.src = originalBase64;
        });
    }

    //needed because Firefox doesn't correctly handle SVG with size = 0, see https://bugzilla.mozilla.org/show_bug.cgi?id=700533
    function fixSvgDocumentFF(svgDocument) {
        try {
            let widthInt = parseInt(svgDocument.documentElement.width.baseVal.value) || 500;
            let heightInt = parseInt(svgDocument.documentElement.height.baseVal.value) || 500;
            svgDocument.documentElement.width.baseVal.newValueSpecifiedUnits(SVGLength.SVG_LENGTHTYPE_PX, widthInt);
            svgDocument.documentElement.height.baseVal.newValueSpecifiedUnits(SVGLength.SVG_LENGTHTYPE_PX, heightInt);
            return svgDocument;
        } catch (e) {
            return svgDocument;
        }
    }

    function svgDocumentToBase64(svgDocument) {
        try {
            let base64EncodedSVG = btoa(new XMLSerializer().serializeToString(svgDocument));
            return 'data:image/svg+xml;base64,' + base64EncodedSVG;
        } catch (e) {
            return null;
        }
    }

    function base64ToSvgDocument(base64) {
        let svg = atob(base64.substring(base64.indexOf('base64,') + 7));
        svg = svg.substring(svg.indexOf('<svg'));
        let parser = new DOMParser();
        return parser.parseFromString(svg, "image/svg+xml");
    } 
</script>
</head>
<body>
    <div id="canvas"></div>
</body>
</html>
'''
with open("flowchart.html","w") as file:
    file.write(code)
