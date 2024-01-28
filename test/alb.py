from flask import Flask, render_template

import svgwrite

def draw_arrow():
    dwg = svgwrite.Drawing('arrow.svg', profile='tiny')

    # Disegna la linea della freccia
    dwg.add(dwg.line(start=(50, 50), end=(200, 50), stroke='black'))

    # Disegna la punta della freccia come un triangolo
    dwg.add(dwg.polygon(points=[(200, 50), (180, 40), (180, 60)], fill='black'))

    # Salva il file SVG
    dwg.save()

draw_arrow()
app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'your secret key'
@app.route('/', methods=('GET', 'POST'))
def index():
      tree_html = draw_arrow()
    # Dati dello schema ad albero
      tree_data = {
            "name": "Root",
            "children": [
                  {
                  "name": "Node 1",
                  "children": [
                        {"name": "Leaf 1"},
                        {"name": "Leaf 2"}
                  ]
                  },
                  {
                  "name": "Node 2",
                  "children": [
                        {"name": "Leaf 3"},
                        {"name": "Leaf 4"}
                  ]
                  }
            ]
      }

      return render_template('alb.html', tree_data=tree_html)

if __name__ == '__main__':
      app.run(debug=True)