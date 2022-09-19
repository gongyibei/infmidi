const websocket = new WebSocket("ws://localhost:8765/");
const MIN_dh = 5;
const MIN_dw = 20;

// var width = window.innerWidth;
// var height = window.innerHeight;
var dh = 20;
var dw = 80;
var notes = [];

var WIDTH = dw * 1000;
var HEIGHT = dh * 128;
var KEY_WIDTH = 30
var NAME_WIDTH = 30
var X_OFFSET = NAME_WIDTH + KEY_WIDTH;
var Y_OFFSET = 30;

var stage = new Konva.Stage({
  container: 'INFMIDI-Viewer',
  width: window.innerWidth,
  height: window.innerHeight,
});


// Draw backdrop 
var backdrop = new Konva.Layer();
stage.add(backdrop);

const set1 = new Set([0, 2, 3, 5, 7, 8, 10]);

function drawBackDrop() {
    for (let i = 0; i < HEIGHT / dh; i++) {
        if (set1.has(i%12)){
            // color = "#bbb"
            color = "rgb(163, 163, 163)";

        }else{
            // color = "#aaa"
            color = "rgb(150, 150, 150)";
        }

        backdrop.add(new Konva.Rect({
            x: 0 + X_OFFSET,
            y: i * dh + Y_OFFSET,
            width: WIDTH,
            height: i * dh + dh,
            fill: color,
            // stroke:"rgba(255,255,255,.3)",
            stroke:"rgb(156, 156, 156)",
            strokeWidth: 1,
        }));
    }
    for (let i = 1; i < Math.ceil(WIDTH / dw); i++) {
        backdrop.add(new Konva.Line({
            points: [i * dw + X_OFFSET, 0 + Y_OFFSET, i * dw + 1 + X_OFFSET, HEIGHT + Y_OFFSET],
            stroke: i % 4 === 0 ? "rgba(0,0,0,.3)" : "rgba(255,255,255,.3)",
            strokeWidth: 1,
        }))
    }
}

// Draw notes
var notelayer = new Konva.Layer();
stage.add(notelayer);

websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    
    notes = [];
    for (var note of event.notes) {
        var value = note[0];
        var velocity = note[1];
        var loc = note[2];
        var length = note[3]
        notes.push({i:127 - value,  j:loc, length, velocity});
    };
    drawNotes();

});

function drawNotes(){
    notelayer.destroyChildren();
    for (let { i, j, length, velocity} of notes) {
        notelayer.add(new Konva.Rect({
            x: j * dw + X_OFFSET,
            y: i * dh + Y_OFFSET,
            width: (length - 0.01) * dw,
            height: dh,
            // fill: "#d16eff",
            fill: "rgb(197, 100, 91)",
            cornerRadius: 5,
            opacity: velocity/(127 * 2) + 0.5,
        }))
    }

}


// Draw top bar
var topbar = new Konva.Layer();
stage.add(topbar)

function drawTopbar() {

    topbar.add(new Konva.Rect({
        x: X_OFFSET,
        y: 0,
        width: WIDTH,
        height: Y_OFFSET,
        // fill: "rgba(0,0,0,.3)",
        fill: "rgb(53, 53, 53)",
    }))

    for (let i = 1; i < Math.ceil(WIDTH / dw); i++) {
        topbar.add(new Konva.Line({
            points: [i * dw + X_OFFSET, 0 + 20, i * dw + X_OFFSET, Y_OFFSET],
            stroke: "rgba(0,0,0,.3)",
        }));
        topbar.add(new Konva.Text({
            x: i * dw + X_OFFSET + 3,
            y: Y_OFFSET - 15 - 3,
            text: String(i),
            fontSize: 15,
            fontFamily: 'Calibri',
            fill: 'white',
        }));
    }

}

// Drow left bar
var leftbar = new Konva.Layer();
stage.add(leftbar)

function drawLeftbar() {

    leftbar.add(new Konva.Rect({
        x: 0,
        y: Y_OFFSET,
        width: NAME_WIDTH,
        height: HEIGHT,
        // fill: "rgba(0,0,0,.3)",
        fill: "rgb(46, 46, 46)",
        // draggable: true,
        // onDragStart: function () {
        //   this.setState({
        //     start: {x: e.target.x(), y: e.target.y()},
        //     isDragging: true,
        //   });
        // },
        // onDragEnd: function (e){
        //     this.setState({
        //         isDragging: false,
        //     });
        //     dh = dh - (this.state.start.y - e.target.y) * 0.1;
        //     console.log(dh);
        // },
    }))

    for (let i = 1; i < 11; i++) {
        leftbar.add(new Konva.Line({
            points: [0, dh * (i * 12 - 4) + NAME_WIDTH, NAME_WIDTH, dh * (i * 12 - 4) + NAME_WIDTH],
            stroke: "rgba(0,0,0,.3)",
        }));
        leftbar.add(new Konva.Text({
            x: (NAME_WIDTH - 15) / 2,
            y: dh * (i * 12 - 4) + NAME_WIDTH - 17,
            text: 'C' + (10 - i),
            fontSize: 15,
            fontFamily: 'Calibri',
            fill: 'white',
        }));
    }


    for (let i = 0; i < HEIGHT / dh; i++) {
        if (set1.has(i%12)){
            color = "rgb(200, 200, 200)"
        }else{
            color = "rgb(26, 26, 26)"
        }

        leftbar.add(new Konva.Rect({
            x: NAME_WIDTH,
            y: i * dh + Y_OFFSET,
            width: KEY_WIDTH,
            height: i * dh + dh,
            fill: color,
            stroke:"rgb(76, 76, 76)",
            strokeWidth: 1,
        }));
    }
}

// Drow corner
var corner = new Konva.Layer();
stage.add(corner)

function drawCorner(){
    corner.add(new Konva.Rect({
        x: 0,
        y: 0,
        width: X_OFFSET,
        height: Y_OFFSET,
        // fill: "rgba(0,0,0,.3)",
        fill: "rgb(65, 65, 65)",
        shadowBlur: 5,
    }))

    corner.add(new Konva.Text({
        x: 11,
        y: -4,
        text: '∞',
        fontSize: 40,
        fontFamily: 'Calibri',
        fill: 'white',
    }))
}
function drawAll() {
    backdrop.destroyChildren();
    notelayer.destroyChildren();
    leftbar.destroyChildren();
    topbar.destroyChildren();
    corner.destroyChildren();
    drawBackDrop();
    drawNotes();
    drawLeftbar();
    drawTopbar();
    drawCorner();
}

stage.on('wheel', function (e) {
  // prevent parent scrolling
  e.evt.preventDefault();
  if (e.evt.x < 30 & e.evt.y > 30){
    dh = dh + e.evt.deltaX * 0.01
    WIDTH = dw * 1000;
    HEIGHT = dh * 128;
    drawAll();

  }else if(e.evt.y < 30 & e.evt.x > 30){
    dw = dw + e.evt.deltaY * 0.1;
    // dw = max(dw, MIN_dw);
    WIDTH = dw * 1000;
    HEIGHT = dh * 128;
    drawAll();

  }else{
    const dx = e.evt.deltaX;
    const dy = e.evt.deltaY;

    const minX = -(WIDTH - stage.width());
    const maxX = 0;

    const x = Math.max(minX, Math.min(backdrop.x() - dx, maxX));

    const minY = -(HEIGHT - stage.height());
    const maxY = 0;

    const y = Math.max(minY, Math.min(backdrop.y() - dy, maxY));
    backdrop.position({x, y });
    notelayer.position({x, y});
    topbar.x(x);
    leftbar.y(y);
  }
});

window.addEventListener("resize", resize);

function resize() {
    stage.width(window.innerWidth);
    stage.height(window.innerHeight);
}

drawAll();
