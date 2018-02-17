var REQ_URL ="";
var REQ_DATA="";
var JS_MODAL=false;
var AccViewInfoFunAttack=null;

var LastMessageId = 0;

function Status(msg){
  $("#StatusBar").html(msg);
}

function CheckNID(num)
{
  var code= num.replace(/[^0-9]/g,'');
  var L=code.length;
  if(L<8 || parseInt(code,10)==0) return false;
  code=('0000'+code).substr(L+4-10);
  if(parseInt(code.substr(3,6),10)==0) return false;
  var c=parseInt(code.substr(9,1),10);
  var s=0;
  for(var i=0;i<9;i++)
    s+=parseInt(code.substr(i,1),10)*(10-i);
  s=s%11;
  return (s<2 && c==s) || (s>=2 && c==(11-s));
  return true;
}


function MemberCode (num) { 
  if(num > 199999)
    return 199999;
  return ('100000').substr(0,6-num.length) + num ;
}


function LoadPage(url,data){
  REQ_URL  = url;
  REQ_DATA = data;
  $("#ModuleContainer").html('<img id="Loading-img" src="/static/loading.gif" />');
  $("#ModuleContainer").load(url,data,ReLoadPage);
}

function PostPage(url,data){
  $.post(url,data,function(response){
    $("#ModuleContainer").html(response);
  });
}

function MessageBox(title,text,btn){
  if(JS_MODAL)
    return;
  JS_MODAL=true ;
  var st='<p title="' + title  + '" >' + text + '</p>';
  $(st).dialog({modal:true,buttons:{
    'تائيد':function(){
      $(this).dialog('destroy');
      JS_MODAL=false;
    }


  }})
}

function logout(){
	$.get('Module/system/logout',function(){
		location.reload();
	});
}

function exit(){
	$.get('Module/system/logout',{
		'action':'session::out'
	},function(){
		window.close();
	});
}
 
function getInt(num){
  num=num.toString()
  return parseInt(num.replace(/[^0-9\-]/g,''));
}

function getNum(str){
  str=str.toString()
  return 1 * (str.replace(/[^0-9\-\.]/g,''));
}

function RefreshPage(){
	LoadPage(REQ_URL,REQ_DATA);
}

function ZoomPic(obj){
  var src=$(obj).attr('src');
  var ig = '<div title="بزرگ نمایی" style="text-align:center;"><img style="min-height:400px;" src="'+src+'" /></div>';
  $(ig).dialog({
    modal:true,
    width:800
  });
}

function BindCheckBox(check,obj){
	$(check).change(function(){
		if($(this).attr("checked")!="")
			$(obj).fadeIn();
		else
			$(obj).fadeOut();
	});
}

function ShowMoney(value) {
	var nStr = value + '';
	var count = nStr.length / 3 ;
	for (var i = 0; i < count; i++) 
		nStr = nStr.replace(/(\d+)(\d{3})/,"$1,$2");
	return nStr;
} 

function MaskDate(obj){$(obj).mask("9999/b9/d9");}
function MaskTime(obj){$(obj).mask("m9:s9");}

function MaskNID(obj){$(obj).mask("999-999999-9");}
function MaskCell(obj){$(obj).mask("0999 999 9999");}
function MaskPhone(obj){$(obj).mask("(999)999-9999");}
function MaskMoney(obj){$(obj).maskMoney();}
function InitMaskMoney () {
  MaskMoney("input.price");
  $(".priceDiv > input.price").keyup(function(){
    var v=$(this).val();
    $(this).parent().find("small").html(convert(v));
  });
}

function ReLoadPage(){

  MaskDate("input.date");
  MaskTime("input.time");
  

  InitMaskMoney();
  $(".priceDiv > input.price").keyup(function(){
    var v=$(this).val();
    $(this).parent().find("small").html(convert(v));
  });

  $('.data-table').dataTable({
    sPaginationType: "full_numbers",
    oLanguage : _i18n_datatable
  });

}

function MakeTable(target){
    $(target).dataTable({sPaginationType: "full_numbers"});
}

$(document).ready(function() {
   
  ReLoadPage();
  $('input').attr('autocomplete','off'); 
  $("#nav a").click(function(){
    var url=$(this).attr("href");
    if(url!="#" && url.length>0)
      LoadPage(url);
    $("#ModuleContainer").focus();
    return false;
  });

	 
	   

});
//window.onunload = logout;
function ShowDocument(Id){
  $.post('report/doc',{'Id':Id,'show_dlg':'sys::yes'},function(resp){
    $('<div title="سند حسابداری" >' +resp + '</div>').dialog({modal:true,width:1024,height:600});
  });	
}

function ShowDocWin(Id){
    window.open('report/doc?Id=' + Id,'doc_' + Id);
}

function SamalDialog(DialogId){
  var dlgCnt=$('#' + DialogId + 'Cnt').html();
  dlgCnt = '<form id="'+ DialogId +'" class="dialog" >' + dlgCnt + '</form>';
  return $(dlgCnt);
}

function ShowPersonInfo(PersonId){
  $.post('person.tableModule',{'PersonId':PersonId},function(info){
    $(info).dialog({modal:true,buttons:{'بستن':function(){$(this).dialog('close');}}});
  });
}

function FormatCurrency(price)
{
	var delimiter = "/"; 
	var amount=price.toString();
	var d = amount; 

	var i = parseInt(d);
	if(isNaN(i)) { return ''; }
	var minus = '';
	if(i < 0) { minus = '-'; }
	i = Math.abs(i);
	var n = new String(i);
	var a = [];
	while(n.length > 3)
	{
		var nn = n.substr(n.length-3);
		a.unshift(nn);
		n = n.substr(0,n.length-3);
	}
	if(n.length > 0) { a.unshift(n); }
	n = a.join(delimiter);
	if(d.length < 1) { amount = n; }
	else { amount = n ; }
	amount = minus + amount;
	return amount;
}

function OpenMessage (id) {
  $.get("user.actionModule",{'act':'open','id':id});
}
function NewMsg (id,sender,message,date,time) {
  if(id <=LastMessageId)return;
  var smsg='';
  smsg +='<div class="info ui-corner-all response-msg " onclick="OpenMessage(' + id + ');$(this).fadeOut(\'slow\');">';
  smsg += '<div class="cont ui-corner-all"><h2>'+ sender  +'</h2>' + date + ' , ' + time + '<br /><br />' + decodeURI(message) + '</div></div>';
  $('#notification').append(smsg);
  LastMessageId=id;
}


function CheckNotifications () {
  // $.getScript("Server-Agent");
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

function CloseDialog  () {
  $('#modal-back').fadeOut(function(){
    $('#modal-container').empty();
    $('#modal-container').removeClass(temp_modal_css);
  });
}


function SumColumn(Table,RowNo){
    var sum=0;
    $( '#' + Table + ' tr > td:nth-child(' + RowNo + ')').each(function(){sum += getNum($(this).text());});
    return sum;
}
function Success(text){
    if(text == undefined){
        text = window.i18n_saved;
    }
    iosOverlay({
		text: text,
		duration: 4e2,
		icon: "/static/images/check.png"
	});
}

function logg(data){
    if(console !== undefined){
        console.log(data);
    }
}