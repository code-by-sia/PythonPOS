function MMV (v){ 
    var s = ",",neg ='';
    if(v < 0){
      v     = -1 * v ;
      neg   = '-' ;
    }
    v = v.toString();
    var a = v.split('.');
    var x = a[0], y = a[1], z = "";
    var l = x.length;
    while (l > 3){
            z = s+x.substr(l-3,3)+z;
            l -=3;
    }
    z = v.substr(0,l)+z;
    if(a.length>1)z=z+'.'+ y;
    return neg+z;
}


var B=0;
var R=0.0;
var OP='';
var SW=0;
var n=1;
function add_calc_digit(nbr){
    if(n ==1 && nbr=='.'){
        n=10;
        return;
    }
    if(n > 1){
        R += nbr / n ;
        n *=  10     ;
    }else{
        R = R * 10 + nbr;
    }
    view_calc_digits();
}
function view_calc_digits(){
    $('#txtCalcDigit').val(MMV(R));
}

function calc_eval_opers(){
    if(OP=='+')R = R + B;
    if(OP=='-')R = B - R;
    if(OP=='*')R = R * B;
    if(OP=='.')R = B / R;

    SW = 1 ;
}
function calc_equal(){
    calc_eval_opers();
    B=0;n=1;OP='eq';SW =0;
    view_calc_digits();
}
function calc_percent(){
    calc_eval_opers();
    B=0;n=1;OP='eq';SW =0;
    R=R / 100;
    view_calc_digits();
}
function calc_opers(opr){
    calc_eval_opers();
    B = R ;
    OP= opr;
    n=1;
    view_calc_digits();
}
function digit_remove(){
    R = Math.floor(R / 10);
    view_calc_digits();       
}
function calc_add_zero(n){
    R = R * Math.pow(10,n);
    view_calc_digits();
}
function calc_func_key(xoper){
    if(SW==1){B=R;R=0.0;SW=0;}
    calc_opers(xoper);
}

function calc_clear() {
    R=0.0;
    B=0;
    n=1;
    OP='';
    view_calc_digits();
}

function keypad_num_click (nbr) {
    if(SW==1){B=R;R=0.0;SW=0;}    
    add_calc_digit(nbr);  
}
function key_detect_calc(evt){
    if(SW==1){B=R;R=0.0;SW=0;}   
    if((evt.keyCode>95) && (evt.keyCode<106))
    {
            var nbr = evt.keyCode-96;
            add_calc_digit(nbr);
    }
    else if((evt.keyCode>47) && (evt.keyCode<58))
    {
            var nbr = evt.keyCode-48;
            add_calc_digit(nbr);
    }
    else if(evt.keyCode==110)   add_calc_digit('.') ;
    else if(evt.keyCode==8  )   digit_remove()      ;
    else if(evt.keyCode==107)   calc_opers('+')     ;
    else if(evt.keyCode==109)   calc_opers('-')     ;
    else if(evt.keyCode==106)   calc_opers('*')     ;
    else if(evt.keyCode==111)   calc_opers('.')     ;
    else if(evt.keyCode==13 )   calc_equal()        ;
    else if(evt.keyCode==27 )   calc_clear()        ;
    else if(evt.keyCode==192)   calc_percent()      ;

}

$(document).ready(function  () {
    $('#txtCalcDigit').focus();
});