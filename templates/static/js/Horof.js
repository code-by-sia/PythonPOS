
s1 = new Array ("","يک","دو","سه","چهار","پنج","شش","هفت","هشت","نه")
s2 = new Array ("ده","يازده","دوازده","سيزده","چهارده","پانزده","شانزده","هفده","هجده","نوزده")
s3 = new Array ("","","بيست","سي","چهل","پنجاه","شصت","هفتاد","هشتاد","نود")
s4 = new Array ("","صد","دويست","سيصد","چهارصد","پانصد","ششصد","هفتصد","هشتصد","نهصد")
function convert(textZ)
{
//z=textZ.replace("/","");
z=textZ.replace(/[^0-9]/g,'');
z=parseInt(z);
if (z==0) { result="صفر" } else {
result=""
convert2(z) }
 
if (result=="Error")
  return "خطا";
else
  return result + " ریال";

}

function convert2(y)
{
if (y>999999999&&y<1000000000000)
	{  bghb=(y%1000000000); temp=y-bghb; bil=temp/1000000000; convert3r(bil); result=result+" ميليارد"; if (bghb!=0) {result=result+" و "; convert2(bghb); } }
else if (y>999999&&y<=999999999)
	{ bghm=(y%1000000); temp=y-bghm; mil=temp/1000000; convert3r(mil); result=result+" ميليون"; if (bghm!=0) {result=result+" و "; convert2(bghm); }	}
else if (y>999&&y<=999999) { bghh=(y%1000); temp=y-bghh; hez=temp/1000; convert3r(hez); result=result+" هزار"; if (bghh!=0) {result=result+" و "; convert2(bghh); } }
else if (y<=999) convert3r(y); else result="Error" ;
} 

function convert3r(x)
{
bgh=(x%100); temp=x-bgh; sad=temp/100; 
if (bgh==0) { result=result+s4[sad] }
	else	 
	 { 
	  if (x>100) result=result+s4[sad]+" و "; 
	 	if (bgh<10) { result=result+s1[bgh] } 
			else if (bgh<20) { bgh2=(bgh%10); result=result+s2[bgh2] }
				else {
				 	  bgh2=(bgh%10); temp=bgh-bgh2; dah=temp/10; 
					  if (bgh2==0) { result=result+s3[dah] }
					  else { result=result+s3[dah]+" و "+s1[bgh2] }
					 } 
	 }
}
