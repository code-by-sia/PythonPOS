var z=.7;
var AutoFitWidth =true;
function ZoomIn(){
  z=z + 0.1;
  Zoom(z);
}
function ZoomOut(){
  z=z - 0.07;
  Zoom(z);
}

function SetJkLeftPadding(){
    
  var XKW= document.getElementById('XK').getClientRects()[0].width ;//$('#XK').width() * z;
  var JKW= document.getElementById('JK').getClientRects()[0].width;//$('#JK').width();
  var DFF= JKW - XKW;
  
  $('#JK').css('padding-left',Math.ceil( (DFF/2)) + 'px');
  
}

function Zoom(z){
  var s="scale(" + z + ") translate(50%,50%)";// 
  $('#XK').css('-webkit-transform',s)
          .css('-moz-transform',s)
          .css('transform',s);
  SetJkLeftPadding();
  
}

function PrintReport(){
  window.print();		 	
}

function getDPI() {
  return document.getElementById("dpi").offsetHeight;
}

function GetXML () {
  window.location = window.location.toString().replace('Report','xml') ;
}

function fitSize(){
  var dpi =getDPI();
  /*var A4_W= 816 * dpi / 96 ; */
  
  var JK_W= $('#JK').width();
  var XK_W= $('#XK').width();
  var scale= Math.round((100*JK_W) / (XK_W + (dpi / 4)))/100;			
  z=scale;
  Zoom(scale);
  //$('#txtScale').val(scale * 100 + "%").change();
}

function fitWidth(){
  fitSize();
  AutoFitWidth = ! AutoFitWidth;
  if(!AutoFitWidth)
    $('#btnFitWidth').removeClass('active');
  else
    $('#btnFitWidth').addClass('active');
}

function Load(data){
  LoadReport("Report/"+THIS_REPORT,data)
}

function LoadReport(report,data) {
  var el  = parent.document.getElementById('viewerFrame');
  var url = report + "?"+data;
  if(el == undefined){
    window.location="../" + url; 
  }else{
    $(el).attr('src',url);
  }
  $('#dialog').dialog('close');		 
}

function ShowMoney(value) {
	var nStr = value + '';
	var count = nStr.length / 3 ;
	for (var i = 0; i < count; i++) 
		nStr = nStr.replace(/(\d+)(\d{3})/,"$1\/$2");
	return nStr;
}

function ViewInfo(acidValue){
  if(acidValue > 100000000)
    $("#acDetail").load("account.infoModule",{accountNumber:acidValue});
}

$(document).ready(function(){
  
  $(".AccCheckValue").blur(function(){
    var cvalue=$(this).val();
    if(cvalue <= 100000000)
    {
      var acid = FullAcc(cvalue);
      $(this).val(acid);
      if($(this).attr("title")=="Info")
	      ViewInfo(acid);
    }
  }); 

  $("#dialog").dialog({
    bgiframe: false,
    resizable: false,
    modal: true ,
    top:0,
    width:650,
    autoOpen: false  
}); 
$(window).resize(function(){
  if(AutoFitWidth)fitSize();
  SetJkLeftPadding();
});

$('#btnOption').click(function(){
  $("#dialog").dialog('open');
});
$('#btnReload').click(function(){
  var el =parent.document.getElementById('viewerFrame');
  if(el==undefined)
    document.location.reload();
  else
    el.contentDocument.location.reload();
});

  $("input.date").mask("1399/b9/d9");
  fitSize();
 
});
