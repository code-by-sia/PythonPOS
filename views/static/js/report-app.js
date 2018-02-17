var zoom_factor=5;
var zoom_distance =.5;


function getDPI() {
  return document.getElementById("dpi").offsetHeight;
}

function Zoom(num){
    zoom_factor=num; 
    document.body.style.fontSize=zoom_factor+ 'mm';
}

function ZoomIn(){
    Zoom(zoom_factor + zoom_distance);
}

function ZoomOut(){
    if(zoom_factor< 3.5)return;
    Zoom(zoom_factor - zoom_distance);
}

function FitSize(){
    var dpi =getDPI();
    var page_width= $('page:first-child').width();
    var body_width= $('body').width();
    var scale= Math.round((100*body_width) / (page_width + (dpi / 4)))/100;
    Zoom(scale / 5.5);
}


var temp_modal_css ="";
function ModalDialog (data,args) {

  $('#modal-container')
    .html(data)
    .css('width' ,args.width + 'px')
    .css('height',args.height + 'px')
    .css('margin-left',(args.width /-2) + 'px')
    .css('margin-top' ,(args.height/-2) + 'px');

  if(args.css != undefined){
    temp_modal_css =  args.css;
    $('#modal-container').addClass(args.css);
  }

  if(args.load != undefined) {
    $('#modal-back').fadeIn(args.load);
  }else{
    $('#modal-back').fadeIn();
  }

}

function CloseDialog(){
  $('#modal-back').fadeOut(function(){
    $('#modal-container').empty();
    $('#modal-container').removeClass(temp_modal_css);
  });
}

function ShowOptions(){
    var opsform = $('#options');
    ModalDialog(opsform.html(),{width:500,height:opsform.height()});
}
$(document).ready(FitSize);
