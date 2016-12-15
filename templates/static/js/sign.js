var mpres=false;
var oldX,oldY;
var Pad_Width=1220,Pad_Height=525;
var minX=Pad_Width,minY=Pad_Height,maxX=0,maxY=0; 

var signCvs = document.getElementById("canvasX");
var signCtx = signCvs.getContext("2d");
signCtx.lineWidth = 3; 
var offset_x = $(signCvs).offset().left;
var offset_y = $(signCvs).offset().top;
var arrData = new Array(0,0); 
 

function NewXY(tx,ty){
	if(tx<minX)minX=tx;
	if(tx>maxX)maxX=tx;
	if(ty<minY)minY=ty;
	if(ty>maxY)maxY=ty;
}
function Save(){
	var SaveCvs = document.createElement('canvas');
	SaveCvs.width = maxX - minX + 20;
	SaveCvs.height = maxY - minY + 20;
	var img =signCtx.getImageData(minX, minY, SaveCvs.width, SaveCvs.height);
	var SaveCtx = SaveCvs.getContext("2d");
	SaveCtx.putImageData(img,10,10);
	return SaveCvs.toDataURL('image/png');
}
function ClearPad(){
	minX=Pad_Width;
	minY=Pad_Height;
	maxX=0;
	maxY=0;
	signCtx.clearRect(0,0,Pad_Width,Pad_Height);
	signCtx.canvas.width=Pad_Width;
	signCtx.canvas.height=Pad_Height;
	signCtx.lineWidth=3;
 }

function DrawLine(x1,y1,x2,y2,signCtx){	
	signCtx.beginPath();
	signCtx.moveTo(x1,y1);
	signCtx.lineTo(x2,y2);
	signCtx.closePath();
	signCtx.stroke();
 
	
	NewXY(x1,y1);
	NewXY(x2,y2);
	 
 }

$(signCvs).mousedown(function(evt){
	offset_x = $(signCvs).offset().left;
	offset_y = $(signCvs).offset().top;
	mpres=true;
	$('#btnClearSignPad').hide();
	oldX = evt.clientX - offset_x;
	oldY = evt.clientY - offset_y; 
});
$(signCvs).mouseup(function(){
	mpres=false;
	$('#btnClearSignPad').show();
});
  
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