var mpres=false;
var oldX,oldY
var minX=800,minY=400,maxX=0,maxY=0; 

var signCvs = document.getElementById("canvasX");
var signCtx = signCvs.getContext("2d");
signCtx.lineWidth = 3; 
var offset_x = $(signCvs).offset().left;
var offset_y = $(signCvs).offset().top;
var arrData = new Array(0,0); 

var arrX1 = new Array();
var arrY1 = new Array();
var arrX2 = new Array();
var arrY2 = new Array();

function NewXY(tx,ty){
	if(tx<minX)minX=tx;
	if(tx>maxX)maxX=tx;
	if(ty<minY)minY=ty;
	if(ty>maxY)maxY=ty;
}
function Save(){
	 signCtx.clearRect(0,0,800,400);
	 signCtx.canvas.width = maxX - minX + 20;
	 signCtx.canvas.height = maxY - minY + 20;
	 signCtx.lineWidth=3;
	var count= arrX1.length;
	
	minY-=10;
	minX-=10;
	
	for(i=0;i<count;i++){
		//DrawLine(arrX1[i]-minX,arrY1[i]-minY,arrX2[i]-minX,arrY2[i]-minY);
		signCtx.beginPath();
		signCtx.moveTo(arrX1[i]-minX,arrY1[i]-minY);
		signCtx.lineTo(arrX2[i]-minX,arrY2[i]-minY);
		signCtx.closePath();
		signCtx.stroke();
	}
	return signCtx.canvas.toDataURL('image/png');
}
function ClearPad(){
	minX=800;
	minY=400;
	maxX=0;
	maxY=0;
	signCtx.clearRect(0,0,800,400);
	signCtx.canvas.width=800;
	signCtx.canvas.height=400;
	signCtx.lineWidth=3;
	var arrX1 = new Array();
	var arrY1 = new Array();
	var arrX2 = new Array();
	var arrY2 = new Array();
	 
}

function DrawLine(x1,y1,x2,y2,signCtx){	
	signCtx.beginPath();
	signCtx.moveTo(x1,y1);
	signCtx.lineTo(x2,y2);
	signCtx.closePath();
	signCtx.stroke();
	
	arrX1.push(x1);
	arrY1.push(y1);
	arrX2.push(x2);
	arrY2.push(y2);
	
	NewXY(x1,y1);
	NewXY(x2,y2);
	 
 }

$(signCvs).mousedown(function(evt){
	offset_x = $(signCvs).offset().left;
	offset_y = $(signCvs).offset().top;
	mpres=true; 
	oldX = evt.clientX - offset_x;
	oldY = evt.clientY - offset_y; 
});
$(signCvs).mouseup(function(){mpres=false;});
  
$(signCvs).mousemove(function(evt){

 if(!mpres)return;
 
	signCvs = document.getElementById("canvasX");
	signCtx = signCvs.getContext("2d");
	var x = evt.clientX - offset_x;
	var y = evt.clientY - offset_y;
	DrawLine(oldX,oldY,x,y,signCtx) 
	
	oldX=x;
	oldY=y;

});