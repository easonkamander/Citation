 const bounds = {
 	width:  [16, 800],
	height: [8,  100],
	top:    [0,  2000],
	bottom: [0,  Infinity],
	left:   [0,  Infinity],
	right:  [0,  Infinity]
}

const checkRectBounds = (rect, bounds) => 
	Object.entries(bounds)
	.map(([k, v]) => checkBound(rect[k], v))
	.every(x => x)

const checkBound = (item, [low, high]) => item > low && item < high

const filter2 = Array.from(document.body.querySelectorAll('*')).filter(i =>
 	i.innerText &&
 	i.childNodes[0].nodeValue &&
 	i.children.length < 5 &&
 	i.querySelectorAll('*').length < 10 &&
 	i.querySelectorAll('canvas,iframe,img,style,script').length == 0 &&
	checkRectBounds(i.getBoundingClientRect(), bounds)
)

